# =============================================================================
# app/__init__.py — O "CONSTRUTOR" DA APLICAÇÃO (Application Factory)
# =============================================================================
# Este arquivo é o coração da pasta "app/". Em Python, todo diretório que
# tem um arquivo __init__.py é tratado como um "pacote" (uma coleção de módulos).
#
# Aqui seguimos um padrão chamado "Application Factory" (fábrica de aplicação).
# Em vez de criar a aplicação diretamente no topo do arquivo, criamos uma
# FUNÇÃO (create_app) que monta tudo sob demanda. Isso facilita testes e
# configurações diferentes (ex: produção vs. desenvolvimento).
#
# O que acontece neste arquivo:
#   1. Cria as "ferramentas" globais: banco de dados e sistema de migrações
#   2. Define a função create_app() que monta tudo
#   3. Na primeira execução, cria as tabelas do banco e insere dados de exemplo
# =============================================================================

from __future__ import annotations

from pathlib import Path        # Módulo para trabalhar com caminhos de arquivos
from flask import Flask         # O framework web que usamos
from flask_sqlalchemy import SQLAlchemy   # Ferramenta para falar com o banco de dados
from flask_migrate import Migrate         # Ferramenta para atualizar o banco quando os modelos mudam

# ---------------------------------------------------------------------------
# Ferramentas globais (instâncias compartilhadas por todo o projeto)
# ---------------------------------------------------------------------------
# Criamos aqui, mas só "ligamos" dentro de create_app().
# Isso evita que o banco tente conectar antes de sabermos qual app vai usar.
db = SQLAlchemy()   # Representa o banco de dados SQLite
migrate = Migrate() # Gerencia mudanças na estrutura do banco (adicionar colunas, etc.)


