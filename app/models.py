# =============================================================================
# app/models.py — MODELOS DO BANCO DE DADOS (ORM)
# =============================================================================
# ORM = Object-Relational Mapping (Mapeamento Objeto-Relacional)
#
# Pense nos modelos como "fichas cadastrais" que descrevem o que o banco
# de dados vai armazenar. Cada CLASSE Python vira uma TABELA no banco.
# Cada ATRIBUTO da classe vira uma COLUNA nessa tabela.
#
# Exemplo prático:
#   class Task → tabela "tasks" no banco SQLite
#   task.title  → coluna "title" da linha correspondente
#
# O SQLAlchemy (nossa ferramenta ORM) traduz operações Python em SQL:
#   Task.query.all()           →  SELECT * FROM tasks
#   db.session.add(task)       →  INSERT INTO tasks ...
#   db.session.delete(task)    →  DELETE FROM tasks WHERE id = ...
#
# Temos 3 modelos (3 tabelas):
#   1. Task          — tarefas do plano de aprendizado
#   2. Project       — projetos do portfólio
#   3. SkillCategory — categorias de competências técnicas
# =============================================================================

from __future__ import annotations

from datetime import date       # Tipo de dado para datas (ano-mês-dia)
from typing import Optional     # Para campos que podem ser nulos (None)

from . import db  # Importa o objeto do banco de dados criado em __init__.py


# =============================================================================
# MODELO 1: Task — Tarefa do plano de aprendizado
# =============================================================================
class Task(db.Model):
    """
    Representa uma tarefa no plano de aprendizado (aba "Plano").

    Cada tarefa tem: título, área, prioridade, status, prazo, horas e
    campos opcionais de evidência e anotações.
    """

    __tablename__ = "tasks"  # Nome da tabela no banco de dados

    # -------------------------------------------------------------------------
    # Colunas da tabela (cada db.Column = uma coluna no banco)
    # -------------------------------------------------------------------------

    # ID único gerado automaticamente — cada tarefa tem um número único
    id: int = db.Column(db.Integer, primary_key=True)

    # Título da tarefa — obrigatório, até 200 caracteres
    title: str = db.Column(db.String(200), nullable=False)

    # Área temática: "IA e Agentes", "UiPath", "Power Automate", etc.
    area: str = db.Column(db.String(80), nullable=False, default="IA e Agentes")

    # Nível de prioridade: "Alta", "Média" ou "Baixa"
    priority: str = db.Column(db.String(20), nullable=False, default="Média")

    # Estado atual: "Não iniciado", "Em andamento" ou "Concluído"
    status: str = db.Column(db.String(30), nullable=False, default="Não iniciado")

    # Prazo da tarefa — Optional significa que pode ficar em branco (None)
    due: Optional[date] = db.Column(db.Date, nullable=True)

    # Horas estimadas para completar a tarefa
    hours: int = db.Column(db.Integer, nullable=False, default=1)

    # Flag (bandeira) booleana: True = concluída, False = pendente
    # Usada para filtros e cálculo de progresso
    completed: bool = db.Column(db.Boolean, nullable=False, default=False)

    # Link para evidência (GitHub, vídeo, artigo, etc.) — opcional
    evidence: str = db.Column(db.String(500), nullable=True)

    # Anotações livres — opcional
    notes: str = db.Column(db.String(500), nullable=True)

    def mark_toggle(self) -> None:
        """
        Alterna o status da tarefa entre concluída e em andamento.

        Funciona como um interruptor (toggle):
          - Se estiver CONCLUÍDA → volta para "Em andamento" e marca completed=False
          - Se NÃO estiver concluída → marca como "Concluído" e completed=True

        Chamada quando você clica no botão "✓ Concluir" ou "↩ Desfazer".
        """
        # Verifica se a tarefa já está concluída (por flag OU por status)
        done = bool(self.completed or self.status == "Concluído")

        # Inverte o estado
        self.completed = not done
        self.status = "Concluído" if not done else "Em andamento"


