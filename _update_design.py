"""Rewrites all template and CSS files with the new React-style dark design."""
import os

BASE = r"D:\Meu Portfolio e HUB"

files = {}

# ── styles.css ──────────────────────────────────────────────────────────────
files["static/css/styles.css"] = r"""/* ==============================================
   DESIGN SYSTEM — Intelligent Automation Planner
   ============================================== */
:root {
  --bg:           #080c14;
  --surface:      #0d1321;
  --surface-2:    #111827;
  --border:       #1e293b;
  --border-h:     #243044;
  --text:         #f1f5f9;
  --text-dim:     #94a3b8;
  --text-muted:   #64748b;
  --blue:         #3b82f6;
  --blue-l:       #60a5fa;
  --purple:       #7c3aed;
  --purple-l:     #a78bfa;
  --green:        #10b981;
  --red:          #ef4444;
  --radius:       12px;
  --radius-sm:    8px;
  --radius-lg:    16px;
}

*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

body {
  background: var(--bg);
  color: var(--text);
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  font-size: 14px;
  line-height: 1.6;
  min-height: 100vh;
}

/* NAVBAR */
.app-nav {
  display: flex; align-items: center; justify-content: space-between;
  padding: .85rem 2rem;
  border-bottom: 1px solid var(--border);
  background: rgba(8,12,20,.92);
  backdrop-filter: blur(12px);
  position: sticky; top: 0; z-index: 100;
}
.brand { display: flex; align-items: center; gap: 12px; }
.brand-icon {
  width: 40px; height: 40px;
  background: linear-gradient(135deg, var(--blue), var(--purple));
  border-radius: 10px;
  display: flex; align-items: center; justify-content: center;
  font-size: 18px; flex-shrink: 0;
}
.brand-text small { color: var(--text-muted); font-size: 11px; display: block; letter-spacing: .4px; }
.brand-text strong { color: var(--text); font-size: 15px; font-weight: 600; display: block; }
.nav-actions { display: flex; align-items: center; gap: 8px; }

/* BUTTONS */
.btn {
  display: inline-flex; align-items: center; gap: 5px;
  padding: 7px 13px; border-radius: var(--radius-sm);
  border: 1px solid var(--border); background: var(--surface-2);
  color: var(--text); font-size: 13px; font-weight: 500;
  cursor: pointer; text-decoration: none;
  transition: all .15s; white-space: nowrap; font-family: inherit;
}
.btn:hover { background: var(--surface); border-color: var(--border-h); color: var(--text); }
.btn-primary { background: var(--blue); border-color: var(--blue); color: #fff; }
.btn-primary:hover { background: #2563eb; border-color: #2563eb; color: #fff; }
.btn-danger { background: transparent; border-color: transparent; color: var(--text-muted); }
.btn-danger:hover { background: rgba(239,68,68,.1); border-color: var(--red); color: var(--red); }
.btn-ghost { background: transparent; border-color: transparent; color: var(--text-dim); }
.btn-ghost:hover { background: var(--surface); border-color: var(--border); color: var(--text); }

/* LAYOUT */
.app-container { max-width: 1200px; margin: 0 auto; padding: 0 2rem 3rem; }

/* HERO */
.hero-section {
  display: grid; grid-template-columns: 1fr 310px;
  gap: 2rem; padding: 2.5rem 0 1.5rem; align-items: start;
}
.hero-badge {
  display: inline-flex; align-items: center; gap: 6px;
  background: rgba(59,130,246,.12); border: 1px solid rgba(59,130,246,.25);
  color: var(--blue-l); border-radius: 20px; padding: 4px 12px;
  font-size: 12px; margin-bottom: 1rem;
}
.hero-headline {
  font-size: 2.4rem; font-weight: 800; line-height: 1.15;
  margin-bottom: .75rem; color: var(--text);
}
.hero-headline .gradient {
  background: linear-gradient(135deg, var(--blue-l), var(--purple-l));
  -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;
}
.hero-desc { color: var(--text-dim); font-size: 14px; line-height: 1.75; max-width: 500px; }

.progress-card {
  background: var(--surface); border: 1px solid var(--border);
  border-radius: var(--radius-lg); padding: 1.5rem;
}
.progress-card-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: .4rem; }
.progress-card-label { color: var(--text-dim); font-size: 12px; }
.progress-card-icon {
  width: 28px; height: 28px; border: 2px solid var(--blue); border-radius: 50%;
  display: flex; align-items: center; justify-content: center; font-size: 11px; color: var(--blue);
}
.progress-percent { font-size: 2.4rem; font-weight: 700; line-height: 1; margin-bottom: .25rem; }
.progress-bar-wrap { background: var(--border); border-radius: 4px; height: 6px; margin: .75rem 0 .5rem; overflow: hidden; }
.progress-bar-fill { height: 100%; background: linear-gradient(90deg, var(--blue), var(--purple)); border-radius: 4px; transition: width .4s ease; }
.progress-sub { color: var(--text-muted); font-size: 12px; }

/* STATS */
.stats-row { display: grid; grid-template-columns: repeat(4,1fr); gap: 1rem; margin-bottom: 1.5rem; }
.stat-card { background: var(--surface); border: 1px solid var(--border); border-radius: var(--radius); padding: 1.25rem 1.5rem; }
.stat-icon { font-size: 18px; margin-bottom: .6rem; display: block; }
.stat-value { font-size: 1.75rem; font-weight: 700; line-height: 1; color: var(--text); display: block; margin-bottom: .2rem; }
.stat-label { color: var(--text-muted); font-size: 12px; }

/* TABS */
.tab-nav {
  display: flex; gap: 3px; background: var(--surface); border: 1px solid var(--border);
  border-radius: var(--radius); padding: 4px; margin-bottom: 1.5rem; width: fit-content;
}
.tab-link {
  display: inline-flex; align-items: center; gap: 6px; padding: 8px 16px;
  border-radius: var(--radius-sm); text-decoration: none; color: var(--text-dim);
  font-size: 13px; font-weight: 500; transition: all .15s; white-space: nowrap;
}
.tab-link:hover { color: var(--text); background: rgba(255,255,255,.05); }
.tab-link.active { background: var(--surface-2); color: var(--text); box-shadow: 0 0 0 1px var(--border); }

/* CARDS */
.card { background: var(--surface); border: 1px solid var(--border); border-radius: var(--radius); padding: 1.5rem; }
.card-title { font-size: 15px; font-weight: 600; color: var(--text); margin-bottom: 1rem; display: flex; align-items: center; gap: 8px; }

/* ABOUT */
.about-grid { display: grid; grid-template-columns: 1fr 310px; gap: 1.25rem; align-items: start; }
.about-side { display: flex; flex-direction: column; gap: 1rem; }
.tag-list { display: flex; flex-wrap: wrap; gap: 6px; margin-top: 1rem; }
.tag { background: rgba(59,130,246,.1); border: 1px solid rgba(59,130,246,.22); color: var(--blue-l); border-radius: 20px; padding: 3px 10px; font-size: 12px; }
.check-list { list-style: none; display: flex; flex-direction: column; gap: 10px; }
.check-list li { display: flex; align-items: flex-start; gap: 8px; font-size: 13px; color: var(--text-dim); }
.check-list li::before { content: '\2713'; color: var(--green); font-weight: 700; flex-shrink: 0; margin-top: 1px; }

/* SECTION HEADER */
.section-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 1.25rem; }
.section-title { font-size: 17px; font-weight: 600; color: var(--text); }
.section-sub { font-size: 12px; color: var(--text-muted); margin-top: 2px; }

/* FILTER */
.filter-bar { display: flex; gap: 8px; flex-wrap: wrap; margin-bottom: 1.25rem; }
.filter-bar input, .filter-bar select {
  background: var(--surface); border: 1px solid var(--border); border-radius: var(--radius-sm);
  color: var(--text); padding: 8px 12px; font-size: 13px; outline: none; transition: border-color .15s; font-family: inherit;
}
.filter-bar input:focus, .filter-bar select:focus { border-color: var(--blue); }
.filter-bar input { flex: 1; min-width: 160px; }
.filter-bar select { min-width: 140px; }
.filter-bar select option { background: var(--surface-2); }

/* ADD FORM */
.add-form { background: var(--surface); border: 1px solid var(--border); border-radius: var(--radius); padding: 1.25rem 1.5rem; margin-bottom: 1.5rem; }
.add-form-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: .85rem; }
.form-row { display: flex; flex-wrap: wrap; gap: 8px; align-items: flex-end; }
.form-row input, .form-row select {
  background: var(--surface-2); border: 1px solid var(--border); border-radius: var(--radius-sm);
  color: var(--text); padding: 8px 12px; font-size: 13px; outline: none; transition: border-color .15s; font-family: inherit;
}
.form-row input:focus, .form-row select:focus { border-color: var(--blue); }
.form-row input::placeholder { color: var(--text-muted); }
.form-row select option { background: var(--surface-2); }
.fr-lg { flex: 2; min-width: 180px; }
.fr-md { flex: 1; min-width: 120px; }
.fr-sm { width: 80px; }

/* TASK CARDS */
.tasks-grid { display: grid; grid-template-columns: repeat(auto-fill,minmax(300px,1fr)); gap: 1rem; }
.task-card { background: var(--surface); border: 1px solid var(--border); border-radius: var(--radius); padding: 1.25rem; display: flex; flex-direction: column; gap: .65rem; transition: border-color .15s; }
.task-card:hover { border-color: var(--border-h); }
.task-title { font-size: 14px; font-weight: 600; color: var(--text); line-height: 1.4; }
.task-meta { display: flex; flex-wrap: wrap; gap: 5px; align-items: center; }
.task-info { color: var(--text-muted); font-size: 12px; line-height: 1.5; }
.task-actions { display: flex; gap: 6px; justify-content: flex-end; margin-top: auto; padding-top: .25rem; }

/* BADGES */
.badge { display: inline-flex; align-items: center; background: rgba(148,163,184,.08); border: 1px solid rgba(148,163,184,.18); color: var(--text-dim); border-radius: 20px; padding: 2px 8px; font-size: 11px; font-weight: 500; }
.chip { border-radius: 20px; padding: 2px 8px; font-size: 11px; font-weight: 600; }
.chip.high { background: rgba(239,68,68,.15);  color: #fca5a5; border: 1px solid rgba(239,68,68,.3); }
.chip.med  { background: rgba(245,158,11,.15); color: #fcd34d; border: 1px solid rgba(245,158,11,.3); }
.chip.low  { background: rgba(16,185,129,.15); color: #6ee7b7; border: 1px solid rgba(16,185,129,.3); }
.chip.done { background: rgba(16,185,129,.15); color: #6ee7b7; border: 1px solid rgba(16,185,129,.3); }
.chip.wip  { background: rgba(59,130,246,.15); color: #93c5fd; border: 1px solid rgba(59,130,246,.3); }

/* PROJECT CARDS */
.projects-grid { display: grid; grid-template-columns: repeat(auto-fill,minmax(300px,1fr)); gap: 1rem; }
.project-card { background: var(--surface); border: 1px solid var(--border); border-radius: var(--radius); padding: 1.25rem; display: flex; flex-direction: column; gap: .65rem; transition: border-color .15s; }
.project-card:hover { border-color: var(--border-h); }
.project-title { font-size: 15px; font-weight: 600; color: var(--text); }
.project-desc { color: var(--text-dim); font-size: 13px; line-height: 1.6; }
.project-actions { display: flex; gap: 6px; justify-content: flex-end; margin-top: auto; }

/* SKILLS */
.skills-grid { display: grid; grid-template-columns: repeat(auto-fill,minmax(260px,1fr)); gap: 1rem; }
.skill-item { display: flex; align-items: center; gap: 8px; padding: .45rem 0; border-bottom: 1px solid var(--border); color: var(--text-dim); font-size: 13px; }
.skill-item:last-child { border-bottom: none; }
.skill-item::before { content: '\203A'; color: var(--blue-l); font-weight: 700; font-size: 16px; }

/* FORM PAGES */
.form-page { max-width: 600px; margin: 2rem auto 0; }
.form-group { display: flex; flex-direction: column; gap: 4px; margin-bottom: .85rem; }
.form-label { font-size: 11px; font-weight: 600; color: var(--text-muted); text-transform: uppercase; letter-spacing: .5px; }
.form-control { background: var(--surface-2); border: 1px solid var(--border); border-radius: var(--radius-sm); color: var(--text); padding: 9px 12px; font-size: 14px; width: 100%; outline: none; transition: border-color .15s; font-family: inherit; }
.form-control:focus { border-color: var(--blue); }
.form-control::placeholder { color: var(--text-muted); }
.form-control option { background: var(--surface-2); }
textarea.form-control { resize: vertical; min-height: 80px; }

/* ALERTS */
.alert { padding: 10px 16px; border-radius: var(--radius-sm); margin-bottom: 1rem; font-size: 13px; }
.alert.error   { background: rgba(239,68,68,.1);  border: 1px solid rgba(239,68,68,.3);  color: #fca5a5; }
.alert.success { background: rgba(16,185,129,.1); border: 1px solid rgba(16,185,129,.3); color: #6ee7b7; }

/* MISC */
a { color: var(--blue-l); text-decoration: none; }
a:hover { color: var(--blue); }
hr { border: none; border-top: 1px solid var(--border); margin: 1.25rem 0; }

.app-footer { border-top: 1px solid var(--border); padding: 1.25rem 2rem; display: flex; justify-content: space-between; color: var(--text-muted); font-size: 12px; margin-top: 2rem; }

/* RESPONSIVE */
@media (max-width: 900px) {
  .hero-section, .about-grid { grid-template-columns: 1fr; }
  .stats-row { grid-template-columns: repeat(2,1fr); }
}
@media (max-width: 600px) {
  .app-nav { padding: .75rem 1rem; flex-wrap: wrap; gap: 8px; }
  .app-container { padding: 0 1rem 2rem; }
  .hero-headline { font-size: 1.75rem; }
  .tab-nav { width: 100%; }
  .tab-link { padding: 8px 10px; font-size: 12px; }
}
"""

