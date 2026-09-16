"""
Migração manual para adicionar project_type e fte_hours à tabela projects.
Execute: python migrate_project_fields.py
"""
import sqlite3
from pathlib import Path

db_path = Path("data/app.db")

if not db_path.exists():
    print(f"ERRO: Banco {db_path} nao encontrado.")
    exit(1)

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

try:
    # Verifica se as colunas já existem
    cursor.execute("PRAGMA table_info(projects)")
    columns = [col[1] for col in cursor.fetchall()]
    
    if "project_type" not in columns:
        print("Adicionando coluna project_type...")
        cursor.execute("ALTER TABLE projects ADD COLUMN project_type VARCHAR(20) NOT NULL DEFAULT 'Pessoal'")
        print("OK - Coluna project_type adicionada.")
    else:
        print("Coluna project_type ja existe.")
    
    if "fte_hours" not in columns:
        print("Adicionando coluna fte_hours...")
        cursor.execute("ALTER TABLE projects ADD COLUMN fte_hours INTEGER")
        print("OK - Coluna fte_hours adicionada.")
    else:
        print("Coluna fte_hours ja existe.")
    
    conn.commit()
    print("\nMigracao concluida com sucesso!")
    
except Exception as e:
    conn.rollback()
    print(f"\nERRO na migracao: {e}")
    
finally:
    conn.close()
