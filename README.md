# Registro Star Wars – Revolta dos Clones

Projeto desenvolvido para a disciplina **Fundamentos de DevOps**.

## Objetivo

Este projeto demonstra uma arquitetura completa utilizando práticas DevOps, incluindo:

- Terraform
- Ansible
- Kubernetes (K3s)
- Docker
- ArgoCD (GitOps)
- PostgreSQL
- Frontend
- Backend

Toda a infraestrutura é provisionada automaticamente e a aplicação é implantada utilizando GitOps.

---

# Arquitetura

AWS
│
├── Terraform
│
├── Ansible
│
└── Cluster K3s
├── Control Plane
├── Worker 1
├── Worker 2
└── Worker 3

↓

ArgoCD

↓

Frontend
Backend
PostgreSQL

---

# Tecnologias utilizadas

- Terraform
- Ansible
- Kubernetes (K3s)
- Docker
- ArgoCD
- PostgreSQL
- Traefik Ingress

---

# Estrutura do projeto

```text
.
├── ansible/
├── terraform/
├── backend/
├── frontend/
├── docker/
├── kubernetes/
└── README.md
```

---

# Provisionamento

A infraestrutura foi criada utilizando Terraform.

Após a criação das máquinas, o Ansible realiza:

- instalação do Docker
- instalação do K3s
- configuração do cluster
- instalação das dependências

---

# Cluster Kubernetes

O cluster possui:

- 1 Control Plane
- 3 Workers

Todos os nós são configurados automaticamente utilizando Ansible.

---

# GitOps

O deploy da aplicação é realizado pelo ArgoCD.

Os manifests estão disponíveis em:

https://github.com/tom-locatelli47/ARGO-DEVOPS-3

Sempre que alterações são enviadas para este repositório, o ArgoCD sincroniza automaticamente o cluster.

---

# Aplicação

A aplicação é composta por:

- Frontend
- Backend
- PostgreSQL

O Backend realiza a comunicação com o banco de dados.

O Frontend consome a API disponibilizada pelo Backend.

---

# Como reproduzir

## 1. Clonar o projeto

git clone https://github.com/tom-locatelli47/registro-star-wars-revolta-dos-clones-devops

## 2. Provisionar a infraestrutura

terraform init

terraform apply

## 3. Executar o Ansible

ansible-playbook playbook.yml

## 4. Instalar o ArgoCD

kubectl create namespace argocd

...

## 5. Criar a aplicação no ArgoCD

Apontar para:

https://github.com/tom-locatelli47/ARGO-DEVOPS-3

Sincronizar.

---

# Organização dos repositórios

Projeto principal

https://github.com/tom-locatelli47/registro-star-wars-revolta-dos-clones-devops

GitOps

https://github.com/tom-locatelli47/ARGO-DEVOPS-3

---

# Autor

Tomas Locatelli

Disciplina: Fundamentos de DevOps
