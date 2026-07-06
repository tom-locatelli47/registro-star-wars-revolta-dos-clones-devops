# ⚔️ Registro Star Wars — Revolta dos Clones

Projeto desenvolvido para a disciplina **Fundamentos de DevOps**.

Uma aplicação de **registro de atividades (tarefas)** construída com **Python (FastAPI)** no backend e **HTML/CSS/JS puro** no frontend, com upload de imagens e autenticação, empacotada e implantada em um cluster **Kubernetes (K3s)** na AWS através de um pipeline **GitOps** completo.

---

## 🚀 Visão Geral

Este repositório contém o código da aplicação e demonstra uma esteira DevOps completa, incluindo:

- **Terraform** — provisionamento da infraestrutura (EC2 na AWS)
- **Ansible** — configuração dos servidores e instalação das dependências
- **Kubernetes (K3s)** — cluster com 1 control plane + 3 workers
- **Docker** — build e publicação da imagem da API
- **ArgoCD (GitOps)** — sincronização automática do deploy
- **PostgreSQL** — banco de dados da aplicação
- **GitHub Actions** — pipeline de CI/CD

Toda a infraestrutura é provisionada automaticamente e a aplicação é implantada de ponta a ponta seguindo práticas de GitOps.

---

## 🏗️ Arquitetura

```
AWS
 │
 ├── Terraform            → provisiona as instâncias EC2
 │
 ├── Ansible               → configura os nós (usuários, SSH, dependências)
 │
 └── Cluster K3s
      ├── Control Plane
      ├── Worker 1
      ├── Worker 2
      └── Worker 3
           │
           ▼
        ArgoCD
           │
           ▼
   ┌───────┴────────┐
   │                │
Backend (API)   PostgreSQL
   │
Frontend (HTML/JS)
```

---

## 📁 Estrutura do Repositório

```
backend/            # API em FastAPI (Python)
  main.py           #   rotas de tarefas (tasks)
  models.py         #   modelos SQLAlchemy (User, Task, Image)
  database.py       #   conexão com o PostgreSQL
  auth.py           #   autenticação
  users.py          #   rotas de usuário
  uploader.py       #   upload/serving de imagens (media)
  Dockerfile        #   imagem da API
  docker-compose.yml#   API + Postgres para rodar localmente
  requirements.txt  #   dependências Python
frontend/
  index.html        # SPA simples (HTML + CSS + JS puro) que consome a API
.github/workflows/
  ci-cd.yml         # pipeline de CI/CD (testes → build → push → bump no GitOps)
README.md           # Esta documentação
```

---

## 🚢 Infraestrutura, Kubernetes e Deploy Contínuo (DevOps)

Este projeto vai além do código da aplicação: inclui provisionamento automatizado em nuvem, cluster Kubernetes e deploy via GitOps.

- **Provisionamento (Terraform + Ansible):** cria um cluster **K3s** (1 control plane + 3 workers) na AWS e prepara os nós para receber o Kubernetes.
- **Manifests / GitOps:** repositório separado [`ARGO-DEVOPS-3`](https://github.com/tom-locatelli47/ARGO-DEVOPS-3) (Kustomize + ArgoCD).
- **CI/CD:** GitHub Actions em [`.github/workflows/ci-cd.yml`](.github/workflows/ci-cd.yml) — testa, builda e publica a imagem da API no Docker Hub e atualiza a tag da imagem no repositório GitOps; o ArgoCD sincroniza o cluster automaticamente.

Fluxo resumido:

```
git push → GitHub Actions (testes → build → Docker Hub → bump da tag no GitOps) → ArgoCD → K3s
```

---

## 🛠 Tecnologias Utilizadas

- **Backend:** Python 3.14, FastAPI, SQLAlchemy, Psycopg, Uvicorn
- **Banco de dados:** PostgreSQL 17
- **Frontend:** HTML5, CSS3, JavaScript (vanilla)
- **Infraestrutura:** Terraform, Ansible, AWS EC2
- **Orquestração:** Kubernetes (K3s), Kustomize
- **GitOps:** ArgoCD
- **CI/CD:** GitHub Actions, Docker Hub

---

## 💻 Como Rodar Localmente

### Pré-requisitos

- Python 3.13+ e pip
- Docker e Docker Compose
- Git

### 1. Clonar o repositório

```bash
git clone https://github.com/tom-locatelli47/registro-star-wars-revolta-dos-clones-devops.git
cd registro-star-wars-revolta-dos-clones-devops
```

### 2. Subir a API e o banco de dados (Docker Compose)

```bash
cd backend
docker compose up --build
```

A API ficará disponível em `http://localhost:8001`.

> Alternativamente, é possível rodar a API sem Docker: crie um ambiente virtual, instale as dependências com `pip install -r requirements.txt` e execute `uvicorn main:app --reload --port 8001`, apontando a variável `DATABASE_URL` para um PostgreSQL local.

### 3. Abrir o frontend

Basta abrir o arquivo `frontend/index.html` no navegador (ou servi-lo com qualquer servidor estático). Ele consome a API configurada em `http://localhost:8001`.

---

## 🌐 API

A API é construída com FastAPI e expõe endpoints REST para:

- `GET /tasks` — lista as tarefas do usuário
- `POST /tasks` — cria uma nova tarefa
- `PATCH /tasks/{task_id}` — atualiza título, status ou imagem de uma tarefa
- `DELETE /tasks/{task_id}` — remove uma tarefa
- Upload e serving de imagens em `/media`
- Rotas de usuário/autenticação

---

## 🔁 Fluxo CD Ponta-a-Ponta

1. Push na branch `main` deste repositório → GitHub Actions roda os testes.
2. Workflow builda e publica a imagem `tomaslocatelli/registro-star-wars-revolta-dos-clones-devops:<sha>` no Docker Hub.
3. Workflow faz commit no repositório GitOps ([`ARGO-DEVOPS-3`](https://github.com/tom-locatelli47/ARGO-DEVOPS-3)) atualizando a tag da imagem via Kustomize.
4. ArgoCD detecta o commit e sincroniza automaticamente o cluster K3s.

---

## 📦 Organização dos Repositórios

| Repositório | Função |
| --- | --- |
| [`registro-star-wars-revolta-dos-clones-devops`](https://github.com/tom-locatelli47/registro-star-wars-revolta-dos-clones-devops) | Código da aplicação (backend + frontend) e pipeline de CI |
| [`ARGO-DEVOPS-3`](https://github.com/tom-locatelli47/ARGO-DEVOPS-3) | Manifests Kubernetes/Kustomize, IaC (Terraform + Ansible) e ArgoCD (GitOps) |

---

## 👤 Autor

**Tomas Locatelli**
Disciplina: Fundamentos de DevOps
