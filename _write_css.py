css = r"""/* ============================================
   DESIGN SYSTEM - Intelligent Automation Planner
   React-style dark UI
   ============================================ */

:root {
  --bg:          #080c14;
  --surface:     #0d1321;
  --surface-2:   #111827;
  --border:      #1e293b;
  --border-h:    #2d3f58;
  --text:        #f1f5f9;
  --text-dim:    #94a3b8;
  --text-muted:  #64748b;
  --blue:        #3b82f6;
  --blue-light:  #60a5fa;
  --purple:      #7c3aed;
  --purple-light:#a78bfa;
  --green:       #10b981;
  --red:         #ef4444;
  --r:           12px;
  --r-sm:        8px;
  --r-lg:        16px;
}

*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

body {
  background: var(--bg);
  color: var(--text);
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
  font-size: 14px;
  line-height: 1.6;
  min-height: 100vh;
}

/* ---- NAVBAR ---- */
.app-nav {
  display: flex; align-items: center; justify-content: space-between;
  padding: .875rem 2rem;
  border-bottom: 1px solid var(--border);
  background: rgba(8,12,20,.95);
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
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
.brand-text small { display: block; font-size: 11px; color: var(--text-muted); letter-spacing: .3px; }
.brand-text strong { font-size: 15px; font-weight: 600; color: var(--text); }
.nav-actions { display: flex; align-items: center; gap: 8px; flex-wrap: wrap; }

.recruiter-toggle {
  display: flex; align-items: center; gap: 7px;
  background: var(--surface-2); border: 1px solid var(--border);
  border-radius: 20px; padding: 5px 12px;
  font-size: 12px; color: var(--text-dim); cursor: pointer; user-select: none;
}
.toggle-track {
  width: 34px; height: 18px; background: var(--border);
  border-radius: 9px; position: relative; transition: background .2s;
}
.toggle-track::after {
  content: ""; position: absolute;
  width: 12px; height: 12px; background: #fff;
  border-radius: 50%; top: 3px; left: 3px; transition: left .2s;
}
.toggle-track.on { background: var(--blue); }
.toggle-track.on::after { left: 19px; }

/* ---- BUTTONS ---- */
.btn {
  display: inline-flex; align-items: center; gap: 5px;
  padding: 6px 13px; border-radius: var(--r-sm);
  border: 1px solid var(--border); background: var(--surface-2);
  color: var(--text); font-size: 13px; font-weight: 500;
  cursor: pointer; text-decoration: none;
  transition: all .15s; white-space: nowrap;
}
.btn:hover { background: var(--surface); border-color: var(--border-h); color: var(--text); }
.btn-primary { background: var(--blue); border-color: var(--blue); color: #fff; }
.btn-primary:hover { background: #2563eb; border-color: #2563eb; color: #fff; }
.btn-ghost { background: transparent; border-color: transparent; color: var(--text-dim); }
.btn-ghost:hover { background: rgba(255,255,255,.05); color: var(--text); }
.btn-danger { color: var(--red); border-color: transparent; background: transparent; }
.btn-danger:hover { background: rgba(239,68,68,.1); border-color: var(--red); color: var(--red); }

/* ---- LAYOUT ---- */
.app-wrap { max-width: 1200px; margin: 0 auto; padding: 0 2rem 4rem; }

/* ---- HERO ---- */
.hero {
  display: grid; grid-template-columns: 1fr 340px;
  gap: 2rem; padding: 2.5rem 0 2rem; align-items: start;
}
.hero-badge {
  display: inline-flex; align-items: center; gap: 6px;
  background: rgba(59,130,246,.1); border: 1px solid rgba(59,130,246,.25);
  color: var(--blue-light); border-radius: 20px;
  padding: 3px 11px; font-size: 12px; margin-bottom: .9rem;
}
.hero-headline { font-size: 2.5rem; font-weight: 800; line-height: 1.15; margin-bottom: .7rem; color: var(--text); }
.hero-headline .grad {
  background: linear-gradient(135deg, var(--blue-light), var(--purple-light));
  -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;
}
.hero-desc { color: var(--text-dim); font-size: 14px; max-width: 520px; line-height: 1.75; }

/* Progress card */
.prog-card { background: var(--surface); border: 1px solid var(--border); border-radius: var(--r-lg); padding: 1.5rem; }
.prog-card-head { display: flex; justify-content: space-between; align-items: center; margin-bottom: .4rem; }
.prog-card-label { font-size: 12px; color: var(--text-dim); }
.prog-card-icon {
  width: 30px; height: 30px; border-radius: 50%;
  border: 2px solid var(--blue);
  display: flex; align-items: center; justify-content: center;
  font-size: 13px; color: var(--blue);
}
.prog-pct { font-size: 2.4rem; font-weight: 700; line-height: 1; color: var(--text); }
.prog-sub { font-size: 12px; color: var(--text-muted); margin-top: .35rem; }

/* Progress bar */
.pbar { background: var(--border); border-radius: 4px; height: 6px; overflow: hidden; margin: .7rem 0 .4rem; }
.pbar-fill { height: 100%; background: linear-gradient(90deg, var(--blue), var(--purple)); border-radius: 4px; transition: width .4s ease; }

/* ---- STATS ---- */
.stats-row { display: grid; grid-template-columns: repeat(4,1fr); gap: 1rem; margin-bottom: 2rem; }
.stat-card { background: var(--surface); border: 1px solid var(--border); border-radius: var(--r); padding: 1.2rem 1.4rem; }
.stat-icon { font-size: 19px; display: block; margin-bottom: .65rem; opacity: .85; }
.stat-val  { font-size: 1.8rem; font-weight: 700; display: block; margin-bottom: .2rem; color: var(--text); }
.stat-lbl  { font-size: 12px; color: var(--text-muted); }

/* ---- TABS ---- */
.tab-bar {
  display: flex; gap: 3px;
  background: var(--surface); border: 1px solid var(--border);
  border-radius: var(--r); padding: 4px;
  width: fit-content; margin-bottom: 1.5rem;
}
.tab-link {
  display: inline-flex; align-items: center; gap: 6px;
  padding: 7px 15px; border-radius: var(--r-sm);
  text-decoration: none; color: var(--text-dim);
  font-size: 13px; font-weight: 500;
  transition: all .15s; white-space: nowrap;
}
.tab-link:hover { color: var(--text); background: rgba(255,255,255,.04); }
.tab-link.active { background: var(--surface-2); color: var(--text); box-shadow: 0 0 0 1px var(--border); }

/* ---- CARDS ---- */
.card { background: var(--surface); border: 1px solid var(--border); border-radius: var(--r); padding: 1.4rem; }
.card:hover { border-color: var(--border-h); }
.card-title { font-size: 15px; font-weight: 600; color: var(--text); margin-bottom: .9rem; display: flex; align-items: center; gap: 7px; }

/* ---- ABOUT ---- */
.about-grid { display: grid; grid-template-columns: 1fr 320px; gap: 1.25rem; align-items: start; }
.about-side { display: flex; flex-direction: column; gap: 1rem; }
.card-text { font-size: 13px; color: var(--text-dim); line-height: 1.75; margin-bottom: .75rem; }
.tag-row { display: flex; flex-wrap: wrap; gap: 6px; margin-top: 1rem; }
.tag { background: rgba(59,130,246,.1); border: 1px solid rgba(59,130,246,.2); color: var(--blue-light); border-radius: 20px; padding: 3px 9px; font-size: 12px; }
.check-list { list-style: none; display: flex; flex-direction: column; gap: 9px; }
.check-list li { display: flex; align-items: flex-start; gap: 7px; font-size: 13px; color: var(--text-dim); }
.check-list li::before { content: "✓"; color: var(--green); font-weight: 700; flex-shrink: 0; }

/* ---- SECTION HEADER ---- */
.sec-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 1.2rem; }
.sec-title { font-size: 17px; font-weight: 600; color: var(--text); }
.sec-sub   { font-size: 12px; color: var(--text-muted); margin-top: 2px; }

/* ---- FILTER BAR ---- */
.filter-bar { display: flex; gap: 7px; flex-wrap: wrap; margin-bottom: 1.25rem; }
.filter-bar input, .filter-bar select {
  background: var(--surface); border: 1px solid var(--border);
  border-radius: var(--r-sm); color: var(--text);
  padding: 7px 11px; font-size: 13px; outline: none;
}
.filter-bar input  { flex: 1; min-width: 150px; }
.filter-bar select { min-width: 130px; }
.filter-bar input:focus, .filter-bar select:focus { border-color: var(--blue); }
.filter-bar input::placeholder { color: var(--text-muted); }

/* ---- ADD FORM ---- */
.add-form { background: var(--surface); border: 1px solid var(--border); border-radius: var(--r); padding: 1.2rem 1.4rem; margin-bottom: 1.5rem; }
.form-row { display: flex; flex-wrap: wrap; gap: 7px; align-items: flex-end; }
.form-row input, .form-row select, .form-row textarea {
  background: var(--surface-2); border: 1px solid var(--border);
  border-radius: var(--r-sm); color: var(--text);
  padding: 7px 11px; font-size: 13px; outline: none;
}
.form-row input:focus, .form-row select:focus { border-color: var(--blue); }
.form-row input::placeholder { color: var(--text-muted); }
.fr-lg { flex: 2; min-width: 180px; }
.fr-md { flex: 1; min-width: 110px; }
.fr-sm { width: 75px; }

/* ---- TASK CARDS ---- */
.tasks-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(310px,1fr)); gap: 1rem; }
.task-card {
  background: var(--surface); border: 1px solid var(--border);
  border-radius: var(--r); padding: 1.2rem;
  display: flex; flex-direction: column; gap: .65rem; transition: border-color .15s;
}
.task-card:hover { border-color: var(--border-h); }
.task-title { font-size: 14px; font-weight: 600; color: var(--text); line-height: 1.4; }
.task-meta  { display: flex; flex-wrap: wrap; gap: 5px; align-items: center; }
.task-info  { font-size: 12px; color: var(--text-muted); }
.task-acts  { display: flex; gap: 5px; justify-content: flex-end; margin-top: auto; }

/* ---- PROJECTS ---- */
.proj-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(310px,1fr)); gap: 1rem; }
.proj-card {
  background: var(--surface); border: 1px solid var(--border);
  border-radius: var(--r); padding: 1.2rem;
  display: flex; flex-direction: column; gap: .65rem;
}
.proj-card:hover { border-color: var(--border-h); }
.proj-title { font-size: 14px; font-weight: 600; color: var(--text); }
.proj-desc  { font-size: 13px; color: var(--text-dim); line-height: 1.65; }
.proj-links { display: flex; gap: 10px; font-size: 13px; }

/* ---- SKILLS ---- */
.skills-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(270px,1fr)); gap: 1rem; }
.skill-item { font-size: 13px; color: var(--text-dim); padding: 5px 0; border-bottom: 1px solid rgba(30,41,59,.6); }
.skill-item:last-child { border-bottom: none; }

/* ---- BADGES & CHIPS ---- */
.badge {
  display: inline-flex; align-items: center;
  padding: 2px 8px; border-radius: 20px;
  background: rgba(148,163,184,.08); border: 1px solid rgba(148,163,184,.18);
  color: var(--text-dim); font-size: 11px; font-weight: 500;
}
.chip { display: inline-block; padding: 2px 8px; border-radius: 20px; font-size: 11px; font-weight: 600; }
.chip.high { background: rgba(239,68,68,.14);  color: #fca5a5; border: 1px solid rgba(239,68,68,.3); }
.chip.med  { background: rgba(245,158,11,.14); color: #fcd34d; border: 1px solid rgba(245,158,11,.3); }
.chip.low  { background: rgba(16,185,129,.14); color: #6ee7b7; border: 1px solid rgba(16,185,129,.3); }
.chip.done { background: rgba(16,185,129,.14); color: #6ee7b7; border: 1px solid rgba(16,185,129,.3); }
.chip.wip  { background: rgba(59,130,246,.14); color: #93c5fd; border: 1px solid rgba(59,130,246,.3); }

/* ---- FORM PAGES ---- */
.form-page { max-width: 620px; margin: 1.5rem auto 0; }
.fgroup { display: flex; flex-direction: column; gap: 4px; margin-bottom: 1rem; }
.flabel { font-size: 11px; font-weight: 600; color: var(--text-muted); text-transform: uppercase; letter-spacing: .5px; }
.finput {
  background: var(--surface-2); border: 1px solid var(--border);
  border-radius: var(--r-sm); color: var(--text);
  padding: 9px 12px; font-size: 14px; width: 100%; outline: none;
}
.finput:focus { border-color: var(--blue); }
.finput::placeholder { color: var(--text-muted); }
textarea.finput { resize: vertical; min-height: 80px; font-family: inherit; }
select.finput option { background: var(--surface-2); color: var(--text); }

/* ---- ALERTS ---- */
.alert { padding: 9px 14px; border-radius: var(--r-sm); margin-bottom: 1rem; font-size: 13px; }
.alert.error   { background: rgba(239,68,68,.1);  border: 1px solid rgba(239,68,68,.3);  color: #fca5a5; }
.alert.success { background: rgba(16,185,129,.1); border: 1px solid rgba(16,185,129,.3); color: #6ee7b7; }

/* ---- FOOTER ---- */
.app-footer {
  border-top: 1px solid var(--border); padding: 1.25rem 2rem;
  display: flex; justify-content: space-between;
  color: var(--text-muted); font-size: 12px; margin-top: 2rem;
}

/* ---- LINKS ---- */
a { color: var(--blue-light); text-decoration: none; }
a:hover { color: #93c5fd; }

/* ---- RESPONSIVE ---- */
@media (max-width: 900px) {
  .hero, .about-grid { grid-template-columns: 1fr; }
  .stats-row { grid-template-columns: repeat(2,1fr); }
}
@media (max-width: 600px) {
  .app-nav { padding: .75rem 1rem; flex-wrap: wrap; gap: 8px; }
  .app-wrap { padding: 0 1rem 2rem; }
  .hero-headline { font-size: 1.8rem; }
  .hero { padding: 1.5rem 0 1rem; }
}
"""

with open("static/css/styles.css", "w", encoding="utf-8") as f:
    f.write(css)
print("CSS written:", len(css), "chars")