# =============================================================================
# MODELO 2: Project — Projeto do portfólio
# =============================================================================
class Project(db.Model):
    """
    Representa um projeto no portfólio (aba "Projetos").

    Cada projeto tem: nome, descrição, stack de tecnologias, progresso,
    status e links opcionais para repositório, demo e evidências.
    """

    __tablename__ = "projects"  # Nome da tabela no banco

    id: int = db.Column(db.Integer, primary_key=True)

    # Nome do projeto — obrigatório
    name: str = db.Column(db.String(160), nullable=False)

    # Descrição em texto livre — opcional
    description: str = db.Column(db.Text, nullable=True)

    # Tecnologias usadas, guardadas como texto separado por vírgulas
    # Exemplo: "Python, Flask, SQLAlchemy, SQLite"
    # Usamos CSV (texto simples) em vez de uma tabela separada — mais simples para este caso
    stack: str = db.Column(db.Text, nullable=True)

    # Percentual de conclusão (0 a 100)
    progress: int = db.Column(db.Integer, nullable=False, default=0)

    # Fase do projeto: "Backlog", "Discovery", "Em desenvolvimento", "Concluído"
    status: str = db.Column(db.String(40), nullable=False, default="Backlog")

    # Links externos — todos opcionais
    repo: str = db.Column(db.String(300), nullable=True)       # Repositório GitHub
    demo: str = db.Column(db.String(300), nullable=True)       # Link de demonstração
    evidence: str = db.Column(db.String(300), nullable=True)   # Evidência (vídeo, doc, etc.)
    highlight: str = db.Column(db.String(300), nullable=True)  # Destaque principal
    
    # Tipo de projeto: "Pessoal" ou "Corporativo"
    # Projetos corporativos não expõem detalhes sensíveis (LGPD/confidencialidade)
    project_type: str = db.Column(db.String(20), nullable=False, default="Pessoal")
    
    # Horas economizadas (FTE) — apenas para projetos corporativos
    fte_hours: float = db.Column(db.Float, nullable=True)

    # Flag: projeto sustentado em produção (manutenção, evolução, troubleshooting)
    sustained: bool = db.Column(db.Boolean, nullable=False, default=False)

    def stack_list(self) -> list[str]:
        """
        Converte o campo 'stack' (texto CSV) em uma lista Python.

        Exemplo:
          self.stack = "Python, Flask, SQLite"
          → retorna ["Python", "Flask", "SQLite"]

        Usado nos templates para exibir cada tecnologia como um badge separado.
        """
        if not self.stack:
            return []  # Se não tiver stack, retorna lista vazia
        # Divide pelo símbolo de vírgula e remove espaços extras de cada item
        return [s.strip() for s in self.stack.split(",") if s.strip()]


# =============================================================================
# MODELO 3: SkillCategory — Categoria de competências
# =============================================================================
class SkillCategory(db.Model):
    """
    Representa uma categoria de competências técnicas (aba "Competências").

    Cada categoria tem: ícone emoji, título e uma lista de competências
    (guardada como texto CSV, igual ao 'stack' dos projetos).

    Exemplos de categorias:
      🤖 RPA e Arquitetura → "REFramework, Queues, SAP Automation"
      ✨ IA e Agentes      → "Copilot Studio, LLMs, AI Agents"
    """

    __tablename__ = "skill_categories"  # Nome da tabela no banco

    id: int = db.Column(db.Integer, primary_key=True)

    # Título da categoria (ex: "RPA e Arquitetura")
    title: str = db.Column(db.String(80), nullable=False)

    # Emoji que representa visualmente a categoria (ex: "🤖", "✨", "💻")
    icon: str = db.Column(db.String(10), nullable=False, default="⚡")

    # Lista de competências em formato CSV (separadas por vírgula)
    # Exemplo: "REFramework avançado, Queues, SAP Automation, Logs e retries"
    items: str = db.Column(db.Text, nullable=True)

    # Número para controlar a ordem de exibição no grid
    # Categoria com order=0 aparece primeiro, order=1 aparece segundo, etc.
    order: int = db.Column(db.Integer, nullable=False, default=0)

    def items_list(self) -> list[str]:
        if not self.items:
            return []
        return [s.strip() for s in self.items.split(",") if s.strip()]


# =============================================================================
# MODELO 4: Certificate — Certificado de curso ou formação
# =============================================================================
class Certificate(db.Model):
    """
    Representa um certificado obtido (aba "Certificados").

    O link do LinkedIn permite ao recrutador validar o certificado
    diretamente no perfil, garantindo autenticidade.
    """

    __tablename__ = "certificates"

    id: int = db.Column(db.Integer, primary_key=True)

    # Nome do certificado (ex: "UiPath RPA Developer Advanced")
    name: str = db.Column(db.String(200), nullable=False)

    # Quem emitiu (ex: "UiPath Academy", "Alura", "Coursera")
    issuer: str = db.Column(db.String(100), nullable=False, default="")

    # Área — para agrupar e filtrar (ex: "UiPath", "IA e Agentes", "Python")
    area: str = db.Column(db.String(80), nullable=False, default="Geral")

    # Data de conclusão
    issued_date: Optional[date] = db.Column(db.Date, nullable=True)

    # Data de validade (None = não expira)
    expiry_date: Optional[date] = db.Column(db.Date, nullable=True)

    # URL do certificado no LinkedIn para validação pelo recrutador
    linkedin_url: str = db.Column(db.String(500), nullable=True)

    # URL alternativa (Credly, site da certificadora, PDF, etc.)
    credential_url: str = db.Column(db.String(500), nullable=True)

    # Código/ID do certificado emitido pela plataforma
    credential_id: str = db.Column(db.String(200), nullable=True)

    # True = aparece em destaque no topo do grid
    featured: bool = db.Column(db.Boolean, nullable=False, default=False)
