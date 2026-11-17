import os
from pathlib import Path
from dotenv import dotenv_values


ENV_PATH = Path(__file__).resolve().parents[1] / ".env"
ENV_VALUES = dotenv_values(ENV_PATH, encoding="utf-8-sig")


def get_setting(name, default=None):
    return ENV_VALUES.get(name) or os.getenv(name) or default


DB_CONFIG = {
    "host": get_setting("ATIVOS_DB_HOST", "192.168.2.220"),
    "port": get_setting("ATIVOS_DB_PORT", "5432"),
    "dbname": get_setting("ATIVOS_DB_NAME", "ativos_ti"),
    "user": get_setting("ATIVOS_DB_USER", "postgres"),
    "password": dotenv_values(
        Path(__file__).resolve().parents[1] / ".env",
        encoding="utf-8-sig",
    ).get("ATIVOS_DB_PASSWORD"),
}

SECRET_KEY = get_setting("ATIVOS_SECRET_KEY")