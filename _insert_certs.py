"""Insere certificados direto no banco SQLite (sem Flask)."""
import sqlite3

DB = "data/app.db"
conn = sqlite3.connect(DB)
c = conn.cursor()

# Limpa certificados existentes
c.execute("DELETE FROM certificates")

certs = [
    # (name, issuer, area, issued_date, expiry_date, linkedin_url, credential_url, credential_id, featured)
    ("Git e GitHub para Iniciantes com Projetos Reais", "Udemy", "Geral", "2026-07-01", None, "", "", "", 0),
    ("Banco de Dados SQL do Zero ao Avançado + Projetos Reais", "Udemy", "Geral", "2026-07-01", None, "", "", "", 0),
    ("Arquitetura de Dados para Engenharia e Ciência de Dados", "Udemy", "Cloud", "2026-07-01", None, "", "", "", 1),
    ("Introdução à Governança de Dados", "LinkedIn", "Geral", "2026-07-01", None, "", "", "", 0),
    ("ISO 31000:2018 & ISO 31010:2019 - Gestão de Riscos e Técnicas para Avaliação", "Interaction Plexus", "Geral", "2024-11-01", None, "", "", "1733135047462", 0),
    ("Power Automate", "Mundo Power", "APIs e Integrações", "2024-06-01", None, "", "", "1719340321722x265689289076768770", 1),
    ("Introdução à Power Platform", "RonanVico", "APIs e Integrações", "2024-10-01", None, "", "", "", 0),
    ("Planejamento de Projetos: Como reunir tudo - Google", "Coursera", "Geral", "2024-02-01", None, "", "", "BN2P2NHG85TE", 0),
    ("Início do projeto: Como começar um projeto bem-sucedido - Google", "Coursera", "Geral", "2023-11-01", None, "", "", "FDYNBUK3PAVF", 0),
    ("Fundamentos do gerenciamento de projetos - Google", "Coursera", "Geral", "2023-09-01", None, "", "", "ZUDJSHU9QE6K", 0),
    ("Master Power BI - De A à Z", "Udemy", "APIs e Integrações", "2024-03-01", None, "", "", "UC-8c44cd1e-59ed-4abb-8344-05567859b6e2", 1),
    ("Gerenciamento de Cronogramas de Projetos", "LinkedIn", "Geral", "2023-06-01", None, "", "", "", 0),
    ("Competências Básicas de Gestão de Projetos", "LinkedIn", "Geral", "2022-08-01", None, "", "", "", 0),
    ("Mapeamento de Processos com BPMN 2.0", "iProcess", "Geral", "2023-06-01", None, "", "", "", 0),
    ("Formação IT Governance Specialist - Site Campus", "Udemy", "Geral", "2022-10-01", None, "", "", "", 0),
    ("RPA Developer Foundation (v2020.10)", "UiPath", "UiPath", "2022-07-01", None, "", "", "", 1),
    ("SC-900 - Microsoft Security, Compliance and Identity Fundamentals", "Green Tecnologia", "Cloud", "2021-07-01", None, "", "", "", 1),
    ("MS-900 - Microsoft 365 Fundamentals", "Green Tecnologia", "Cloud", "2021-07-01", None, "", "", "", 1),
    ("AZ-900 - Microsoft Azure Fundamentals", "Green Tecnologia", "Cloud", "2021-07-01", None, "", "", "", 1),
    ("MySQL - Básico", "Curso em Vídeo", "Geral", "2022-03-01", None, "", "", "", 0),
    ("Técnico em Redes de Computadores", "Etec Prof. Horácio Augusto da Silveira", "Geral", "2015-06-01", None, "", "", "", 0),
]

sql = """INSERT INTO certificates
    (name, issuer, area, issued_date, expiry_date, linkedin_url, credential_url, credential_id, featured)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)"""

c.executemany(sql, certs)
conn.commit()
print(f"OK - {len(certs)} certificados inseridos com sucesso.")

# Resumo
areas = {}
for cert in certs:
    a = cert[2]
    areas[a] = areas.get(a, 0) + 1
print("\nDistribuição por área:")
for area, count in sorted(areas.items()):
    print(f"  {area}: {count}")
destaques = sum(1 for cert in certs if cert[8])
print(f"\n* {destaques} em destaque")

conn.close()
