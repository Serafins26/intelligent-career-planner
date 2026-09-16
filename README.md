# Intelligent Career Planner

Uma plataforma web para organizar seu desenvolvimento profissional — estudos, projetos, certificações e metas de carreira — tudo em um só lugar.

## Visão Geral

Este projeto nasceu da necessidade de organizar informações relacionadas ao desenvolvimento profissional, centralizando estudos, projetos, certificações e metas em um único lugar.

O objetivo é disponibilizar uma base que possa ser utilizada e adaptada por qualquer profissional de tecnologia — seja você Desenvolvedor RPA, Analista de Dados, Engenheiro de IA, especialista em Governança de TI, engenheiro de infraestrutura ou estudante.

## Funcionalidades

- **Planejador de Tarefas** — Crie e acompanhe objetivos de estudo com área, prioridade, prazos e estimativas de tempo
- **Revisão Semanal** — Planeje sua semana com tarefas focadas e registro diário
- **Gestão de Projetos** — Acompanhe projetos pessoais e corporativos com progresso, stack técnica, links de evidências e métricas de FTE
- **Dashboard de Competências** — Organize competências técnicas por categoria (RPA, Cloud, IA, Integrações, etc.)
- **Gerenciador de Certificados** — Registre certificações com emissor, datas, IDs de credencial e links de validação do LinkedIn
- **Gerador de Currículo** — Página de currículo auto-gerada (HTML + PDF) obtendo dados do banco de dados e de `data/resume.json`
- **Modo Admin** — Edição protegida por login com modo visualização/recrutador que oculta dados sensíveis (LGPD/NDA)
- **Backup & Restauração** — Exportar/importar todos os dados como JSON

## Tecnologias

| Camada | Stack |
|--------|-------|
| Backend | Python 3.11+, Flask 3, Flask-SQLAlchemy, Flask-Migrate |
| Banco de Dados | SQLite (baseado em arquivo, zero configuração) |
| Frontend | Templates Jinja2, CSS vanilla, JS vanilla |
| PDF | WeasyPrint (opcional, fallback para impressão do navegador) |
| Hospedagem | Render (ou qualquer host WSGI) |
| Servidor | Gunicorn |

## Instalação

```bash
# Clone o repositório
git clone https://github.com/seu-usuario/intelligent-career-planner.git
cd intelligent-career-planner

# Crie um ambiente virtual
python -m venv venv
source venv/bin/activate   # Linux/Mac
venv\\Scripts\\activate      # Windows

# Instale as dependências
pip install -r requirements.txt

# Execute a aplicação
python app.py
```

A aplicação inicia em `http://localhost:5000`. Na primeira execução, o banco de dados é criado automaticamente com dados de demonstração.

### Acesso Admin

Navegue para `/admin?key=admin2026` para ativar o modo admin (editar, adicionar, excluir dados).

Defina a variável de ambiente `ADMIN_KEY` para alterar a chave padrão:

```bash
export ADMIN_KEY=sua-chave-secreta
```

### Variáveis de Ambiente

| Variável | Padrão | Descrição |
|----------|--------|-----------|
| `SECRET_KEY` | `dev-secret-change-me` | Chave secreta da sessão Flask |
| `ADMIN_KEY` | `admin2026` | Chave de login do admin |
| `DATABASE_URL` | `sqlite:///data/app.db` | URI do banco de dados |

## Estrutura do Projeto

```
intelligent-career-planner/
├── app/
│   ├── __init__.py        # Application factory + dados seed
│   ├── config.py          # Configuração (variáveis de ambiente, caminhos)
│   ├── models.py          # Modelos SQLAlchemy (Task, Project, SkillCategory, Certificate)
│   └── routes.py          # Todas as rotas, lógica CRUD, cálculo de estatísticas
├── templates/             # Templates HTML Jinja2
│   ├── base.html          # Layout com navbar, abas, rodapé
│   ├── about.html         # Página de boas-vindas / dashboard
│   ├── planner.html       # Planejador de tarefas
│   ├── weekly.html        # Revisão semanal
│   ├── projects.html      # Lista de projetos + formulário de adição
│   ├── project_detail.html # Detalhe do projeto com evidências
│   ├── skills.html        # Dashboard de competências
│   ├── certificates.html  # Gerenciador de certificados
│   ├── resume.html        # Página de currículo / CV
│   └── edit_*.html        # Formulários de edição
├── static/
│   ├── css/styles.css     # Sistema de design completo (tema escuro)
│   └── js/main.js         # Interações do lado do cliente
├── data/
│   ├── app.db             # Banco de dados SQLite (criado automaticamente)
│   └── resume.json        # Dados extras do currículo (experiência, educação)
├── app.py                 # Ponto de entrada de desenvolvimento
├── wsgi.py                # Ponto de entrada de produção (Gunicorn)
├── render.yaml            # Configuração de deploy no Render.com
└── requirements.txt       # Dependências Python
```

## Personalização

### Seus Dados de Currículo

Edite `data/resume.json` com suas informações pessoais:

```json
{
  "name": "Seu Nome",
  "headline": "Seu Título | Sua Especialidade",
  "location": "Cidade, País",
  "email": "voce@email.com",
  "linkedin": "https://linkedin.com/in/seuperfil",
  "summary": "Seu resumo profissional...",
  "keywords": ["Python", "RPA", "IA"],
  "experience": [...],
  "education": [...]
}
```

### Categorias de Competências

Adicione categorias de competências pela interface admin ou edite os dados seed em `app/__init__.py`.

### Marca

Atualize `templates/base.html` para alterar o nome da aplicação e o slogan.

## Roadmap

- [ ] Alternância de tema escuro/claro
- [ ] Suporte multi-idioma (i18n)
- [ ] Gráficos no dashboard (progresso ao longo do tempo)
- [ ] Exportar currículo para DOCX
- [ ] Endpoints de API para integrações externas
- [ ] Registro de usuários (multi-tenant)
- [ ] Melhorias de responsividade mobile
- [ ] Sistema de notificações para prazos

## Contribuindo

Contribuições são bem-vindas! Fique à vontade para abrir issues ou enviar pull requests.

1. Faça um fork do repositório
2. Crie sua branch de funcionalidade (`git checkout -b feature/funcionalidade-incrivel`)
3. Commit suas mudanças (`git commit -m 'Adiciona funcionalidade incrível'`)
4. Push para a branch (`git push origin feature/funcionalidade-incrivel`)
5. Abra um Pull Request

## Licença

Este projeto está licenciado sob a Licença MIT — veja o arquivo [LICENSE](LICENSE) para detalhes.