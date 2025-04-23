from flask_login import UserMixin
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass

class User(Base, UserMixin):
    __tablename__ = 'users'
    id: Mapped[int] = mapped_column(primary_key=True)
    nome: Mapped[str] = mapped_column()
    email: Mapped[str] = mapped_column(unique=True)
    senha: Mapped[str] = mapped_column()

    fase_quiz: Mapped[int] = mapped_column()
    trofeu_quiz: Mapped[int] = mapped_column()
    fase_qcbc: Mapped[int] = mapped_column()
    trofeu_qcbc: Mapped[int] = mapped_column()
    fase_trilha: Mapped[int] = mapped_column()
    trofeu_trilha: Mapped[int] = mapped_column()