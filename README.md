# registro-star-wars-revolta-dos-clones-devops

Projeto de teste para a disciplina de Fundamentos de DevOps. O repositório foi reorganizado em duas partes:

- `backend/`: aplicação FastAPI com autenticação, tarefas e integração com PostgreSQL.
- `frontend/`: página estática para testar cadastro, login e CRUD de tarefas.

## Portas e acesso

| Componente                          | Porta          | Como acessar                                                            |
| ----------------------------------- | -------------- | ----------------------------------------------------------------------- |
| Backend FastAPI                     | `8001`         | `http://localhost:8001`                                                 |
| Documentação Swagger                | `8001`         | `http://localhost:8001/docs`                                            |
| PostgreSQL local via Docker Compose | `5433`         | `localhost:5433`                                                        |
| Frontend                            | sem porta fixa | abrir o arquivo [frontend/index.html](frontend/index.html) no navegador |

## Como testar localmente

1. Suba o backend e o banco com Docker Compose dentro da pasta `backend`.
2. Abra [frontend/index.html](frontend/index.html) no navegador.
3. No campo "API base", mantenha `http://localhost:8001`.
4. Registre um usuário, faça login e crie tarefas para validar a gravação no banco.

## Rotas principais da API

- `POST /api/users/register`
- `POST /api/token`
- `POST /api/token/refresh`
- `GET /tasks`
- `POST /tasks`
- `PATCH /tasks/{task_id}`
- `DELETE /tasks/{task_id}`

## Estrutura do repositório

- `backend/`
- `frontend/`
- `.github/workflows/`

## Observações

- O frontend foi criado para testar o banco por meio da API.
- No ambiente Kubernetes, o banco fica exposto apenas internamente pelo cluster.
- O objetivo do projeto é demonstrar backend, frontend, banco e GitOps com ArgoCD.
