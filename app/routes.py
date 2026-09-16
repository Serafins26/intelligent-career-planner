# =============================================================================
# app/routes.py — ROTAS E LÓGICA DAS PÁGINAS
# =============================================================================
# Este é o arquivo mais importante depois dos modelos. Ele define:
#
#   1. As PÁGINAS que existem no sistema (Sobre mim, Plano, Projetos, Competências)
#   2. As AÇÕES que o usuário pode executar (adicionar, editar, excluir, concluir)
#   3. Utilitários de BACKUP e RESTAURAÇÃO dos dados
#
# Conceito de ROTA:
#   Quando você digita "http://localhost:5000/planner" no browser,
#   o Flask procura uma função marcada com @bp.route("/planner") e a executa.
#   Essa função busca dados no banco, monta a resposta e devolve o HTML da página.
#
# Conceito de BLUEPRINT:
#   Um Blueprint é uma forma de organizar rotas em grupos.
#   Aqui temos um único Blueprint chamado "main" que agrupa todas as rotas do app.
#   Em projetos maiores, teríamos vários Blueprints (ex: auth, admin, api).
#
# CRUD = Create, Read, Update, Delete (Criar, Ler, Atualizar, Excluir)
#   As 4 operações básicas que fazemos com dados no banco.
# =============================================================================

from __future__ import annotations

from datetime import datetime   # Para converter strings de data (ex: "2026-09-18") em objetos Date
from datetime import date, timedelta  # Para cálculos de semana no Weekly Plan
from typing import Any          # Tipo genérico usado na anotação de retorno de funções

from flask import (
    Blueprint,       # Para criar o grupo de rotas
    render_template, # Para renderizar (montar) os templates HTML com dados do Python
    redirect,        # Para redirecionar o usuário para outra página
    url_for,         # Para gerar URLs a partir do nome das funções (mais seguro que escrever à mão)
    request,         # Para acessar dados enviados pelo browser (formulários, parâmetros de URL)
    send_file,       # Para enviar um arquivo para download
    flash,           # Para exibir mensagens temporárias (ex: "Salvo com sucesso!")
    session,         # Para guardar dados temporários do usuário (ex: se está em modo recrutador)
    current_app,     # Para acessar configurações e paths da app
)
import csv
import io
import json
from pathlib import Path

from . import db                              # O banco de dados
from .config import Config                    # Configurações (para foto de perfil)
from .models import Task, Project, SkillCategory, Certificate  # Os modelos (tabelas)

# Cria o Blueprint chamado "main" — todas as rotas aqui pertencerão a ele
bp = Blueprint("main", __name__)


# -----------------------------------------------------------------------------
# FTE de referência (fallback) para projetos corporativos conhecidos
# Usado para backfill quando fte_hours está ausente/zero no banco.
# Fonte: lista de projetos corporativos previamente inserida (seeds).
# -----------------------------------------------------------------------------
KNOWN_FTE_BY_NAME: dict[str, float] = {
    # Demo data — replace with your own corporate project FTE values
    "Invoice Processing Automation": 24.5,
    "HR Onboarding Bot": 18.0,
    "Report Generation Pipeline": 12.0,
    "Vendor Management App": 8.5,
}


@bp.before_request
def _guard_write_actions():
    """Bloqueia ações de escrita (POST) para quem não é admin."""
    if request.method == "POST":
        allowed = {"/admin/login", "/admin/logout", "/recruiter/toggle"}
        if request.path not in allowed and not session.get("is_admin", False):
            flash("Acesso restrito. Faça login como admin.", "error")
            return redirect(request.referrer or url_for("main.about"))


# =============================================================================
# FUNÇÕES AUXILIARES (Helpers)
# Funções internas usadas por várias rotas — não são páginas, apenas utilidades.
# O underscore (_) no início do nome indica que são "privadas" (uso interno).
# =============================================================================

def _compute_stats() -> dict[str, Any]:
    """
    Calcula as estatísticas gerais exibidas nos cards do topo de cada página.

    Retorna um dicionário com:
      - total:          quantidade total de tarefas no banco
      - done:           quantas estão concluídas
      - hours:          soma de todas as horas planejadas
      - doneHours:      soma das horas das tarefas concluídas
      - progress:       percentual de conclusão (0 a 100)
      - activeProjects: quantidade de projetos que ainda não estão concluídos

    Por que usar uma função separada?
      Porque todas as páginas (Sobre, Plano, Projetos, Competências) precisam
      exibir esses números no topo. Em vez de repetir o código em cada rota,
      centralizamos aqui e chamamos uma vez por página.
    """
    # Conta o total de tarefas na tabela
    total = Task.query.count()

    # Conta apenas as concluídas — aceita tanto a flag "completed" quanto o status "Concluído"
    # O | significa "OU" (basta uma das condições ser verdadeira)
    done = Task.query.filter(
        (Task.completed.is_(True)) | (Task.status == "Concluído")
    ).count()

    # Soma todas as horas planejadas (coalesce substitui NULL por 0 se a tabela estiver vazia)
    hours = db.session.query(
        db.func.coalesce(db.func.sum(Task.hours), 0)
    ).scalar() or 0

    # Soma as horas apenas das tarefas concluídas
    done_hours = (
        db.session.query(db.func.coalesce(db.func.sum(Task.hours), 0))
        .filter((Task.completed.is_(True)) | (Task.status == "Concluído"))
        .scalar()
        or 0
    )

    # Calcula o percentual: (concluídas / total) × 100
    # Evita divisão por zero com "if total else 0"
    progress = int(round((done / total) * 100)) if total else 0

    # Projetos ativos = todos que NÃO estão concluídos
    # Considera concluído se status == "Concluído" OU progress >= 100
    active_projects = (
        Project.query
        .filter((Project.status != "Concluído") & (Project.progress < 100))
        .count()
    )

    # Projetos concluídos (status Concluído ou progresso >= 100)
    completed_projects = (
        Project.query
        .filter((Project.status == "Concluído") | (Project.progress >= 100))
        .count()
    )

    # Projetos corporativos (independente de status)
    corporate_projects = (
        Project.query
        .filter(Project.project_type == "Corporativo")
        .count()
    )

    # Horas FTE economizadas — soma com fallback: usa fte_hours do banco,
    # e quando ausente/zero tenta KNOWN_FTE_BY_NAME para evitar subcontagem.
    total_fte = 0.0
    corp = (
        Project.query
        .filter(
            (Project.project_type == "Corporativo") &
            ((Project.status == "Concluído") | (Project.progress >= 100))
        )
        .all()
    )
    for p in corp:
        val = (p.fte_hours or 0.0)
        if not val or val == 0.0:
            val = KNOWN_FTE_BY_NAME.get(p.name, 0.0)
        total_fte += float(val or 0.0)
    fte_saved = round(total_fte, 2)

    # Entregas: tarefas concluídas com evidência registrada
    deliveries = (
        Task.query
        .filter(
            ((Task.completed.is_(True)) | (Task.status == "Concluído"))
            & (Task.evidence.isnot(None))
            & (Task.evidence != "")
        )
        .count()
    )

    # Projetos sustentados em produção
    sustained_projects = (
        Project.query
        .filter(Project.sustained.is_(True))
        .count()
    )

    # Certificados emitidos
    cert_count = Certificate.query.count()

    # Retorna tudo em um dicionário — as chaves são usadas nos templates HTML
    return {
        "total": total,
        "done": done,
        "hours": hours,
        "doneHours": done_hours,
        "progress": progress,
        "activeProjects": active_projects,
        "completedProjects": completed_projects,
        "corporateProjects": corporate_projects,
        "sustainedProjects": sustained_projects,
        "fteSaved": fte_saved,
        "deliveries": deliveries,
        "certCount": cert_count,
    }


