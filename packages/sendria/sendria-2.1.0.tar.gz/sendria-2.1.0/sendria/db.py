__all__ = ['setup', 'connection', 'add_message', 'delete_message', 'delete_messages', 'get_message',
    'get_message_attachments', 'get_message_part_cid', 'get_message_part_html', 'get_message_part_plain',
    'get_messages', 'message_saver',
]

import asyncio
import json
import pathlib
import sqlite3
from contextlib import asynccontextmanager
from typing import Iterable, Optional, Union, List, NoReturn

import aiosqlite
from structlog import get_logger

from . import callback
from .http import notifier
from .message import Message

logger = get_logger()
DB_PATH: Optional[str] = None
DbMessagesQueue: Optional[asyncio.Queue] = None


async def setup(db: Union[str, pathlib.Path]) -> NoReturn:
    global DB_PATH, DbMessagesQueue
    DB_PATH = str(db)

    DbMessagesQueue = asyncio.Queue()

    async with connection() as conn:
        await create_tables(conn)
        logger.info('DB initialized')


@asynccontextmanager
async def connection() -> NoReturn:
    conn = await aiosqlite.connect(DB_PATH, detect_types=sqlite3.PARSE_DECLTYPES)
    conn.row_factory = aiosqlite.Row
    conn.text_factory = str
    try:
        yield conn
    finally:
        await conn.close()


async def create_tables(conn: aiosqlite.Connection) -> NoReturn:
    await conn.execute("""
        CREATE TABLE IF NOT EXISTS message (
            id INTEGER PRIMARY KEY ASC,
            sender_envelope TEXT,
            sender_message TEXT,
            recipients_envelope TEXT,
            recipients_message_to TEXT,
            recipients_message_cc TEXT,
            recipients_message_bcc TEXT,
            subject TEXT,
            source BLOB,
            size INTEGER,
            type TEXT,
            peer TEXT,
            created_at TIMESTAMP
        )
    """)

    await conn.execute("""
        CREATE TABLE IF NOT EXISTS message_part (
            id INTEGER PRIMARY KEY ASC,
            message_id INTEGER NOT NULL,
            cid TEXT,
            type TEXT,
            is_attachment INTEGER,
            filename TEXT,
            charset TEXT,
            body BLOB,
            size INTEGER,
            created_at TIMESTAMP
        )
    """)


def add_message(message: Message) -> NoReturn:
    DbMessagesQueue._loop.call_soon_threadsafe(DbMessagesQueue.put_nowait, message)


async def message_saver() -> NoReturn:
    while True:
        message: Message = await DbMessagesQueue.get()
        async with connection() as conn:
            await store_message(conn, message)
        DbMessagesQueue.task_done()


async def store_message(conn: aiosqlite.Connection, message: Message) -> int:
    sql = """
        INSERT INTO message
            (sender_envelope, sender_message, recipients_envelope, recipients_message_to,
             recipients_message_cc, recipients_message_bcc, subject,
              source, type, size, peer, created_at)
        VALUES
            (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, datetime('now'))
    """

    cur = await conn.cursor()

    try:
        await cur.execute(
            sql,
            (
                message.sender_envelope,
                message.sender_message,
                message.recipients_envelope,
                json.dumps(message.recipients_message_to),
                json.dumps(message.recipients_message_cc),
                json.dumps(message.recipients_message_bcc),
                message.subject,
                message.source,
                message.type,
                message.size,
                message.peer,
            )
        )
        message.id = cur.lastrowid
        # Store parts (why do we do this for non-multipart at all?!)
        for part in message.parts:
            part_id = await _save_message_part(cur, message.id, part['cid'], part['part'])
            part['part_id'] = part_id
        await cur.execute('COMMIT')
    finally:
        await cur.close()

    logger.debug('message stored', message_id=message.id,
        parts=[{'part_id': part['part_id'], 'cid': part['cid']} for part in message.parts])
    await notifier.broadcast('add_message', message.id)
    await callback.enqueue(message)
    return message.id


async def _save_message_part(cur: aiosqlite.Cursor, message_id: int, cid: str, part) -> int:
    sql = """
        INSERT INTO message_part
            (message_id, cid, type, is_attachment, filename, charset, body, size, created_at)
        VALUES
            (?, ?, ?, ?, ?, ?, ?, ?, datetime('now'))
    """

    body = part.get_payload(decode=True)
    body_len = len(body) if body else 0
    await cur.execute(
        sql,
        (
            message_id,
            cid,
            part.get_content_type(),
            part.get_filename() is not None,
            part.get_filename(),
            part.get_content_charset(),
            body,
            body_len
        )
    )
    return cur.lastrowid