def create_app(config_object: str | None = None) -> Flask:
    """
    Função que constrói e configura toda a aplicação Flask.

    Pense nela como a linha de montagem de uma fábrica:
      - Pega as configurações (config.py)
      - Garante que a pasta do banco existe
      - Liga as ferramentas (banco, migrações)
      - Registra as rotas/páginas (routes.py)
      - Cria as tabelas do banco na primeira execução
    """

    # Cria a aplicação Flask
    # __name__ diz ao Flask em qual pasta ele está
    # template_folder aponta para a pasta "templates/" na raiz do projeto
    # static_folder aponta para a pasta "static/" (CSS, JS, imagens)
    app = Flask(
        __name__,
        instance_relative_config=False,
        template_folder="../templates",
        static_folder="../static"
    )

    # Define qual arquivo de configuração usar (padrão: app/config.py → classe Config)
    if config_object is None:
        config_object = "app.config.Config"
    app.config.from_object(config_object)  # Carrega as configurações

    # ---------------------------------------------------------------------------
    # Garante que a pasta "data/" existe (onde o arquivo do banco SQLite fica)
    # ---------------------------------------------------------------------------
    # O banco de dados é um único arquivo: data/app.db
    # Se a pasta não existir, criamos ela automaticamente
    db_uri = app.config.get("SQLALCHEMY_DATABASE_URI", "")
    if db_uri.startswith("sqlite"):
        try:
            # Extrai o caminho do arquivo a partir da URI (ex: "sqlite:///data/app.db")
            path = db_uri.split("///", 1)[1]
            Path(path).parent.mkdir(parents=True, exist_ok=True)  # Cria a pasta se não existir
        except Exception:
            pass  # Se falhar, ignora (pode ser um banco em memória)

    # ---------------------------------------------------------------------------
    # Liga as ferramentas à aplicação
    # ---------------------------------------------------------------------------
    db.init_app(app)       # Conecta o SQLAlchemy à nossa app Flask
    migrate.init_app(app, db)  # Conecta o Flask-Migrate para poder rodar migrações

    # ---------------------------------------------------------------------------
    # Registra as rotas (páginas e ações do sistema)
    # ---------------------------------------------------------------------------
    # Importamos aqui dentro (e não no topo) para evitar um problema chamado
    # "importação circular" — routes.py precisa do db, que precisa da app...
    from .routes import bp as main_bp
    app.register_blueprint(main_bp)  # Diz ao Flask: "use essas rotas"

    @app.context_processor
    def inject_globals():
        from flask import session as _s
        return {
            "is_admin": bool(_s.get("is_admin", False)),
        }

    # ---------------------------------------------------------------------------
    # Cria as tabelas do banco e insere dados de exemplo (apenas na 1ª execução)
    # ---------------------------------------------------------------------------
    from .models import Task, Project, Certificate  # Importa os modelos para criar as tabelas

    with app.app_context():  # "Contexto de aplicação": necessário para acessar o banco
        db.create_all()      # Cria todas as tabelas que ainda não existem no banco

        # Adiciona colunas novas em tabelas existentes (db.create_all não faz isso)
        from sqlalchemy import inspect as _inspect, text as _text
        _insp = _inspect(db.engine)
        _proj_cols = [c["name"] for c in _insp.get_columns("projects")]
        if "sustained" not in _proj_cols:
            db.session.execute(_text("ALTER TABLE projects ADD COLUMN sustained BOOLEAN NOT NULL DEFAULT FALSE"))
            db.session.commit()

        # Se o banco estiver vazio (primeira vez que a app roda), insere dados de exemplo
        # Isso serve para mostrar como o sistema funciona sem precisar cadastrar nada
        if Task.query.count() == 0 and Project.query.count() == 0:
            import datetime as _dt

            # Tarefas de exemplo (Objetivos)
            sample_tasks = [
                Task(title="Aprender IA Generativa", area="IA e Agentes", priority="Alta", status="Em andamento", due=_dt.date(2026, 10, 15), hours=12),
                Task(title="Obter certificação Cloud", area="Cloud", priority="Alta", status="Não iniciado", due=_dt.date(2026, 11, 1), hours=20),
                Task(title="Concluir projeto interno", area="Projetos", priority="Média", status="Em andamento", due=_dt.date(2026, 10, 30), hours=16),
                Task(title="Evoluir habilidades de automação", area="Automação", priority="Média", status="Não iniciado", due=_dt.date(2026, 12, 1), hours=10),
                # Cursos como tarefas
                Task(title="Python Fundamentals", area="Cursos", priority="Média", status="Não iniciado", hours=8),
                Task(title="Power BI Essentials", area="Cursos", priority="Média", status="Não iniciado", hours=6),
                Task(title="UiPath Advanced Developer", area="Cursos", priority="Alta", status="Em andamento", hours=20),
                Task(title="Azure Fundamentals", area="Cursos", priority="Média", status="Não iniciado", hours=10),
            ]

            # Projetos de exemplo (genéricos)
            sample_projects = [
                Project(name="Customer Service Bot", description="Chatbot para atendimento com automações de backoffice.", stack="RPA, APIs, NLP", progress=45, status="Em desenvolvimento", project_type="Pessoal", fte_hours=80.0),
                Project(name="Inventory Automation", description="Automação de inventário e integração com ERP.", stack="RPA, SAP, APIs", progress=100, status="Concluído", project_type="Pessoal", fte_hours=60.0),
                Project(name="Document Processing AI", description="Classificação e extração de dados de documentos.", stack="AI, OCR, LLM", progress=70, status="Em desenvolvimento", project_type="Pessoal", fte_hours=120.0),
                Project(name="Data Analytics Dashboard", description="Dashboard analítico com indicadores de negócio.", stack="Power BI, SQL", progress=30, status="Discovery", project_type="Pessoal", fte_hours=40.0),
            ]

            # Certificações de exemplo
            sample_certificates = [
                Certificate(name="AWS Cloud Practitioner", issuer="AWS", area="Cloud", featured=True),
                Certificate(name="Microsoft Azure Fundamentals (AZ-900)", issuer="Microsoft", area="Cloud", featured=True),
                Certificate(name="UiPath Advanced Developer", issuer="UiPath", area="RPA", featured=True),
            ]

            db.session.add_all(sample_tasks + sample_projects + sample_certificates)
            db.session.commit()

        # Se não houver nenhum certificado cadastrado (ex.: migração para novo banco),
        # garante a carga inicial mesmo que já existam tasks/projetos
        if Certificate.query.count() == 0:
            seed_certs = [
                Certificate(name="AWS Cloud Practitioner", issuer="AWS", area="Cloud", featured=True),
                Certificate(name="Microsoft Azure Fundamentals (AZ-900)", issuer="Microsoft", area="Cloud", featured=True),
                Certificate(name="UiPath Advanced Developer", issuer="UiPath", area="RPA", featured=True),
            ]
            db.session.add_all(seed_certs)
            db.session.commit()

    return app  # Retorna a aplicação pronta para uso


# Garante que os modelos sejam importados quando alguém importar este pacote
# Necessário para que o Flask-Migrate consiga enxergar todos os modelos
from . import models  # noqa: E402