def _is_admin() -> bool:
    """Verifica se o usuário autenticou como admin nesta sessão."""
    return bool(session.get("is_admin", False))


def _is_recruiter() -> bool:
    """
    Verifica se o usuário está em 'Modo Visualização'.
    Visitantes (não-admin) estão SEMPRE em modo visualização.
    Admin pode alternar entre visualização e edição.
    """
    if not _is_admin():
        return True  # visitante = sempre modo visualização
    return bool(session.get("recruiter_mode", False))


# =============================================================================
# ROTAS DE CONTROLE
# =============================================================================

@bp.route("/admin/login")
def admin_login():
    """Autentica como admin via query param ?key=<ADMIN_KEY>."""
    import os
    admin_key = os.environ.get("ADMIN_KEY", "andre2026")
    if request.args.get("key") == admin_key:
        session["is_admin"] = True
        session["recruiter_mode"] = False
        flash("Modo admin ativado.", "success")
    else:
        flash("Chave inválida.", "error")
    return redirect(request.referrer or url_for("main.about"))


@bp.route("/admin/logout", methods=["POST"])
def admin_logout():
    """Desautentica o admin."""
    session.pop("is_admin", None)
    session.pop("recruiter_mode", None)
    flash("Saiu do modo admin.", "success")
    return redirect(request.referrer or url_for("main.about"))


@bp.route("/recruiter/toggle", methods=["POST"])
def toggle_recruiter():
    """Alterna entre modo edição e visualização (somente admin)."""
    if not _is_admin():
        return redirect(request.referrer or url_for("main.about"))
    session["recruiter_mode"] = not _is_recruiter()
    return redirect(request.referrer or url_for("main.about"))


@bp.route("/")
def home():
    """
    Rota raiz (/) — redireciona automaticamente para a página 'Sobre mim'.
    Quem acessar http://localhost:5000 vai parar em /about.
    """
    return redirect(url_for("main.about"))


# =============================================================================
# PÁGINAS PRINCIPAIS
# =============================================================================

@bp.route("/about")
def about():
    """
    Página 'Sobre mim' — a página inicial do sistema.

    Busca as estatísticas e passa para o template about.html.
    O template usa essas informações para montar o hero, os cards de stats
    e o conteúdo de apresentação.
    """
    stats = _compute_stats()
    # Define URL da foto de perfil: prioriza Config.PROFILE_PHOTO_URL; senão, usa arquivo local se existir
    from pathlib import Path
    profile_photo_url = None
    if getattr(Config, "PROFILE_PHOTO_URL", ""):
        profile_photo_url = Config.PROFILE_PHOTO_URL
    else:
        static_dir = Path(current_app.static_folder)
        local_photo = static_dir / "img" / "profile.jpg"
        local_photo_png = static_dir / "img" / "profile.png"
        if local_photo.exists():
            profile_photo_url = url_for("static", filename="img/profile.jpg")
        elif local_photo_png.exists():
            profile_photo_url = url_for("static", filename="img/profile.png")
    return render_template("about.html", stats=stats, recruiter=_is_recruiter(), profile_photo_url=profile_photo_url)


@bp.route("/planner")
def planner():
    """
    Página 'Plano' — lista de tarefas com filtros.
    Visível apenas para admin em modo edição.
    Visitantes e modo visualização são redirecionados para Projetos.
    """
    if _is_recruiter():
        return redirect(url_for("main.projects"))

    stats = _compute_stats()

    # Lê os filtros da URL (request.args = parâmetros depois do "?" na URL)
    area   = request.args.get("area", "Todas")
    status = request.args.get("status", "Todos")
    q      = (request.args.get("q") or "").strip().lower()  # Texto de busca, em minúsculas

    # Começa com todas as tarefas e vai refinando conforme os filtros aplicados
    query = Task.query

    if area and area != "Todas":
        query = query.filter(Task.area == area)      # Filtra pela área selecionada

    if status and status != "Todos":
        query = query.filter(Task.status == status)  # Filtra pelo status selecionado

    if q:
        like = f"%{q}%"  # O % é um coringa: "%python%" encontra "aprender python básico"
        query = query.filter(
            (Task.title.ilike(like)) | (Task.area.ilike(like))  # Busca no título OU na área
        )

    # Ordena: tarefas sem prazo vão para o final; as com prazo aparecem pela data mais próxima
    # Ordena por prioridade (Alta → Média → Baixa) e depois por prazo
    from sqlalchemy import case
    priority_order = case(
        (Task.priority == "Alta",  0),
        (Task.priority == "Média", 1),
        (Task.priority == "Baixa", 2),
        else_=3,
    )
    tasks = query.order_by(priority_order, Task.due.is_(None), Task.due.asc()).all()

    return render_template(
        "planner.html",
        tasks=tasks,       # Lista de tarefas filtradas
        stats=stats,       # KPIs para o topo
        q=q,               # Texto de busca (para manter preenchido no input)
        area=area,         # Área selecionada (para manter o select no estado certo)
        status=status,     # Status selecionado
        recruiter=_is_recruiter()
    )