# ── base.html ────────────────────────────────────────────────────────────────
files["templates/base.html"] = """<!doctype html>
<html lang="pt-br">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Intelligent Automation Portfolio Planner</title>
  <link rel="stylesheet" href="{{ url_for('static', filename='css/styles.css') }}">
</head>
<body>

<nav class="app-nav">
  <div class="brand">
    <div class="brand-icon">&#129302;</div>
    <div class="brand-text">
      <small>Career &amp; Portfolio Tracker</small>
      <strong>Intelligent Automation Planner</strong>
    </div>
  </div>
  <div class="nav-actions">
    <a class="btn" href="{{ url_for('main.export_data') }}">&#11015; Backup</a>
    <form action="{{ url_for('main.import_data') }}" method="post" enctype="multipart/form-data" style="display:flex;align-items:center;gap:6px">
      <input type="file" name="file" accept="application/json" style="background:var(--surface-2);border:1px solid var(--border);border-radius:var(--radius-sm);color:var(--text);padding:6px 10px;font-size:12px;font-family:inherit;cursor:pointer;">
      <button class="btn" type="submit">&#11014; Restaurar</button>
    </form>
  </div>
</nav>

<div class="app-container">
  {% with messages = get_flashed_messages(with_categories=true) %}
    {% if messages %}
      {% for category, message in messages %}
        <div class="alert {{ category }}" style="margin-top:1rem">{{ message }}</div>
      {% endfor %}
    {% endif %}
  {% endwith %}
  {% block content %}{% endblock %}
</div>

<footer class="app-footer">
  <span>&#128190; SQLite local &mdash; data/app.db</span>
  <span>Construindo hoje as habilidades da automa&#231;&#227;o de amanh&#227;.</span>
</footer>

<script src="{{ url_for('static', filename='js/main.js') }}"></script>
</body>
</html>
"""

