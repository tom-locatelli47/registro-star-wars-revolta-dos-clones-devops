from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session, joinedload

import models
import schemas
import uploader
from database import Base, engine, get_db
from uploader import MEDIA_DIR, router as upload_router
from users import router as users_router

ANONYMOUS_EMAIL = "anonymous@local"


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Both models (Task and Image) are registered with Base because uploader
    # is imported above — create_all picks them both up.
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(title="Registro de Atividades API", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origin_regex=r"^(null|http://localhost(:\d+)?|http://127\.0\.0\.1(:\d+)?)$",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(upload_router)
app.include_router(users_router)
app.mount("/media", StaticFiles(directory=str(MEDIA_DIR)), name="media")


def get_or_create_anonymous_user(db: Session) -> models.User:
    user = db.query(models.User).filter(models.User.email == ANONYMOUS_EMAIL).first()
    if user is None:
        user = models.User(email=ANONYMOUS_EMAIL, hashed_password="anonymous")
        db.add(user)
        db.commit()
        db.refresh(user)
    return user


@app.get("/tasks", response_model=list[schemas.TaskOut])
def list_tasks(
    db: Session = Depends(get_db),
):
    current_user = get_or_create_anonymous_user(db)
    return (
        db.query(models.Task)
        .options(joinedload(models.Task.img))
        .filter(models.Task.user_id == current_user.id)
        .order_by(models.Task.id)
        .all()
    )


@app.post("/tasks", response_model=schemas.TaskOut, status_code=201)
def create_task(
    task: schemas.TaskCreate,
    db: Session = Depends(get_db),
):
    current_user = get_or_create_anonymous_user(db)
    db_task = models.Task(title=task.title, done=False, user_id=current_user.id)
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task


@app.patch("/tasks/{task_id}", response_model=schemas.TaskOut)
def update_task(
    task_id: int,
    task: schemas.TaskUpdate,
    db: Session = Depends(get_db),
):
    current_user = get_or_create_anonymous_user(db)
    db_task = (
        db.query(models.Task)
        .options(joinedload(models.Task.img))
        .filter(models.Task.id == task_id, models.Task.user_id == current_user.id)
        .first()
    )
    if not db_task:
        raise HTTPException(status_code=404, detail="Tarefa não encontrada")
    if task.title is not None:
        db_task.title = task.title
    if task.done is not None:
        db_task.done = task.done
    if task.img_attachment_key is not None:
        image = (
            db.query(uploader.Image)
            .filter(uploader.Image.attachment_key == str(task.img_attachment_key))
            .first()
        )
        if not image:
            raise HTTPException(status_code=404, detail="Imagem não encontrada")
        db_task.img_id = image.id
        db_task.img = image
    db.commit()
    db.refresh(db_task)
    return db_task


@app.delete("/tasks/{task_id}", status_code=204)
def delete_task(
    task_id: int,
    db: Session = Depends(get_db),
):
    current_user = get_or_create_anonymous_user(db)
    db_task = (
        db.query(models.Task)
        .filter(models.Task.id == task_id, models.Task.user_id == current_user.id)
        .first()
    )
    if not db_task:
        raise HTTPException(status_code=404, detail="Tarefa não encontrada!!!!")
    db.delete(db_task)
    db.commit()