# =============================================================================
# WEEKLY PLAN — visão semanal
# - Admin (não recruiter): visão detalhada por dia, com notas e ações
# - Recruiter/visitante: visão macro (resumo por área e próximos prazos), sem detalhes
# =============================================================================

@bp.route("/weekly")
def weekly_plan():
    """
    Página de plano semanal.
    Visível apenas para admin em modo edição.
    """
    if _is_recruiter():
        return redirect(url_for("main.projects"))

    stats = _compute_stats()
    recruiter = False

    # Semana atual: segunda (start) até domingo (end)
    today = date.today()
    start = today - timedelta(days=today.weekday())   # Monday
    end = start + timedelta(days=6)                   # Sunday

    # Busca tarefas com due definido e dentro do intervalo
    week_tasks = (
        Task.query
        .filter(Task.due.isnot(None))
        .filter(Task.due >= start)
        .filter(Task.due <= end)
        .order_by(Task.due.asc(), Task.priority.asc())
        .all()
    )

    # Agrupa por dia (dict[date] -> list[Task])
    by_day: dict[date, list[Task]] = {}
    for t in week_tasks:
        by_day.setdefault(t.due, []).append(t)

    # Resumo macro por área (contagem e próximos títulos)
    macro: dict[str, dict[str, any]] = {}
    for t in week_tasks:
        area = t.area or "Outros"
        m = macro.setdefault(area, {"count": 0, "items": []})
        m["count"] += 1
        # Lista curta apenas com título e data
        if len(m["items"]) < 3:
            m["items"].append({"title": t.title, "due": t.due})

    return render_template(
        "weekly.html",
        stats=stats,
        recruiter=recruiter,
        start=start,
        end=end,
        by_day=by_day,
        macro=macro,
    )

@bp.post("/tasks/<int:task_id>/log")
def quick_log(task_id: int):
    """
    Adiciona um micro-log rápido às notas da tarefa (append).
    Usado no Weekly para registrar o que foi feito/aprendido na sessão.
    """
    task = Task.query.get_or_404(task_id)
    log_text = request.form.get("log", "").strip()
    if log_text:
        timestamp = date.today().strftime("%d/%m")
        entry = f"[{timestamp}] {log_text}"
        if task.notes:
            task.notes = f"{task.notes} | {entry}"
        else:
            task.notes = entry
        db.session.commit()
        flash("Log salvo.", "success")
    referrer = request.referrer or url_for("main.weekly_plan")
    return redirect(referrer)


@bp.post("/tasks/<int:task_id>/send-to-week")
def send_to_week(task_id: int):
    """
    Move o prazo de uma tarefa para um dia específico da semana atual.
    Recebe o parâmetro 'day' (0=Seg, 1=Ter, ..., 5=Sáb, 6=Dom).
    Se não informado, usa segunda-feira.
    """
    task = Task.query.get_or_404(task_id)
    today = date.today()
    monday = today - timedelta(days=today.weekday())
    day_offset = int(request.form.get("day", 0))
    target = monday + timedelta(days=day_offset)

    day_names = {0: "Seg", 1: "Ter", 2: "Qua", 3: "Qui", 4: "Sex", 5: "Sáb", 6: "Dom"}
    day_name = day_names.get(day_offset, "")

    task.due = target
    db.session.commit()
    flash(f"'{task.title}' agendada para {day_name} ({target.strftime('%d/%m')}).", "success")
    referrer = request.referrer or url_for("main.planner")
    return redirect(referrer)


@bp.post("/seed-milestones")
def seed_milestones():
    """
    Cria marcos estratégicos no Planner (DoD AI Email Processor, Marco Candidatura, Meta UiARD).
    Só cria se não existirem pelo título.
    """
    milestones = [
        {
            "title": "🎯 DoD — AI Email Processor v1",
            "area": "Projeto",
            "priority": "Alta",
            "hours": 20,
            "due": date(2026, 11, 30),
            "notes": "DoD: FastAPI /classify (categoria+confiança) | UiPath HTTP→Queue | Limiar confiança + fallback 'ambíguo' | Logs/erros/retry | Vídeo 60s demo | README com arquitetura e KPIs",
        },
        {
            "title": "🚀 MARCO — Iniciar candidaturas (Onda 0)",
            "area": "Marca profissional",
            "priority": "Alta",
            "hours": 2,
            "due": date(2026, 10, 7),
            "notes": "Gatilho: UiPath HTTP→Queue funcionando | Ações: 5 candidaturas/semana + 5 contatos LinkedIn + CV atualizado com case + headline Intelligent Automation",
        },
        {
            "title": "📜 META — Certificação UiPath Advanced (UiARD)",
            "area": "UiPath",
            "priority": "Alta",
            "hours": 94,
            "due": date(2026, 12, 15),
            "notes": "Finalizar Learning Plan (94h) → Agendar exame UiARD → Certificado no LinkedIn e Portfolio",
        },
    ]

    created = 0
    for m in milestones:
        exists = Task.query.filter_by(title=m["title"]).first()
        if not exists:
            task = Task(
                title=m["title"],
                area=m["area"],
                priority=m["priority"],
                status="Não iniciado",
                due=m["due"],
                hours=m["hours"],
                notes=m["notes"],
            )
            db.session.add(task)
            created += 1

    if created:
        db.session.commit()
        flash(f"{created} marco(s) estratégico(s) criado(s).", "success")
    else:
        flash("Marcos já existem no Plano.", "info")
    return redirect(url_for("main.planner"))


# =============================================================================
# CRUD DE TAREFAS
# =============================================================================