# ── MACRO: stats row + tab nav (used in every page) ─────────────────────────
STATS = """
<div class="stats-row">
  <div class="stat-card">
    <span class="stat-icon">&#9776;</span>
    <span class="stat-value">{{ stats.done }}</span>
    <span class="stat-label">Tarefas conclu&#237;das</span>
  </div>
  <div class="stat-card">
    <span class="stat-icon">&#128197;</span>
    <span class="stat-value">{{ stats.hours }}h</span>
    <span class="stat-label">Horas planejadas</span>
  </div>
  <div class="stat-card">
    <span class="stat-icon">&#10003;</span>
    <span class="stat-value">{{ stats.doneHours }}h</span>
    <span class="stat-label">Horas entregues</span>
  </div>
  <div class="stat-card">
    <span class="stat-icon">&#128640;</span>
    <span class="stat-value">{{ stats.activeProjects }}</span>
    <span class="stat-label">Projetos ativos</span>
  </div>
</div>
"""

def tabs(active):
    items = [
        ("about",    "&#128100; Sobre mim"),
        ("planner",  "&#8862; Plano"),
        ("projects", "&#128193; Projetos"),
        ("skills",   "&lt;/&gt; Compet&#234;ncias"),
    ]
    links = ""
    for key, label in items:
        cls = "tab-link active" if key == active else "tab-link"
        url = "{{ url_for('main." + key + "') }}"
        links += f'  <a class="{cls}" href="{url}">{label}</a>\n'
    return f'<nav class="tab-nav">\n{links}</nav>\n'


