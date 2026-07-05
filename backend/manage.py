#!/usr/bin/env python
"""CLI de gerenciamento — semelhante ao manage.py do Django.

Uso:
    python manage.py createuser
"""

import sys


def createuser():
    import getpass

    from sqlalchemy.exc import IntegrityError

    from auth import hash_password
    from database import Base, SessionLocal, engine
    import models  # garante que User/Task estão registrados no Base
    import uploader  # garante que Image está registrado no Base

    Base.metadata.create_all(bind=engine)

    print("=== Criar usuário ===")
    email = input("Email: ").strip()
    if not email:
        print("Erro: email não pode ser vazio.")
        sys.exit(1)

    password = getpass.getpass("Senha: ")
    if not password:
        print("Erro: senha não pode ser vazia.")
        sys.exit(1)

    confirm = getpass.getpass("Confirme a senha: ")
    if password != confirm:
        print("Erro: as senhas não coincidem.")
        sys.exit(1)

    db = SessionLocal()
    try:
        user = models.User(email=email, hashed_password=hash_password(password))
        db.add(user)
        db.commit()
        db.refresh(user)
        print(f"Usuário criado com sucesso! (id={user.id}, email={user.email})")
    except IntegrityError:
        db.rollback()
        print(f"Erro: já existe um usuário com o email '{email}'.")
        sys.exit(1)
    finally:
        db.close()


COMMANDS = {
    "createuser": createuser,
}

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(f"Uso: python manage.py <comando>")
        print(f"Comandos disponíveis: {', '.join(COMMANDS)}")
        sys.exit(1)

    command = sys.argv[1]
    if command not in COMMANDS:
        print(f"Comando desconhecido: '{command}'")
        print(f"Comandos disponíveis: {', '.join(COMMANDS)}")
        sys.exit(1)

    COMMANDS[command]()