@bp.post("/tasks/add")
def add_task():
    """
    Cria uma nova tarefa a partir dos dados do formulário.

    @bp.post = só aceita requisições POST (formulários que enviam dados).
    Lê cada campo do formulário, valida o mínimo (título obrigatório),
    cria o objeto Task, salva no banco e redireciona para o Plano.
    """
    title = request.form.get("title", "").strip()
    if not title:
        # Se o título estiver vazio, mostra mensagem de erro e volta para o Plano
        flash("Título é obrigatório.", "error")
        return redirect(url_for("main.planner"))

    # Converte a data de string ("2026-09-18") para objeto date do Python
    due_raw = request.form.get("due") or None
    due = datetime.strptime(due_raw, "%Y-%m-%d").date() if due_raw else None

    # Cria o objeto Task com todos os campos do formulário
    task = Task(
        title=title,
        area=request.form.get("area", "IA e Agentes"),
        priority=request.form.get("priority", "Média"),
        status=request.form.get("status", "Não iniciado"),
        due=due,
        hours=int(request.form.get("hours", 1) or 1),
        evidence=(request.form.get("evidence") or "").strip(),
        notes=(request.form.get("notes") or "").strip(),
        completed=(request.form.get("status") == "Concluído"),  # Marca como concluída se status for "Concluído"
    )
    db.session.add(task)    # Adiciona à sessão (equivalente ao INSERT pendente)
    db.session.commit()     # Confirma e salva no arquivo .db
    return redirect(url_for("main.planner"))


@bp.post("/tasks/<int:task_id>/toggle")
def toggle_task(task_id: int):
    """
    Alterna o status de uma tarefa (Concluir / Desfazer).

    <int:task_id> na URL captura o número da tarefa.
    Ex: POST /tasks/3/toggle → alterna a tarefa com id=3.

    get_or_404 busca a tarefa pelo id. Se não encontrar, retorna erro 404.
    """
    task = Task.query.get_or_404(task_id)
    task.mark_toggle()   # Chama o método definido no modelo (inverte o status)
    db.session.commit()  # Salva a mudança no banco
    return redirect(url_for("main.planner"))


@bp.post("/tasks/<int:task_id>/delete")
def delete_task(task_id: int):
    """
    Exclui uma tarefa permanentemente do banco de dados.
    """
    task = Task.query.get_or_404(task_id)
    db.session.delete(task)  # Marca para exclusão
    db.session.commit()      # Confirma e remove do banco
    return redirect(url_for("main.planner"))


@bp.get("/tasks/<int:task_id>/edit")
def edit_task(task_id: int):
    """
    Exibe o formulário de edição de uma tarefa (GET = mostrar o formulário).

    @bp.get = só aceita requisições GET (quando você abre uma URL no browser).
    Busca a tarefa pelo id e renderiza o template edit_task.html com os dados atuais.
    """
    task = Task.query.get_or_404(task_id)
    stats = _compute_stats()
    return render_template("edit_task.html", task=task, stats=stats)


@bp.post("/tasks/<int:task_id>/edit")
def save_task(task_id: int):
    """
    Salva as alterações feitas no formulário de edição (POST = receber os dados).

    Mesma URL que edit_task, mas método POST — Flask roteia para funções diferentes
    dependendo do método HTTP (GET para mostrar, POST para salvar).
    """
    task = Task.query.get_or_404(task_id)

    # Atualiza cada campo com o valor do formulário, mantendo o original se não enviado
    task.title    = request.form.get("title", task.title).strip()
    task.area     = request.form.get("area", task.area)
    task.priority = request.form.get("priority", task.priority)
    task.status   = request.form.get("status", task.status)

    due_raw  = request.form.get("due") or None
    task.due = datetime.strptime(due_raw, "%Y-%m-%d").date() if due_raw else None

    task.hours     = int(request.form.get("hours", task.hours) or task.hours)
    task.evidence  = (request.form.get("evidence") or "").strip()
    task.notes     = (request.form.get("notes") or "").strip()
    task.completed = (task.status == "Concluído")  # Sincroniza a flag com o status

    db.session.commit()  # Salva tudo no banco
    return redirect(url_for("main.planner"))


# =============================================================================
# PÁGINA DE PROJETOS
# =============================================================================

@bp.route("/projects")
def projects():
    """
    Página 'Projetos' — lista todos os projetos do portfólio.

    Aceita filtros via query string:
      /projects?status=Concluído&tipo=Corporativo&tech=UiPath&q=sap
    """
    stats = _compute_stats()

    # Lê filtros da URL
    f_status = request.args.get("status", "Todos")
    f_tipo = request.args.get("tipo", "Todos")
    f_tech = request.args.get("tech", "Todas")
    f_q = (request.args.get("q") or "").strip().lower()

    query = Project.query

    if f_status and f_status != "Todos":
        query = query.filter(Project.status == f_status)

    if f_tipo and f_tipo != "Todos":
        query = query.filter(Project.project_type == f_tipo)

    if f_tech and f_tech != "Todas":
        like = f"%{f_tech}%"
        query = query.filter(Project.stack.ilike(like))

    if f_q:
        like = f"%{f_q}%"
        query = query.filter(
            (Project.name.ilike(like)) | (Project.description.ilike(like)) | (Project.stack.ilike(like))
        )

    projects_list = query.order_by(
        Project.status.desc(),
        Project.progress.desc()
    ).all()

    # Coleta todas as tecnologias únicas para o filtro
    all_projects = Project.query.all()
    all_techs = sorted({
        tech.strip()
        for p in all_projects
        if p.stack
        for tech in p.stack.split(",")
        if tech.strip()
    })

    return render_template(
        "projects.html",
        stats=stats,
        projects=projects_list,
        recruiter=_is_recruiter(),
        all_techs=all_techs,
        f_status=f_status,
        f_tipo=f_tipo,
        f_tech=f_tech,
        f_q=f_q,
    )


# =============================================================================
# PÁGINA DE COMPETÊNCIAS + CRUD
# =============================================================================

