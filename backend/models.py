from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)

    tasks = relationship("Task", back_populates="user")


class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    done = Column(Boolean, default=False, nullable=False)
    img_id = Column(Integer, ForeignKey("images.id"), nullable=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    img = relationship("Image", lazy="select")
    user = relationship("User", back_populates="tasks")

    @property
    def img_url(self) -> str | None:
        return self.img.url if self.img else None
