from .extensions import db
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, Text
from flask_login import UserMixin


class Comment(db.Model):
    """table containing comments. Every comment is linked to one User
    """
    __tablename__ = "comment"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    author_id: Mapped[int] = mapped_column(Integer, db.ForeignKey("users.id"))
    author = relationship("User", back_populates="comments")

    created_on: Mapped[str] = mapped_column(String(250), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)


class User(UserMixin, db.Model):
    """table containing users. Every user can be linked to multiple comments
    """
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    email: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(100), nullable=False)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    profile_pic: Mapped[str] = mapped_column(String(100), nullable=False)
    comments = relationship("Comment", back_populates="author")
