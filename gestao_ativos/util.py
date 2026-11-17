import hashlib
from werkzeug.utils import secure_filename


def gerar_hash_senha(senha):
    return hashlib.sha256(senha.encode("utf-8")).hexdigest()


def normalizar_nome_arquivo(nome_arquivo):
    nome_seguro = secure_filename(nome_arquivo or "")
    if not nome_seguro:
        nome_seguro = "anexo"
    return nome_seguro


def to_int_or_none(value):
    if value in (None, "", "None"):
        return None
    return int(value)
