# =============================================================================
# app/config.py — CONFIGURAÇÕES DA APLICAÇÃO
# =============================================================================
# Centraliza todas as configurações em um único lugar.
# Vantagem: se precisar mudar algo (ex: caminho do banco, chave secreta),
# você altera aqui e afeta todo o sistema — sem precisar caçar em vários arquivos.
#
# Em projetos maiores, teríamos várias classes de Config:
#   - Config (base)
#   - DevelopmentConfig (para desenvolver localmente)
#   - ProductionConfig (para o servidor online)
# Por ora usamos uma só, que serve para ambos os casos.
# =============================================================================

from __future__ import annotations

from pathlib import Path  # Módulo para montar caminhos de forma segura (funciona no Windows e Linux)
import os

# ---------------------------------------------------------------------------
# Caminhos do projeto
# ---------------------------------------------------------------------------
# Path(__file__) = caminho deste arquivo (config.py)
# .resolve()     = transforma em caminho absoluto (ex: D:\Meu Portfolio e HUB\app\config.py)
# .parent        = pasta pai (app/)
# .parent        = pasta avó (D:\Meu Portfolio e HUB/) ← raiz do projeto
BASE_DIR = Path(__file__).resolve().parent.parent  # Raiz do projeto

DATA_DIR = BASE_DIR / "data"      # Pasta onde o banco de dados fica (data/)
DB_PATH  = DATA_DIR / "app.db"   # Arquivo do banco: data/app.db


class Config:
    """
    Configurações padrão da aplicação.

    Todos os valores aqui podem ser sobrescritos por variáveis de ambiente
    em produção (Railway, Render, etc.), o que é uma boa prática de segurança.
    """

    # -------------------------------------------------------------------------
    # SECRET_KEY — Chave secreta do Flask
    # -------------------------------------------------------------------------
    # Usada para assinar cookies de sessão (onde guardamos o "Modo Recrutador").
    # Em produção, troque por uma string longa e aleatória e guarde em variável
    # de ambiente — NUNCA deixe uma chave fraca em produção!
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-change-me")

    # -------------------------------------------------------------------------
    # SQLALCHEMY_DATABASE_URI — Endereço do banco de dados
    # -------------------------------------------------------------------------
    # Formato SQLite: "sqlite:///caminho/para/arquivo.db"
    # Em produção (Render, etc.), use variável de ambiente DATABASE_URL (ex.: postgres://...)
    # SQLAlchemy aceita "postgresql://"; normalizamos caso venha "postgres://".
    _env_db = os.environ.get("DATABASE_URL", "").strip()
    if _env_db:
        if _env_db.startswith("postgres://"):
            _env_db = _env_db.replace("postgres://", "postgresql://", 1)
        SQLALCHEMY_DATABASE_URI = _env_db
    else:
        # O banco inteiro é um único arquivo .db — fácil de fazer backup.
        # .as_posix() garante que as barras funcionem tanto no Windows quanto no Linux
        SQLALCHEMY_DATABASE_URI = f"sqlite:///{DB_PATH.as_posix()}"

    # Desativa o sistema de rastreamento de mudanças do SQLAlchemy
    # (consome memória e não usamos — melhor desligado)
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # -------------------------------------------------------------------------
    # JSON_AS_ASCII — Preserva caracteres especiais no JSON
    # -------------------------------------------------------------------------
    # False = permite acentos (ã, é, ç) no JSON exportado, em vez de usar códigos
    JSON_AS_ASCII = False

    # -------------------------------------------------------------------------
    # PROFILE_PHOTO_URL — URL pública da sua foto de perfil (opcional)
    # -------------------------------------------------------------------------
    # Caso queira usar uma foto hospedada (ex: CDN, site pessoal), defina aqui a URL.
    # Se deixar em branco, a aplicação tentará usar o arquivo local
    # static/img/profile.jpg, quando existir.
    PROFILE_PHOTO_URL = ""