# ── about.html ───────────────────────────────────────────────────────────────
files["templates/about.html"] = """{{% extends 'base.html' %}}
{{% block content %}}

<section class="hero-section">
  <div>
    <div class="hero-badge">&#9881; Em evolu&#231;&#227;o cont&#237;nua</div>
    <h1 class="hero-headline">
      RPA s&#243;lido. IA aplicada.<br>
      <span class="gradient">Automa&#231;&#227;o sem limites<br>de ferramenta.</span>
    </h1>
    <p class="hero-desc">Este painel re&#250;ne minha trajet&#243;ria, projetos, estudos e evid&#234;ncias pr&#225;ticas em automa&#231;&#227;o inteligente.</p>
  </div>
  <div>
    <div class="progress-card">
      <div class="progress-card-header">
        <span class="progress-card-label">Progresso geral</span>
        <div class="progress-card-icon">&#9711;</div>
      </div>
      <div class="progress-percent">{{{{ stats.progress }}}}%</div>
      <div class="progress-bar-wrap">
        <div class="progress-bar-fill" style="width:{{{{ stats.progress }}}}%"></div>
      </div>
      <div class="progress-sub">{{{{ stats.done }}}} de {{{{ stats.total }}}} tarefas conclu&#237;das</div>
    </div>
  </div>
</section>

""" + STATS + tabs("about") + """
<div class="about-grid">
  <div>
    <div class="card">
      <div class="card-title">&#128100; Sobre mim</div>
      <p style="color:var(--text-dim);font-size:13px;line-height:1.8;margin-bottom:.75rem">
        Atuo com automa&#231;&#227;o de processos e tecnologia, desenvolvendo, implantando e sustentando solu&#231;&#245;es corporativas que conectam sistemas, regras de neg&#243;cio e efici&#234;ncia operacional.
      </p>
      <p style="color:var(--text-dim);font-size:13px;line-height:1.8;margin-bottom:.75rem">
        Experi&#234;ncia com RPA, REFramework, Orchestrator, Queues, automa&#231;&#245;es SAP, integra&#231;&#245;es via APIs REST, tratamento de exce&#231;&#245;es e monitoramento.
      </p>
      <p style="color:var(--text-dim);font-size:13px;line-height:1.8">
        Ampliando atua&#231;&#227;o em Intelligent Automation: GenAI, LLMs, AI Agents, Microsoft Copilot, MCP e n8n. Objetivo: combinar automa&#231;&#227;o, IA e integra&#231;&#245;es para solu&#231;&#245;es escal&#225;veis.
      </p>
      <div class="tag-list">
        {{% for tag in ['Intelligent Automation','RPA','GenAI','AI Agents','API Integration','SAP','UiPath','MCP','n8n'] %}}
          <span class="tag">{{{{ tag }}}}</span>
        {{% endfor %}}
      </div>
    </div>
  </div>
  <div class="about-side">
    <div class="card">
      <div class="card-title">&#9679; Objetivo profissional</div>
      <p style="color:var(--text-dim);font-size:13px;line-height:1.7">
        Evoluir como especialista em automa&#231;&#227;o inteligente, mantendo profundidade em RPA e ampliando compet&#234;ncias em agentes, IA generativa, APIs e arquitetura de solu&#231;&#245;es.
      </p>
    </div>
    <div class="card">
      <div class="card-title">&#127885; O que este portf&#243;lio comprova</div>
      <ul class="check-list">
        <li>Aprendizado cont&#237;nuo com entregas pr&#225;ticas</li>
        <li>Projetos documentados e evolu&#231;&#227;o mensur&#225;vel</li>
        <li>Evid&#234;ncias por c&#243;digo, demonstra&#231;&#227;o e conte&#250;do t&#233;cnico</li>
      </ul>
    </div>
  </div>
</div>

{{% endblock %}}
"""

