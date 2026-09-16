"""
Insere projetos no banco de dados (corporativos e do portfólio).
Executar: python seed_projects.py
"""
import sqlite3
from pathlib import Path

db_path = Path("data/app.db")
if not db_path.exists():
    print(f"ERRO: Banco {db_path} nao encontrado.")
    exit(1)

projects = [
    # ---------------------------------------------
    # Portfólio (pessoais)
    # ---------------------------------------------
    ("Intelligent Automation Portfolio Planner", "Pessoal", 0.00, "Em desenvolvimento", 40, "Portfólio"),
    ("AI Email Processor", "Pessoal", 0.00, "Em desenvolvimento", 10, "Automação + IA"),
    ("Document Intelligence", "Pessoal", 0.00, "Backlog", 0, "POC"),

    # ---------------------------------------------
    # Corporativos (existentes)
    # ---------------------------------------------
    ("Compensar documentos na conta transitória", "Financeiro", 3.70, "Concluído", 100, "Automação"),
    ("Inserir protocolo e número aleatório na nota fiscal", "Fiscal", 8.23, "Concluído", 100, "Automação"),
    ("Extrair relatório ARIN RECON Invoinet", "Financeiro", 1.23, "Concluído", 100, "Automação"),
    ("Aprovar e executar batch input", "Contabilidade", 30.86, "Concluído", 100, "Automação"),
    ("Patch Management", "TI", 2.47, "Concluído", 100, "Automação"),
    ("Compensar estorno fiscal", "Financeiro", 6.17, "Concluído", 100, "Automação"),
    ("Black List", "TI", 4.94, "Concluído", 100, "Automação"),
    ("Armazenar documentos de suporte no SAP", "Contabilidade", 51.44, "Concluído", 100, "Automação"),
    ("Enviar certificados de treinamento", "RH", 2.06, "Concluído", 100, "Automação"),
    ("Gerar PDF de nota fiscal", "Fiscal", 30.86, "Concluído", 100, "Automação"),
    ("Criar relatório para análise de adiantamento pago ao fornecedor", "Financeiro", 6.17, "Concluído", 100, "Análise de Dados"),
    ("Clean folders", "TI", 3.09, "Concluído", 100, "Automação"),
    ("Executar a saída de estoque para bulk material", "Produção", 12.35, "Concluído", 100, "Automação"),
    ("Extrair relatório SAP CBW e criar arquivo no SharePoint", "Logística", 1.03, "Concluído", 100, "Automação"),
    ("Extrair relatório SAP CSC", "Produção", 4.12, "Concluído", 100, "Automação"),
    ("Extrair relatório supplier tooling", "Compras", 0.41, "Concluído", 100, "Automação"),
    ("Executar batch input de fornecedores e clientes", "Contabilidade", 2.01, "Em desenvolvimento", 20, "Automação"),
    ("Alterar variante de execução FF_5", "Financeiro", 3.09, "Concluído", 100, "Automação"),
    ("Criar app para controle de contratos de TI", "TI", 2.06, "Concluído", 100, "Análise de Dados"),
]

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

inserted = 0
for name, area, fte, status, progress, categoria in projects:
    # Verifica duplicata
    cursor.execute("SELECT id FROM projects WHERE name = ?", (name,))
    if cursor.fetchone():
        print(f"  Ja existe: {name}")
        continue

    # Ajusta descrição/stack por tipo
    if area == "Pessoal":
        desc = "Projeto do portfólio (UiPath + IA)"
        stack = "Python, Flask, UiPath, OpenAI"
        highlight = categoria
        project_type = "Pessoal"
        fte_hours = None
    else:
        stack = "UiPath" if categoria == "Automação" else "Power Apps, SharePoint"
        desc = f"Desenvolvimento {categoria.lower()} - Area {area}"
        highlight = f"Area: {area}"
        project_type = "Corporativo"
        fte_hours = fte

    cursor.execute(
        """INSERT INTO projects
           (name, description, stack, progress, status, repo, demo, evidence, highlight, project_type, fte_hours)
           VALUES (?, ?, ?, ?, ?, '', '', '', ?, ?, ?)""",
        (name, desc, stack, progress, status, highlight, project_type, fte_hours),
    )
    inserted += 1
    print(f"  + {name} (FTE: {fte}%)")

conn.commit()
conn.close()
print(f"\n{inserted} projeto(s) inserido(s) com sucesso.")
