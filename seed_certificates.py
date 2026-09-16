# =============================================================================
# seed_certificates.py — CARGA INICIAL DE CERTIFICADOS
# =============================================================================
# Execute UMA VEZ para inserir todos os certificados:
#   python seed_certificates.py
#
# O script apaga os certificados existentes e insere os novos.
# Execute com o servidor Flask PARADO para evitar conflitos.
# =============================================================================

import datetime
from app import create_app, db
from app.models import Certificate

app = create_app()

with app.app_context():

    # Remove certificados anteriores
    Certificate.query.delete()
    db.session.commit()
    print("Certificados anteriores removidos.")

    # -----------------------------------------------------------------
    # Lista de certificados extraídos do LinkedIn
    # Formato: (nome, emissor, área, data_emissão, data_validade,
    #           linkedin_url, credential_url, credential_id, destaque)
    # -----------------------------------------------------------------
    certificados = [
        # === Git / Banco de Dados ===
        (
            "Git e GitHub para Iniciantes com Projetos Reais",
            "Udemy",
            "Geral",
            datetime.date(2026, 7, 1),
            None, "", "", "", False,
        ),
        (
            "Banco de Dados SQL do Zero ao Avançado + Projetos Reais",
            "Udemy",
            "Geral",
            datetime.date(2026, 7, 1),
            None, "", "", "", False,
        ),
        # === Cloud / Dados ===
        (
            "Arquitetura de Dados para Engenharia e Ciência de Dados",
            "Udemy",
            "Cloud",
            datetime.date(2026, 7, 1),
            None, "", "", "", True,
        ),
        (
            "Introdução à Governança de Dados",
            "LinkedIn",
            "Geral",
            datetime.date(2026, 7, 1),
            None, "", "", "", False,
        ),
        # === Gestão de Riscos ===
        (
            "ISO 31000:2018 & ISO 31010:2019 - Gestão de Riscos e Técnicas para Avaliação",
            "Interaction Plexus",
            "Geral",
            datetime.date(2024, 11, 1),
            None, "", "", "1733135047462", False,
        ),
        # === Power Platform / RPA ===
        (
            "Power Automate",
            "Mundo Power",
            "APIs e Integrações",
            datetime.date(2024, 6, 1),
            None, "", "", "1719340321722x265689289076768770", True,
        ),
        (
            "Introdução à Power Platform",
            "RonanVico",
            "APIs e Integrações",
            datetime.date(2024, 10, 1),
            None, "", "", "", False,
        ),
        # === Gestão de Projetos (Google / Coursera) ===
        (
            "Planejamento de Projetos: Como reunir tudo - Google",
            "Coursera",
            "Geral",
            datetime.date(2024, 2, 1),
            None, "", "", "BN2P2NHG85TE", False,
        ),
        (
            "Início do projeto: Como começar um projeto bem-sucedido - Google",
            "Coursera",
            "Geral",
            datetime.date(2023, 11, 1),
            None, "", "", "FDYNBUK3PAVF", False,
        ),
        (
            "Fundamentos do gerenciamento de projetos - Google",
            "Coursera",
            "Geral",
            datetime.date(2023, 9, 1),
            None, "", "", "ZUDJSHU9QE6K", False,
        ),
        # === Power BI ===
        (
            "Master Power BI - De A à Z",
            "Udemy",
            "APIs e Integrações",
            datetime.date(2024, 3, 1),
            None, "", "", "UC-8c44cd1e-59ed-4abb-8344-05567859b6e2", True,
        ),
        # === LinkedIn Learning ===
        (
            "Gerenciamento de Cronogramas de Projetos",
            "LinkedIn",
            "Geral",
            datetime.date(2023, 6, 1),
            None, "", "", "", False,
        ),
        (
            "Competências Básicas de Gestão de Projetos",
            "LinkedIn",
            "Geral",
            datetime.date(2022, 8, 1),
            None, "", "", "", False,
        ),
        # === BPMN ===
        (
            "Mapeamento de Processos com BPMN 2.0",
            "iProcess",
            "Geral",
            datetime.date(2023, 6, 1),
            None, "", "", "", False,
        ),
        # === IT Governance ===
        (
            "Formação IT Governance Specialist - Site Campus",
            "Udemy",
            "Geral",
            datetime.date(2022, 10, 1),
            None, "", "", "", False,
        ),
        # === UiPath ===
        (
            "RPA Developer Foundation (v2020.10)",
            "UiPath",
            "UiPath",
            datetime.date(2022, 7, 1),
            None, "", "", "", True,
        ),
        # === Cloud / Microsoft ===
        (
            "SC-900 - Microsoft Security, Compliance and Identity Fundamentals",
            "Green Tecnologia",
            "Cloud",
            datetime.date(2021, 7, 1),
            None, "", "", "", True,
        ),
        (
            "MS-900 - Microsoft 365 Fundamentals",
            "Green Tecnologia",
            "Cloud",
            datetime.date(2021, 7, 1),
            None, "", "", "", True,
        ),
        (
            "AZ-900 - Microsoft Azure Fundamentals",
            "Green Tecnologia",
            "Cloud",
            datetime.date(2021, 7, 1),
            None, "", "", "", True,
        ),
        # === MySQL ===
        (
            "MySQL - Básico",
            "Curso em Vídeo",
            "Geral",
            datetime.date(2022, 3, 1),
            None, "", "", "", False,
        ),
        # === Redes ===
        (
            "Técnico em Redes de Computadores",
            "Etec Prof. Horácio Augusto da Silveira",
            "Geral",
            datetime.date(2015, 6, 1),
            None, "", "", "", False,
        ),
    ]

    for (name, issuer, area, issued, expiry,
         linkedin_url, credential_url, credential_id, featured) in certificados:
        db.session.add(Certificate(
            name=name,
            issuer=issuer,
            area=area,
            issued_date=issued,
            expiry_date=expiry,
            linkedin_url=linkedin_url,
            credential_url=credential_url,
            credential_id=credential_id,
            featured=featured,
        ))

    db.session.commit()
    print(f"✅ {len(certificados)} certificados inseridos com sucesso.")

    # Resumo
    areas = {}
    for c in certificados:
        areas[c[2]] = areas.get(c[2], 0) + 1
    print("\nDistribuição por área:")
    for area, count in sorted(areas.items()):
        print(f"  {area}: {count}")

    destaques = sum(1 for c in certificados if c[8])
    print(f"\n⭐ {destaques} em destaque")