@bp.route("/skills")
def skills():
    """
    Página 'Competências' — lista as categorias de competências técnicas.

    Na primeira vez que é acessada (banco vazio), insere as 6 categorias padrão
    automaticamente (seed). Isso garante que a página nunca apareça vazia.
    """
    stats = _compute_stats()

    # Se ainda não há nenhuma categoria, cria as 6 padrão
    if SkillCategory.query.count() == 0:
        defaults = [
            ("🤖", "RPA e Arquitetura",    "REFramework avançado, Orchestrator e Queues, SAP Automation, Logs e retries, Tratamento de exceções", 0),
            ("✨", "IA e Agentes",          "Copilot Studio, LLMs e GenAI, AI Agents, MCP, Bases de conhecimento",                                1),
            ("🔗", "Integrações",           "REST APIs, OAuth 2.0 e JWT, Webhooks, JSON e OpenAPI",                                               2),
            ("⚙️", "Low-code Automation",  "Power Automate, Workflows orientados a eventos, Tratamento de erros, Integrações com IA",            3),
            ("💻", "Desenvolvimento",       "Python para automação, SQL, Git e GitHub, Documentação técnica",                                      4),
            ("🏆", "Marca Profissional",    "Projetos demonstráveis, Posts técnicos, Evidências no GitHub, Networking qualificado",                5),
        ]
        for icon, title, items, order in defaults:
            db.session.add(SkillCategory(icon=icon, title=title, items=items, order=order))
        db.session.commit()

    # Busca todas as categorias ordenadas pelo campo "order" (menor número = aparece primeiro)
    categories = SkillCategory.query.order_by(
        SkillCategory.order.asc(),
        SkillCategory.id.asc()
    ).all()

    return render_template("skills.html", stats=stats, categories=categories, recruiter=_is_recruiter())


@bp.post("/skills/add")
def add_skill():
    """Cria uma nova categoria de competências."""
    title = request.form.get("title", "").strip()
    if not title:
        flash("Título é obrigatório.", "error")
        return redirect(url_for("main.skills"))

    cat = SkillCategory(
        icon=request.form.get("icon", "⚡").strip() or "⚡",
        title=title,
        items=request.form.get("items", "").strip(),
        order=SkillCategory.query.count(),  # Coloca no final da lista
    )
    db.session.add(cat)
    db.session.commit()
    return redirect(url_for("main.skills"))


@bp.get("/skills/<int:cat_id>/edit")
def edit_skill(cat_id: int):
    """Exibe o formulário de edição de uma categoria de competências."""
    cat = SkillCategory.query.get_or_404(cat_id)
    stats = _compute_stats()
    return render_template("edit_skill.html", cat=cat, stats=stats)


# =============================================================================
# CURRÍCULO (RESUME)
# =============================================================================

@bp.get("/resume")
def resume():
    """Página de currículo (HTML) baseada nos dados do portfólio."""
    stats = _compute_stats()

    # Coleta categorias de competências
    categories = SkillCategory.query.order_by(
        SkillCategory.order.asc(), SkillCategory.id.asc()
    ).all()

    # Seleciona projetos pessoais (prioriza concluídos, depois progresso)
    personal_projects = (
        Project.query.filter_by(project_type="Pessoal")
        .order_by(Project.status.desc(), Project.progress.desc(), Project.id.desc())
        .limit(6)
        .all()
    )

    # Certificados em destaque
    from .models import Certificate
    featured_certs = Certificate.query.filter_by(featured=True).order_by(Certificate.issued_date.desc()).limit(6).all()

    # Dados extras opcionais (experiência, educação) via data/resume.json
    resume_extra: dict[str, object] = {}
    try:
        data_path = Path(current_app.root_path).parent / "data" / "resume.json"
        if data_path.exists():
            with data_path.open("r", encoding="utf-8") as f:
                resume_extra = json.load(f)
    except Exception:
        resume_extra = {}

    return render_template(
        "resume.html",
        stats=stats,
        categories=categories,
        projects=personal_projects,
        featured_certs=featured_certs,
        resume_extra=resume_extra,
        recruiter=True,  # resume é somente visualização
    )


@bp.get("/resume.pdf")
def resume_pdf():
    """Gera PDF do currículo a partir do template HTML (best-effort)."""
    # Reexecuta a coleta de dados como em /resume
    stats = _compute_stats()
    categories = SkillCategory.query.order_by(
        SkillCategory.order.asc(), SkillCategory.id.asc()
    ).all()
    personal_projects = (
        Project.query.filter_by(project_type="Pessoal")
        .order_by(Project.status.desc(), Project.progress.desc(), Project.id.desc())
        .limit(6)
        .all()
    )
    from .models import Certificate
    featured_certs = (
        Certificate.query.filter_by(featured=True)
        .order_by(Certificate.issued_date.desc())
        .limit(6)
        .all()
    )
    resume_extra: dict[str, object] = {}
    try:
        data_path = Path(current_app.root_path).parent / "data" / "resume.json"
        if data_path.exists():
            with data_path.open("r", encoding="utf-8") as f:
                resume_extra = json.load(f)
    except Exception:
        resume_extra = {}

    html = render_template(
        "resume.html",
        stats=stats,
        categories=categories,
        projects=personal_projects,
        featured_certs=featured_certs,
        resume_extra=resume_extra,
        recruiter=True,
        pdf_mode=True,
    )

    try:
        from weasyprint import HTML, CSS  # type: ignore
        import traceback as _tb

        # CSS path — try static_folder first, then fallback
        css_path = Path(current_app.static_folder) / "css" / "styles.css"
        if not css_path.exists():
            css_path = Path(current_app.root_path).parent / "static" / "css" / "styles.css"

        stylesheets = []
        if css_path.exists():
            stylesheets.append(CSS(filename=str(css_path)))

        pdf_bytes = HTML(
            string=html,
            base_url=request.url_root,
        ).write_pdf(stylesheets=stylesheets)

        from flask import make_response
        resp = make_response(pdf_bytes)
        resp.headers["Content-Type"] = "application/pdf"
        resp.headers["Content-Disposition"] = "inline; filename=Resume.pdf"
        return resp
    except Exception as exc:
        current_app.logger.error("resume_pdf failed: %s\n%s", exc, _tb.format_exc())
        flash("Geração de PDF indisponível no servidor. Use Ctrl+P para salvar em PDF.", "error")
        return redirect(url_for("main.resume"))


# =============================================================================
# DETALHE DO PROJETO (inclui evidências)
# =============================================================================