# ── planner.html ─────────────────────────────────────────────────────────────
files["templates/planner.html"] = """{{% extends 'base.html' %}}
{{% block content %}}

<div style="padding-top:1.5rem">
""" + STATS + tabs("planner") + """
<div class="section-header">
  <div>
    <div class="section-title">Plano de aprendizado</div>
    <div class="section-sub">{{{{ stats.done }}}} de {{{{ stats.total }}}} tarefas conclu&#237;das</div>
  </div>
  <div style="display:flex;align-items:center;gap:.75rem">
    <div style="width:180px">
      <div class="progress-bar-wrap"><div class="progress-bar-fill" style="width:{{{{ stats.progress }}}}%"></div></div>
      <div class="progress-sub" style="margin-top:4px">{{{{ stats.progress }}}}% conclu&#237;do</div>
    </div>
  </div>
</div>

<form method="get" action="{{{{ url_for('main.planner') }}}}">
  <div class="filter-bar">
    <input name="q" placeholder="&#128269; Buscar tarefa..." value="{{{{ q }}}}">
    <select name="area">
      <option value="Todas" {{{{ 'selected' if area=='Todas' else '' }}}}>Todas as &#225;reas</option>
      {{% for opt in ['Marca profissional','IA e Agentes','APIs e Integra&#231;&#245;es','n8n','UiPath','Conte&#250;do'] %}}
        <option value="{{{{ opt }}}}" {{{{ 'selected' if area==opt else '' }}}}>{{{{ opt }}}}</option>
      {{% endfor %}}
    </select>
    <select name="status">
      {{% for opt in ['Todos','N&#227;o iniciado','Em andamento','Conclu&#237;do'] %}}
        <option value="{{{{ opt }}}}" {{{{ 'selected' if status==opt else '' }}}}>{{{{ opt }}}}</option>
      {{% endfor %}}
    </select>
    <button class="btn btn-primary" type="submit">Filtrar</button>
  </div>
</form>

<div class="add-form">
  <div class="add-form-header">
    <span class="section-title" style="font-size:15px">Adicionar tarefa</span>
    <span class="section-sub">T&#237;tulo obrigat&#243;rio</span>
  </div>
  <form method="post" action="{{{{ url_for('main.add_task') }}}}">
    <div class="form-row">
      <input class="fr-lg" name="title" placeholder="T&#237;tulo da tarefa" required>
      <select class="fr-md" name="area">
        {{% for opt in ['Marca profissional','IA e Agentes','APIs e Integra&#231;&#245;es','n8n','UiPath','Conte&#250;do'] %}}
          <option value="{{{{ opt }}}}">{{{{ opt }}}}</option>
        {{% endfor %}}
      </select>
      <select class="fr-md" name="priority">
        {{% for opt in ['Alta','M&#233;dia','Baixa'] %}}
          <option value="{{{{ opt }}}}">{{{{ opt }}}}</option>
        {{% endfor %}}
      </select>
      <select class="fr-md" name="status">
        {{% for opt in ['N&#227;o iniciado','Em andamento','Conclu&#237;do'] %}}
          <option value="{{{{ opt }}}}">{{{{ opt }}}}</option>
        {{% endfor %}}
      </select>
      <input class="fr-md" type="date" name="due">
      <input class="fr-sm" type="number" min="1" name="hours" value="1">
      <input class="fr-md" name="evidence" placeholder="Link evid&#234;ncia">
      <input class="fr-lg" name="notes" placeholder="Anota&#231;&#245;es">
      <button class="btn btn-primary" type="submit">Salvar</button>
    </div>
  </form>
</div>

<div class="tasks-grid">
  {{% for task in tasks %}}
    <div class="task-card">
      <div class="task-title">{{{{ task.title }}}}</div>
      <div class="task-meta">
        <span class="badge">{{{{ task.area }}}}</span>
        <span class="chip {{{{ 'high' if task.priority=='Alta' else ('med' if task.priority=='M&#233;dia' else 'low') }}}}">{{{{ task.priority }}}}</span>
        {{% if task.status == 'Conclu&#237;do' %}}
          <span class="chip done">{{{{ task.status }}}}</span>
        {{% elif task.status == 'Em andamento' %}}
          <span class="chip wip">{{{{ task.status }}}}</span>
        {{% else %}}
          <span class="badge">{{{{ task.status }}}}</span>
        {{% endif %}}
      </div>
      <div class="task-info">
        {{{{ task.due or 'Sem prazo' }}}} &middot; {{{{ task.hours }}}}h
        {{% if task.evidence %}} &middot; <a href="{{{{ task.evidence }}}}" target="_blank">Evid&#234;ncia &#8599;</a>{{% endif %}}
      </div>
      {{% if task.notes %}}<div class="task-info">{{{{ task.notes }}}}</div>{{% endif %}}
      <div class="task-actions">
        <form method="post" action="{{{{ url_for('main.toggle_task', task_id=task.id) }}}}" style="display:inline">
          <button class="btn" type="submit">{{{{ '&#8629; Desfazer' if task.completed or task.status=='Conclu&#237;do' else '&#10003; Concluir' }}}}</button>
        </form>
        <a class="btn" href="{{{{ url_for('main.edit_task', task_id=task.id) }}}}">&#9998; Editar</a>
        <form method="post" action="{{{{ url_for('main.delete_task', task_id=task.id) }}}}" style="display:inline">
          <button class="btn btn-danger" type="submit">&#10005;</button>
        </form>
      </div>
    </div>
  {{% endfor %}}
</div>
</div>
{{% endblock %}}
"""

