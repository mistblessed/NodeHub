import psycopg2
from psycopg2 import pool
from app.config import Config

# Глобальная переменная для пула соединений
_connection_pool = None

def get_pool():
    """Инициализирует и возвращает пул соединений (синглтон)."""
    global _connection_pool
    if _connection_pool is None:
        config = Config()
        _connection_pool = pool.ThreadedConnectionPool(
            minconn=1,
            maxconn=10,
            host=config.DB_HOST,
            port=config.DB_PORT,
            dbname=config.DB_NAME,
            user=config.DB_USER,
            password=config.DB_PASSWORD,
            client_encoding='UTF8'
        )
    return _connection_pool

def get_connection():
    """Возвращает соединение из пула."""
    return get_pool().getconn()

def return_connection(conn):
    """Возвращает соединение обратно в пул."""
    get_pool().putconn(conn)

def execute_query(query, params=None, fetch=False):
    """
    Выполняет SQL-запрос, при необходимости возвращает результат.
    :param query: строка SQL
    :param params: кортеж параметров для параметризованного запроса
    :param fetch: если True, возвращает список словарей (для SELECT)
    :return: результат выборки или None
    """
    conn = None
    result = None
    try:
        conn = get_connection()
        with conn.cursor() as cur:
            cur.execute(query, params)
            if fetch:
                # Получаем названия колонок
                columns = [desc[0] for desc in cur.description] if cur.description else []
                rows = cur.fetchall()
                result = [dict(zip(columns, row)) for row in rows]
            conn.commit()
    except Exception as e:
        if conn:
            conn.rollback()
        raise e
    finally:
        if conn:
            return_connection(conn)
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
    Предполагается, что запрос содержит RETURNING id.
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
            conn.rollback()
        raise e
    finally:
        if conn:
            return_connection(conn)
    return inserted_id