@bp.get("/projects/<int:project_id>")
def project_detail(project_id: int):
    """Página de detalhes do projeto com seção de evidências."""
    project = Project.query.get_or_404(project_id)
    stats = _compute_stats()

    # Evidências múltiplas separadas por vírgula ou ponto e vírgula
    evidences: list[str] = []
    if project.evidence:
        raw = project.evidence.replace(";", ",")
        evidences = [e.strip() for e in raw.split(",") if e.strip()]

    return render_template(
        "project_detail.html",
        project=project,
        evidences=evidences,
        stats=stats,
        recruiter=_is_recruiter(),
    )


@bp.post("/skills/<int:cat_id>/edit")
def save_skill(cat_id: int):
    """Salva as alterações de uma categoria de competências."""
    cat = SkillCategory.query.get_or_404(cat_id)
    cat.icon  = request.form.get("icon", cat.icon).strip() or cat.icon
    cat.title = request.form.get("title", cat.title).strip()
    cat.items = request.form.get("items", "").strip()
    db.session.commit()
    return redirect(url_for("main.skills"))


@bp.post("/skills/<int:cat_id>/delete")
def delete_skill(cat_id: int):
    """Exclui uma categoria de competências."""
    cat = SkillCategory.query.get_or_404(cat_id)
    db.session.delete(cat)
    db.session.commit()
    return redirect(url_for("main.skills"))


# =============================================================================
# CERTIFICADOS — CRUD completo
# =============================================================================

@bp.route("/certificates")
def certificates():
    """Página de certificados. Exibe todos agrupados por área."""
    stats = _compute_stats()
    # Destacados primeiro, depois por data mais recente
    certs = Certificate.query.order_by(
        Certificate.featured.desc(),
        Certificate.issued_date.desc()
    ).all()
    # Áreas únicas para o filtro
    areas = sorted({c.area for c in certs}) if certs else []
    return render_template("certificates.html", stats=stats, certs=certs, areas=areas, recruiter=_is_recruiter())


@bp.post("/certificates/add")
def add_certificate():
    """Adiciona um novo certificado."""
    name = request.form.get("name", "").strip()
    if not name:
        flash("Nome do certificado é obrigatório.", "error")
        return redirect(url_for("main.certificates"))

    issued_raw  = request.form.get("issued_date", "").strip()
    expiry_raw  = request.form.get("expiry_date", "").strip()

    import datetime as _dt
    def _parse_date(s):
        if not s:
            return None
        for fmt in ("%Y-%m-%d", "%Y-%m"):
            try:
                return _dt.datetime.strptime(s, fmt).date()
            except ValueError:
                continue
        return None

    cert = Certificate(
        name=name,
        issuer=(request.form.get("issuer") or "").strip(),
        area=(request.form.get("area") or "Geral").strip(),
        issued_date=_parse_date(issued_raw),
        expiry_date=_parse_date(expiry_raw),
        linkedin_url=(request.form.get("linkedin_url") or "").strip(),
        credential_url=(request.form.get("credential_url") or "").strip(),
        credential_id=(request.form.get("credential_id") or "").strip(),
        featured=bool(request.form.get("featured")),
    )
    db.session.add(cert)
    db.session.commit()
    flash("Certificado adicionado!", "success")
    return redirect(url_for("main.certificates"))


@bp.get("/certificates/<int:cert_id>/edit")
def edit_certificate(cert_id: int):
    """Formulário de edição de um certificado."""
    cert = Certificate.query.get_or_404(cert_id)
    stats = _compute_stats()
    return render_template("edit_certificate.html", cert=cert, stats=stats, recruiter=_is_recruiter())


@bp.post("/certificates/<int:cert_id>/edit")
def save_certificate(cert_id: int):
    """Salva as alterações de um certificado."""
    cert = Certificate.query.get_or_404(cert_id)

    import datetime as _dt
    def _parse_date(s):
        if not s:
            return None
        for fmt in ("%Y-%m-%d", "%Y-%m"):
            try:
                return _dt.datetime.strptime(s, fmt).date()
            except ValueError:
                continue
        return None

    cert.name           = request.form.get("name", cert.name).strip()
    cert.issuer         = (request.form.get("issuer") or "").strip()
    cert.area           = (request.form.get("area") or "Geral").strip()
    cert.issued_date    = _parse_date(request.form.get("issued_date", ""))
    cert.expiry_date    = _parse_date(request.form.get("expiry_date", ""))
    cert.linkedin_url   = (request.form.get("linkedin_url") or "").strip()
    cert.credential_url = (request.form.get("credential_url") or "").strip()
    cert.credential_id  = (request.form.get("credential_id") or "").strip()
    cert.featured       = bool(request.form.get("featured"))
    db.session.commit()
    flash("Certificado atualizado!", "success")
    return redirect(url_for("main.certificates"))


@bp.post("/certificates/<int:cert_id>/delete")
def delete_certificate(cert_id: int):
    """Exclui um certificado permanentemente."""
    cert = Certificate.query.get_or_404(cert_id)
    db.session.delete(cert)
    db.session.commit()
    return redirect(url_for("main.certificates"))


# =============================================================================
# CRUD DE PROJETOS
# =============================================================================

@bp.post("/projects/add")
def add_project():
    """Cria um novo projeto no portfólio."""
    name = request.form.get("name", "").strip()
    if not name:
        flash("Nome do projeto é obrigatório.", "error")
        return redirect(url_for("main.projects"))

    # Normaliza status x progresso
    _progress = int(request.form.get("progress", 0) or 0)
    _progress = max(0, min(_progress, 100))  # clamp 0..100
    _status = request.form.get("status", "Backlog")
    if _progress >= 100:
        _progress = 100
        _status = "Concluído"
    elif (_status or "").strip() == "Concluído" and _progress < 100:
        _progress = 100

    ptype_raw = (request.form.get("project_type", "Pessoal") or "").strip()
    ptype = "Corporativo" if ptype_raw.lower().startswith("corp") else "Pessoal"
    fte = float(request.form.get("fte_hours", 0) or 0) if ptype == "Corporativo" else None

    project = Project(
        name=name,
        description=(request.form.get("description") or "").strip(),
        stack=(request.form.get("stack") or "").strip(),
        progress=_progress,
        status=_status,
        repo=(request.form.get("repo") or "").strip(),
        demo=(request.form.get("demo") or "").strip(),
        evidence=(request.form.get("evidence") or "").strip(),
        highlight=(request.form.get("highlight") or "").strip(),
        project_type=ptype,
        fte_hours=fte,
        sustained=bool(request.form.get("sustained")),
    )
    db.session.add(project)
    db.session.commit()
    return redirect(url_for("main.projects"))