# ── projects.html ────────────────────────────────────────────────────────────
files["templates/projects.html"] = """{{% extends 'base.html' %}}
{{% block content %}}

<div style="padding-top:1.5rem">
""" + STATS + tabs("projects") + """
<div class="section-header">
  <div>
    <div class="section-title">Projetos</div>
    <div class="section-sub">{{{{ projects|length }}}} projeto(s) cadastrado(s)</div>
  </div>
</div>

<div class="add-form">
  <div class="add-form-header">
    <span class="section-title" style="font-size:15px">Adicionar projeto</span>
  </div>
  <form method="post" action="{{{{ url_for('main.add_project') }}}}">
    <div class="form-row">
      <input class="fr-lg" name="name" placeholder="Nome do projeto" required>
      <input class="fr-lg" name="description" placeholder="Descri&#231;&#227;o">
      <input class="fr-md" name="stack" placeholder="Tecnologias (v&#237;rgula)">
      <select class="fr-md" name="status">
        {{% for opt in ['Backlog','Discovery','Em desenvolvimento','Conclu&#237;do'] %}}
          <option value="{{{{ opt }}}}">{{{{ opt }}}}</option>
        {{% endfor %}}
      </select>
      <input class="fr-sm" type="number" min="0" max="100" name="progress" value="0" placeholder="%">
      <input class="fr-md" name="repo" placeholder="GitHub (link)">
      <input class="fr-md" name="demo" placeholder="Demo (link)">
      <input class="fr-md" name="highlight" placeholder="Destaque">
      <button class="btn btn-primary" type="submit">Adicionar</button>
    </div>
  </form>
</div>

<div class="projects-grid">
  {{% for p in projects %}}
    <div class="project-card">
      <div class="project-title">{{{{ p.name }}}}</div>
      <div class="task-meta">
        <span class="badge">{{{{ p.status }}}}</span>
        <span class="section-sub">{{{{ p.progress }}}}%</span>
      </div>
      {{% if p.description %}}<div class="project-desc">{{{{ p.description }}}}</div>{{% endif %}}
      <div class="progress-bar-wrap"><div class="progress-bar-fill" style="width:{{{{ p.progress }}}}%"></div></div>
      <div class="task-meta" style="flex-wrap:wrap;gap:4px">
        {{% for tech in p.stack %}}
          <span class="badge">{{{{ tech }}}}</span>
        {{% endfor %}}
      </div>
      <div class="task-info">
        {{% if p.repo %}}<a href="{{{{ p.repo }}}}" target="_blank">C&#243;digo &#8599;</a>{{% endif %}}
        {{% if p.demo %}} &middot; <a href="{{{{ p.demo }}}}" target="_blank">Demo &#8599;</a>{{% endif %}}
        {{% if p.evidence %}} &middot; <a href="{{{{ p.evidence }}}}" target="_blank">Evid&#234;ncia &#8599;</a>{{% endif %}}
      </div>
      <div class="project-actions">
        <a class="btn" href="{{{{ url_for('main.edit_project', project_id=p.id) }}}}">&#9998; Editar</a>
        <form method="post" action="{{{{ url_for('main.delete_project', project_id=p.id) }}}}" style="display:inline">
          <button class="btn btn-danger" type="submit">&#10005;</button>
        </form>
      </div>
    </div>
  {{% endfor %}}
</div>
</div>
{{% endblock %}}
"""

