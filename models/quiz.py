from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from sqlalchemy.types import JSON
from typing import List
from models import Base


class Pergunta(Base):
    __tablename__ = 'perguntas'
    id:Mapped[int] = mapped_column(primary_key=True)
    titulo:Mapped[str]
    opcoes:Mapped[List[str]] = mapped_column(JSON)
    resposta:Mapped[int]

    quiz_id: Mapped[int] = mapped_column(ForeignKey('quiz.id'))
    quiz: Mapped["Quiz_tb"] = relationship(back_populates="perguntas")
    

class Quiz_tb(Base):
    __tablename__ = 'quiz'
    id:Mapped[int] = mapped_column(primary_key=True)
    perguntas: Mapped[List["Pergunta"]] = relationship(back_populates="quiz")