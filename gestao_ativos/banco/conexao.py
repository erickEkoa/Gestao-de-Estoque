import psycopg2
from gestao_ativos.config import DB_CONFIG


def get_connection():
    return psycopg2.connect(**DB_CONFIG)