# ── skills.html ──────────────────────────────────────────────────────────────
files["templates/skills.html"] = """{{% extends 'base.html' %}}
{{% block content %}}

<div style="padding-top:1.5rem">
""" + STATS + tabs("skills") + """
<div class="section-header">
  <div class="section-title">Compet&#234;ncias t&#233;cnicas</div>
</div>

<div class="skills-grid">
  {{% for block in skills_blocks %}}
    <div class="card">
      <div class="card-title">{{{{ block.title }}}}</div>
      <ul style="list-style:none;padding:0;margin:0">
        {{% for item in block.items %}}
          <div class="skill-item">{{{{ item }}}}</div>
        {{% endfor %}}
      </ul>
    </div>
  {{% endfor %}}
</div>
</div>
{{% endblock %}}
"""

# ── edit_task.html ───────────────────────────────────────────────────────────
files["templates/edit_task.html"] = """{{% extends 'base.html' %}}
{{% block content %}}
<div class="form-page">
  <div style="margin-bottom:1.5rem">
    <div class="section-title">Editar tarefa</div>
  </div>
  <div class="card">
    <form method="post">
      <div class="form-group">
        <label class="form-label">T&#237;tulo</label>
        <input class="form-control" name="title" value="{{{{ task.title }}}}" required>
      </div>
      <div class="form-group">
        <label class="form-label">&#193;rea</label>
        <select class="form-control" name="area">
          {{% for opt in ['Marca profissional','IA e Agentes','APIs e Integra&#231;&#245;es','n8n','UiPath','Conte&#250;do'] %}}
            <option value="{{{{ opt }}}}" {{{{ 'selected' if task.area==opt else '' }}}}>{{{{ opt }}}}</option>
          {{% endfor %}}
        </select>
      </div>
      <div class="form-group">
        <label class="form-label">Prioridade</label>
        <select class="form-control" name="priority">
          {{% for opt in ['Alta','M&#233;dia','Baixa'] %}}
            <option value="{{{{ opt }}}}" {{{{ 'selected' if task.priority==opt else '' }}}}>{{{{ opt }}}}</option>
          {{% endfor %}}
        </select>
      </div>
      <div class="form-group">
        <label class="form-label">Status</label>
        <select class="form-control" name="status">
          {{% for opt in ['N&#227;o iniciado','Em andamento','Conclu&#237;do'] %}}
            <option value="{{{{ opt }}}}" {{{{ 'selected' if task.status==opt else '' }}}}>{{{{ opt }}}}</option>
          {{% endfor %}}
        </select>
      </div>
      <div class="form-group">
        <label class="form-label">Prazo</label>
        <input class="form-control" type="date" name="due" value="{{{{ task.due }}}}">
      </div>
      <div class="form-group">
        <label class="form-label">Horas</label>
        <input class="form-control" type="number" min="1" name="hours" value="{{{{ task.hours }}}}">
      </div>
      <div class="form-group">
        <label class="form-label">Evid&#234;ncia (link)</label>
        <input class="form-control" name="evidence" value="{{{{ task.evidence }}}}">
      </div>
      <div class="form-group">
        <label class="form-label">Anota&#231;&#245;es</label>
        <input class="form-control" name="notes" value="{{{{ task.notes }}}}">
      </div>
      <div style="display:flex;gap:8px;margin-top:1rem">
        <button class="btn btn-primary" type="submit">Salvar</button>
        <a class="btn" href="{{{{ url_for('main.planner') }}}}">Cancelar</a>
      </div>
    </form>
  </div>
</div>
{{% endblock %}}
"""

