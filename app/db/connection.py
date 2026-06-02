import time
import psycopg2
from psycopg2 import pool
from app.config import Config

_connection_pool = None

def get_pool():
    global _connection_pool
    if _connection_pool is None:
        config = Config()
        _connection_pool = pool.ThreadedConnectionPool(
            minconn=1,
            maxconn=5,
            host=config.DB_HOST,
            port=config.DB_PORT,
            dbname=config.DB_NAME,
            user=config.DB_USER,
            password=config.DB_PASSWORD,
            client_encoding='UTF8',
            sslmode='require',
            connect_timeout=10,
            keepalives=1,
            keepalives_idle=30,
            keepalives_interval=10,
            keepalives_count=5
        )
    return _connection_pool

def get_connection():
    """
    Получает соединение из пула с повторными попытками.
    Если БД временно недоступна, делает до MAX_RETRIES попыток
    с экспоненциальной задержкой.
    """
    config = Config()
    max_retries = getattr(config, 'DB_MAX_RETRIES', 5)
    base_delay = getattr(config, 'DB_RETRY_DELAY', 0.5)

    for attempt in range(max_retries):
        try:
            return get_pool().getconn()
        except (psycopg2.OperationalError, psycopg2.InterfaceError) as e:
            if attempt == max_retries - 1:
                raise e
            delay = base_delay * (2 ** attempt)
            time.sleep(delay)
    # Эта строка никогда не выполнится, но для надёжности:
    raise Exception("Не удалось подключиться к БД после нескольких попыток")

def return_connection(conn, close=False):
    if close:
        get_pool().putconn(conn, close=True)
    else:
        get_pool().putconn(conn)

def execute_query(query, params=None, fetch=False):
    conn = None
    result = None
    try:
        conn = get_connection()
        with conn.cursor() as cur:
            cur.execute(query, params)
            if fetch:
                columns = [desc[0] for desc in cur.description] if cur.description else []
                rows = cur.fetchall()
                result = [dict(zip(columns, row)) for row in rows]
            conn.commit()
    except Exception as e:
        if conn:
            try:
                conn.rollback()
            except Exception:
                pass
            return_connection(conn, close=True)
        raise e
    else:
        if conn:
            return_connection(conn)
    return result

def fetch_one(query, params=None):
    result = execute_query(query, params, fetch=True)
    return result[0] if result else None

def fetch_all(query, params=None):
    return execute_query(query, params, fetch=True)

def execute_insert(query, params=None):
    conn = None
    inserted_id = None
    try:
        conn = get_connection()
        with conn.cursor() as cur:
            cur.execute(query, params)
            row = cur.fetchone()
            if row:
                inserted_id = row[0]
            conn.commit()
    except Exception as e:
        if conn:
            try:
                conn.rollback()
            except Exception:
                pass
            return_connection(conn, close=True)
        raise e
    else:
        if conn:
            return_connection(conn)
    return inserted_id