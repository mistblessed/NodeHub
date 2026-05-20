import psycopg2
from psycopg2 import pool, errors
from app.config import Config

_connection_pool = None

def get_pool():
    global _connection_pool
    if _connection_pool is None:
        config = Config()
        _connection_pool = pool.ThreadedConnectionPool(
            minconn=1,
            maxconn=5,                     # уменьшаем максимальное количество соединений
            host=config.DB_HOST,
            port=config.DB_PORT,
            dbname=config.DB_NAME,
            user=config.DB_USER,
            password=config.DB_PASSWORD,
            client_encoding='UTF8',
            sslmode='require',
            connect_timeout=10,            # таймаут подключения
            keepalives=1,                  # включение keepalive
            keepalives_idle=30,            # секунд простоя до проверки
            keepalives_interval=10,        # интервал между проверками
            keepalives_count=5             # количество попыток
        )
    return _connection_pool

def get_connection():
    """Получает соединение из пула."""
    return get_pool().getconn()

def return_connection(conn, close=False):
    """
    Возвращает соединение в пул.
    Если close=True, соединение закрывается и удаляется из пула.
    """
    if close:
        get_pool().putconn(conn, close=True)
    else:
        get_pool().putconn(conn)

def execute_query(query, params=None, fetch=False):
    """
    Выполняет SQL-запрос, при необходимости возвращает результат.
    При возникновении ошибки соединение закрывается.
    """
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
            return_connection(conn, close=True)   # закрываем сбойное соединение
        raise e
    else:
        if conn:
            return_connection(conn)                # успешное выполнение — возвращаем в пул
    return result

def fetch_one(query, params=None):
    """Выполняет SELECT и возвращает одну запись в виде словаря."""
    result = execute_query(query, params, fetch=True)
    return result[0] if result else None

def fetch_all(query, params=None):
    """Выполняет SELECT и возвращает все записи в виде списка словарей."""
    return execute_query(query, params, fetch=True)

def execute_insert(query, params=None):
    """
    Выполняет INSERT-запрос и возвращает id вставленной записи.
    При ошибке соединение закрывается.
    """
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