# ── edit_project.html ────────────────────────────────────────────────────────
files["templates/edit_project.html"] = """{{% extends 'base.html' %}}
{{% block content %}}
<div class="form-page">
  <div style="margin-bottom:1.5rem">
    <div class="section-title">Editar projeto</div>
  </div>
  <div class="card">
    <form method="post">
      <div class="form-group">
        <label class="form-label">Nome</label>
        <input class="form-control" name="name" value="{{{{ project.name }}}}" required>
      </div>
      <div class="form-group">
        <label class="form-label">Descri&#231;&#227;o</label>
        <textarea class="form-control" name="description">{{{{ project.description }}}}</textarea>
      </div>
      <div class="form-group">
        <label class="form-label">Tecnologias (v&#237;rgula)</label>
        <input class="form-control" name="stack" value="{{{{ project.stack }}}}">
      </div>
      <div class="form-group">
        <label class="form-label">Status</label>
        <select class="form-control" name="status">
          {{% for opt in ['Backlog','Discovery','Em desenvolvimento','Conclu&#237;do'] %}}
            <option value="{{{{ opt }}}}" {{{{ 'selected' if project.status==opt else '' }}}}>{{{{ opt }}}}</option>
          {{% endfor %}}
        </select>
      </div>
      <div class="form-group">
        <label class="form-label">Progresso (%)</label>
        <input class="form-control" type="number" min="0" max="100" name="progress" value="{{{{ project.progress }}}}">
      </div>
      <div class="form-group">
        <label class="form-label">GitHub (link)</label>
        <input class="form-control" name="repo" value="{{{{ project.repo }}}}">
      </div>
      <div class="form-group">
        <label class="form-label">Demo (link)</label>
        <input class="form-control" name="demo" value="{{{{ project.demo }}}}">
      </div>
      <div class="form-group">
        <label class="form-label">Evid&#234;ncia (link)</label>
        <input class="form-control" name="evidence" value="{{{{ project.evidence }}}}">
      </div>
      <div class="form-group">
        <label class="form-label">Destaque</label>
        <input class="form-control" name="highlight" value="{{{{ project.highlight }}}}">
      </div>
      <div style="display:flex;gap:8px;margin-top:1rem">
        <button class="btn btn-primary" type="submit">Salvar</button>
        <a class="btn" href="{{{{ url_for('main.projects') }}}}">Cancelar</a>
      </div>
    </form>
  </div>
</div>
{{% endblock %}}
"""

# ── Write files ──────────────────────────────────────────────────────────────
for rel_path, content in files.items():
    full_path = os.path.join(BASE, rel_path)
    with open(full_path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"OK  {rel_path}")

print("\nDone! Reload the browser.")