@bp.get("/projects/<int:project_id>/edit")
def edit_project(project_id: int):
    """Exibe o formulário de edição de um projeto."""
    project = Project.query.get_or_404(project_id)
    stats = _compute_stats()
    return render_template("edit_project.html", project=project, stats=stats)


@bp.post("/projects/<int:project_id>/edit")
def save_project(project_id: int):
    """Salva as alterações de um projeto."""
    project = Project.query.get_or_404(project_id)
    project.name        = request.form.get("name", project.name).strip()
    project.description = (request.form.get("description") or "").strip()
    project.stack       = (request.form.get("stack") or "").strip()
    # Normaliza progresso + status mantendo consistência
    _progress = int(request.form.get("progress", project.progress) or project.progress)
    _progress = max(0, min(_progress, 100))
    _status = request.form.get("status", project.status)
    if _progress >= 100:
        _progress = 100
        _status = "Concluído"
    elif (_status or "").strip() == "Concluído" and _progress < 100:
        _progress = 100

    project.progress    = _progress
    project.status      = _status
    project.repo        = (request.form.get("repo") or "").strip()
    project.demo        = (request.form.get("demo") or "").strip()
    project.evidence    = (request.form.get("evidence") or "").strip()
    project.highlight   = (request.form.get("highlight") or "").strip()
    
    ptype_raw = (request.form.get("project_type", project.project_type) or "").strip()
    ptype = "Corporativo" if ptype_raw.lower().startswith("corp") else "Pessoal"
    project.project_type = ptype
    project.fte_hours = float(request.form.get("fte_hours", project.fte_hours or 0) or 0) if ptype == "Corporativo" else None
    project.sustained = bool(request.form.get("sustained"))

    db.session.commit()
    return redirect(url_for("main.projects"))


@bp.post("/projects/set-all-corporate")
def set_all_corporate():
    """Marca todos os projetos como Corporativo."""
    affected = db.session.query(Project).update({"project_type": "Corporativo"})
    db.session.commit()
    flash(f"{affected} projeto(s) atualizado(s) para Corporativo.", "success")
    return redirect(url_for("main.projects"))


@bp.post("/projects/mark-sustained-corporate")
def mark_sustained_corporate():
    """Marca como sustentados todos os projetos do tipo Corporativo."""
    affected = (
        db.session.query(Project)
        .filter(Project.project_type == "Corporativo")
        .update({"sustained": True}, synchronize_session=False)
    )
    db.session.commit()
    flash(f"{affected} projeto(s) corporativos marcados como sustentados.", "success")
    return redirect(url_for("main.projects"))


@bp.post("/projects/<int:project_id>/delete")
def delete_project(project_id: int):
    """Exclui um projeto permanentemente."""
    project = Project.query.get_or_404(project_id)
    db.session.delete(project)
    db.session.commit()
    return redirect(url_for("main.projects"))


# =============================================================================
# BACKUP E RESTAURAÇÃO DOS DADOS
# =============================================================================

@bp.post("/projects/import_csv")
def import_projects_csv():
    """
    Importa projetos corporativos a partir de um CSV fornecido pelo usuário.

    Mapeamento de colunas (flexível):
      - Nome do projeto: "Projeto" | "Projetos" | "Nome" | "Name" (obrigatória)
      - Área (opcional): "Área" | "Area" — gravada genericamente no highlight
      - FTE (opcional): "FTE" | "FTEs" | "FTE (h)" | "FTE (horas)" — aceita vírgula como decimal
      - Progresso (opcional): "Progresso" | "Progress" — aceita "100%"; padrão 100
      - Status (opcional): se ausente, deduz de progresso

    Todos serão salvos como Corporativo e stack "UiPath". Nenhum dado sensível é copiado.
    """
    file = request.files.get("file")
    if not file:
        flash("Selecione um arquivo CSV.", "error")
        return redirect(request.referrer or url_for("main.projects"))

    try:
        raw = file.read()
        try:
            text = raw.decode("utf-8")
        except Exception:
            text = raw.decode("latin-1")

        reader = csv.DictReader(io.StringIO(text))
        inserted = 0

        def to_float(v):
            if v is None:
                return None
            s = str(v).strip()
            if not s:
                return None
            s = s.replace("%", "").replace(" ", "").replace(",", ".")
            try:
                return float(s)
            except Exception:
                return None

        def to_progress(v, default=100):
            if v is None:
                return default
            s = str(v).strip().replace("%", "")
            try:
                n = int(float(s))
                return max(0, min(n, 100))
            except Exception:
                return default

        for row in reader:
            keys = { (k or '').strip().lower(): (row[k] if row[k] is not None else '') for k in row.keys() }
            name = (keys.get("projeto") or keys.get("projetos") or keys.get("nome") or keys.get("name") or "").strip()
            if not name:
                continue
            area = (keys.get("área") or keys.get("area") or "").strip()
            fte = to_float(keys.get("fte") or keys.get("ftes") or keys.get("fte (h)") or keys.get("fte (horas)"))
            progress = to_progress(keys.get("progresso") or keys.get("progress"), 100)
            status = (keys.get("status") or "").strip().title()
            if not status:
                status = "Concluído" if progress >= 100 else "Em Desenvolvimento"

            description = "Automação UiPath corporativa. Detalhes funcionais suprimidos (LGPD/NDA)."
            highlight = f"Área: {area}" if area else "Projeto corporativo UiPath"

            db.session.add(Project(
                name=name,
                description=description,
                stack="UiPath",
                progress=progress,
                status=status,
                repo="",
                demo="",
                evidence="",
                highlight=highlight,
                project_type="Corporativo",
                fte_hours=fte,
            ))
            inserted += 1

        db.session.commit()
        flash(f"{inserted} projeto(s) importado(s) do CSV.", "success")
    except Exception:
        db.session.rollback()
        flash("Falha ao importar CSV. Verifique o formato e os cabeçalhos.", "error")

    return redirect(url_for("main.projects"))

