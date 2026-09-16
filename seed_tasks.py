# =============================================================================
# seed_tasks.py — SCRIPT DE CARGA INICIAL DE TAREFAS E PROJETOS
# =============================================================================
# Execute este arquivo UMA VEZ para inserir todas as tarefas do backlog:
#   python seed_tasks.py
#
# O script apaga apenas as tarefas e projetos existentes e insere os novos.
# Execute com o servidor Flask PARADO para evitar conflitos.
# =============================================================================

import datetime
from app import create_app
from app import db
from app.models import Task, Project

app = create_app()

with app.app_context():

    # -------------------------------------------------------------------------
    # Apaga tarefas e projetos existentes para começar limpo
    # -------------------------------------------------------------------------
    Task.query.delete()
    Project.query.delete()
    db.session.commit()
    print("Tarefas e projetos anteriores removidos.")

    # -------------------------------------------------------------------------
    # Tarefas priorizadas (com prazo até o fim do ano)
    # Cada item: (título, área, prioridade, status, horas, notas, due[YYYY-MM-DD])
    # -------------------------------------------------------------------------
    tarefas = [
        (
            "UiPath Advanced — módulos críticos (Queues/Triggers, Orchestrator, Integration Service, DU + Action Center)",
            "UiPath", "Alta", "Em andamento", 12,
            "DoD: aplicar cada módulo em um mini-flow do AI Email Processor.",
            "2026-10-05",
        ),
        (
            "Python para Automação — requests/autenticação, JSON, Excel, e-mail",
            "Python", "Alta", "Não iniciado", 8,
            "DoD: script que lê e-mails, chama OpenAI e retorna categoria+confiança.",
            "2026-10-12",
        ),
        (
            "AI Email Processor v1 — fechar escopo (categorias, limiar, 'Ambíguo', exceções)",
            "IA e Agentes", "Alta", "Não iniciado", 2,
            "Definir 5–7 categorias, limiar de confiança e rotas de exceção.",
            "2026-09-20",
        ),
        (
            "AI Email Processor v1 — FastAPI /classify {categoria, confianca, motivos}",
            "Python", "Alta", "Não iniciado", 6,
            "Testes básicos + logs estruturados.",
            "2026-09-27",
        ),
        (
            "AI Email Processor v1 — UiPath: ler e-mails → HTTP /classify → Orchestrator Queue",
            "UiPath", "Alta", "Não iniciado", 8,
            "Logar confiança e id da mensagem.",
            "2026-10-07",
        ),
        (
            "AI Email Processor v1 — fallback no Action Center (baixa confiança)",
            "UiPath", "Média", "Não iniciado", 6,
            "Reclassificar e reenfileirar após validação humana.",
            "2026-10-14",
        ),
        (
            "Portfolio Planner v1 — seção 'Cases' com AI Email Processor (problema, arquitetura, KPIs, vídeo)",
            "Marca profissional", "Média", "Não iniciado", 4,
            "Vídeo 30–60s e diagrama simples.",
            "2026-10-21",
        ),
        (
            "LinkedIn — atualizar headline e resumo (UiPath + IA aplicada) e incluir KPIs do case",
            "Marca profissional", "Média", "Não iniciado", 2,
            "Publicar 1 post do case.",
            "2026-10-22",
        ),
        (
            "OpenAI API — /extract (texto→JSON) e /summarize; integrar no UiPath quando útil",
            "IA e Agentes", "Baixa", "Não iniciado", 6,
            "Endpoints prontos e testados.",
            "2026-11-07",
        ),
        (
            "Document Intelligence POC — DU campos de fatura + Action Center + métricas",
            "UiPath", "Baixa", "Não iniciado", 10,
            "Métricas: acurácia e AHT.",
            "2026-11-15",
        ),
        (
            "Regra de foco (anti-ansiedade): WIP máx. 2; sem novos cursos até 1º case; agenda 6h UiPath/3h Python/1h IA",
            "Marca profissional", "Alta", "Não iniciado", 1,
            "Bloquear agenda e revisar semanalmente.",
            "2026-09-16",
        ),
    ]

    for titulo, area, prioridade, status, horas, notas, due_str in tarefas:
        due = None
        try:
            due = datetime.date.fromisoformat(due_str) if due_str else None
        except Exception:
            due = None
        db.session.add(
            Task(
                title=titulo,
                area=area,
                priority=prioridade,
                status=status,
                due=due,
                hours=horas,
                notes=notas,
                completed=False,
            )
        )

    # -------------------------------------------------------------------------
    # Projetos
    # -------------------------------------------------------------------------
    projetos = [
        Project(
            name="Intelligent Automation Portfolio Planner",
            description="Aplicação de portfólio profissional para exibir cases (UiPath + IA), roadmap e competências.",
            stack="Python, Flask, SQLAlchemy, SQLite",
            progress=40,
            status="Em desenvolvimento",
            highlight="P0 · Portfólio",
        ),
        Project(
            name="AI Email Processor",
            description="Classifica e-mails com OpenAI via FastAPI e integra com UiPath Orchestrator (Queues/Action Center).",
            stack="Python, FastAPI, OpenAI API, UiPath Orchestrator",
            progress=10,
            status="Em desenvolvimento",
            highlight="P1 · Alta Prioridade",
        ),
        Project(
            name="Document Intelligence",
            description="POC de extração de campos de fatura com UiPath Document Understanding e validação no Action Center.",
            stack="UiPath DU, Action Center",
            progress=0,
            status="Backlog",
            highlight="P2 · Prova de Valor",
        ),
    ]

    for p in projetos:
        db.session.add(p)

    db.session.commit()
    print(f"OK {len(tarefas)} tarefas inseridas com sucesso.")
    print(f"OK {len(projetos)} projetos inseridos com sucesso.")
    print()
    print("Resumo por prioridade:")
    altas = sum(1 for _,_,p,_,_,_,_ in tarefas if p == "Alta")
    medias = sum(1 for _,_,p,_,_,_,_ in tarefas if p == "Média")
    baixas = sum(1 for _,_,p,_,_,_,_ in tarefas if p == "Baixa")
    print(f"  Alta: {altas} tarefas")
    print(f"  Média: {medias} tarefas")
    print(f"  Baixa: {baixas} tarefas")