def _parse_recipients(recipients: Optional[str]) -> List[str]:
    if not recipients:
        return []
    recipients = json.loads(recipients)
    return recipients


def _prepare_message_row_inplace(row: dict) -> NoReturn:
    row['recipients_envelope'] = Message.split_addresses(row['recipients_envelope'])
    row['recipients_message_to'] = _parse_recipients(row['recipients_message_to'])
    row['recipients_message_cc'] = _parse_recipients(row['recipients_message_cc'])
    row['recipients_message_bcc'] = _parse_recipients(row['recipients_message_bcc'])


async def get_message(conn: aiosqlite.Connection, message_id: int) -> Optional[dict]:
    async with conn.execute('SELECT * FROM message WHERE id = ?', (message_id,)) as cur:
        row = await cur.fetchone()
    if not row:
        return None
    row = dict(row)
    _prepare_message_row_inplace(row)
    return row


async def get_message_attachments(conn: aiosqlite.Connection, message_id: int) -> Iterable[sqlite3.Row]:
    sql = """
        SELECT
            message_id, cid, type, filename, size
        FROM
            message_part
        WHERE
            message_id = ? AND
            is_attachment = 1
        ORDER BY
            filename ASC
    """
    async with conn.execute(sql, (message_id,)) as cur:
        data = await cur.fetchall()

    return data


async def _get_message_part_types(conn: aiosqlite.Connection, message_id: int, types: List[str]) -> sqlite3.Row:
    sql = """
        SELECT
            *
        FROM
            message_part
        WHERE
            message_id = ? AND
            type IN ({0}) AND
            is_attachment = 0
        LIMIT
            1
    """.format(','.join('?' * len(types)))

    async with conn.execute(sql, (message_id,) + types) as cur:
        data = await cur.fetchone()
    return data


async def get_message_part_html(conn: aiosqlite.Connection, message_id: int) -> sqlite3.Row:
    return await _get_message_part_types(conn, message_id, ('text/html', 'application/xhtml+xml'))


async def get_message_part_plain(conn: aiosqlite.Connection, message_id: int) -> sqlite3.Row:
    return await _get_message_part_types(conn, message_id, ('text/plain',))


async def get_message_part_cid(conn: aiosqlite.Connection, message_id: int, cid: str) -> sqlite3.Row:
    async with conn.execute('SELECT * FROM message_part WHERE message_id = ? AND cid = ?', (message_id, cid)) as cur:
        data = await cur.fetchone()
    return data


async def _message_has_types(conn: aiosqlite.Connection, message_id: int, types: List[str]) -> bool:
    sql = """
        SELECT
            1
        FROM
            message_part
        WHERE
            message_id = ? AND
            is_attachment = 0 AND
            type IN ({0})
        LIMIT
            1
    """.format(','.join('?' * len(types)))
    async with conn.execute(sql, (message_id,) + types) as cur:
        data = await cur.fetchone()
    return data is not None


async def message_has_html(conn: aiosqlite.Connection, message_id: int) -> bool:
    return await _message_has_types(conn, message_id, ('application/xhtml+xml', 'text/html'))


async def message_has_plain(conn: aiosqlite.Connection, message_id: int) -> bool:
    return await _message_has_types(conn, message_id, ('text/plain',))


async def get_messages(conn: aiosqlite.Connection) -> List[dict]:
    async with conn.execute('SELECT * FROM message ORDER BY created_at ASC') as cur:
        data = await cur.fetchall()

    data = list(map(dict, data))
    for row in data:
        _prepare_message_row_inplace(row)
    return data


async def delete_message(conn: aiosqlite.Connection, message_id: int) -> NoReturn:
    cur = await conn.cursor()
    try:
        await cur.execute('DELETE FROM message WHERE id = ?', (message_id,))
        await cur.execute('DELETE FROM message_part WHERE message_id = ?', (message_id,))
        await cur.execute('COMMIT')
    finally:
        await cur.close()
    logger.debug('message deleted', message_id=message_id)
    await notifier.broadcast('delete_message', message_id)


async def delete_messages(conn: aiosqlite.Connection) -> NoReturn:
    cur = await conn.cursor()
    try:
        await cur.execute('DELETE FROM message')
        await cur.execute('DELETE FROM message_part')
        await cur.execute('COMMIT')
    finally:
        await cur.close()
    logger.debug('all messages deleted')
    await notifier.broadcast('delete_messages')