@bp.get("/export")
def export_data():
    """
    Exporta todos os dados para um arquivo JSON.

    Monta um dicionário com todas as tarefas e projetos,
    converte para JSON formatado e envia como download para o browser.

    Útil para: fazer backup, migrar para outro servidor, ou compartilhar dados.
    """
    import json
    from pathlib import Path

    # Arquivo temporário onde o JSON será escrito antes do download
    tmp = Path("data/export.json")
    tmp.parent.mkdir(parents=True, exist_ok=True)

    # Monta o dicionário com todos os dados
    # "List comprehension" ([... for t in Task.query.all()]) = percorre cada item e monta um dict
    payload = {
        "tasks": [
            {
                "id": t.id,
                "title": t.title,
                "area": t.area,
                "priority": t.priority,
                "status": t.status,
                "due": t.due.isoformat() if t.due else None,  # Converte date para string "2026-09-18"
                "hours": t.hours,
                "completed": t.completed,
                "evidence": t.evidence,
                "notes": t.notes,
            }
            for t in Task.query.all()  # Para cada tarefa no banco
        ],
        "projects": [
            {
                "id": p.id,
                "name": p.name,
                "description": p.description,
                "stack": p.stack_list(),  # Converte CSV para lista Python
                "progress": p.progress,
                "status": p.status,
                "repo": p.repo,
                "demo": p.demo,
                "evidence": p.evidence,
                "highlight": p.highlight,
            }
            for p in Project.query.all()  # Para cada projeto no banco
        ],
        "certificates": [
            {
                "id": c.id,
                "name": c.name,
                "issuer": c.issuer,
                "area": c.area,
                "issued_date": c.issued_date.isoformat() if c.issued_date else None,
                "expiry_date": c.expiry_date.isoformat() if c.expiry_date else None,
                "linkedin_url": c.linkedin_url,
                "credential_url": c.credential_url,
                "credential_id": c.credential_id,
                "featured": bool(c.featured),
            }
            for c in Certificate.query.all()
        ],
    }

    # Escreve o JSON no arquivo com formatação legível (indent=2) e suporte a acentos
    tmp.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")

    # Envia o arquivo como download
    return send_file(tmp, as_attachment=True, download_name="intelligent-automation-portfolio.json")


@bp.post("/import")
def import_data():
    """
    Importa dados de um arquivo JSON previamente exportado.

    Fluxo:
      1. Lê o arquivo enviado pelo formulário
      2. Valida o formato (precisa ter "tasks" e "projects")
      3. Apaga os dados atuais do banco
      4. Insere os dados do arquivo
      5. Mostra mensagem de sucesso ou erro

    ATENÇÃO: Substitui TODOS os dados existentes. Use com cuidado!
    """
    import json

    file = request.files.get("file")
    if not file:
        flash("Selecione um arquivo JSON.", "error")
        return redirect(request.referrer or url_for("main.about"))

    try:
        # Lê e decodifica o arquivo JSON
        payload = json.loads(file.read().decode("utf-8"))

        # Valida se o formato é o esperado
        if not isinstance(payload, dict) or "tasks" not in payload or "projects" not in payload:
            raise ValueError("Formato inválido")

        # Apaga todos os dados atuais (limpa o banco antes de importar)
        Task.query.delete()
        Project.query.delete()
        Certificate.query.delete()
        db.session.commit()

        # Insere as tarefas do arquivo
        for t in payload.get("tasks", []):
            due = None
            if t.get("due"):
                try:
                    due = datetime.fromisoformat(t["due"]).date()  # Converte string para date
                except Exception:
                    pass  # Se a data for inválida, ignora
            db.session.add(
                Task(
                    title=t.get("title", ""),
                    area=t.get("area", "IA e Agentes"),
                    priority=t.get("priority", "Média"),
                    status=t.get("status", "Não iniciado"),
                    due=due,
                    hours=int(t.get("hours") or 1),
                    completed=bool(t.get("completed")),
                    evidence=t.get("evidence", ""),
                    notes=t.get("notes", ""),
                )
            )

        # Insere os projetos do arquivo
        for p in payload.get("projects", []):
            stack_val = p.get("stack", [])
            # O stack pode vir como lista (do export) ou como string — tratamos os dois casos
            if isinstance(stack_val, list):
                stack_val = ", ".join(stack_val)  # Converte lista de volta para CSV
            db.session.add(
                Project(
                    name=p.get("name", ""),
                    description=p.get("description", ""),
                    stack=stack_val,
                    progress=int(p.get("progress") or 0),
                    status=p.get("status", "Backlog"),
                    repo=p.get("repo", ""),
                    demo=p.get("demo", ""),
                    evidence=p.get("evidence", ""),
                    highlight=p.get("highlight", ""),
                )
            )

        # Insere os certificados do arquivo (opcional)
        for c in payload.get("certificates", []):
            issued = None
            expiry = None
            try:
                if c.get("issued_date"):
                    issued = datetime.fromisoformat(c["issued_date"]).date()
            except Exception:
                issued = None
            try:
                if c.get("expiry_date"):
                    expiry = datetime.fromisoformat(c["expiry_date"]).date()
            except Exception:
                expiry = None

            db.session.add(
                Certificate(
                    name=c.get("name", ""),
                    issuer=c.get("issuer", ""),
                    area=c.get("area", "Geral"),
                    issued_date=issued,
                    expiry_date=expiry,
                    linkedin_url=c.get("linkedin_url", ""),
                    credential_url=c.get("credential_url", ""),
                    credential_id=c.get("credential_id", ""),
                    featured=bool(c.get("featured", False)),
                )
            )

        db.session.commit()  # Confirma todos os inserts de uma vez
        flash("Dados importados com sucesso.", "success")

    except Exception:
        db.session.rollback()  # Desfaz qualquer mudança parcial em caso de erro
        flash("Arquivo JSON inválido.", "error")

    return redirect(request.referrer or url_for("main.about"))
