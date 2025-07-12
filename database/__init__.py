from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from models import Base, quiz, user


# cria a engine
engine = create_engine('sqlite:///database/database.db')
# cria o banco
Base.metadata.create_all(bind=engine)
# cria uma sessão para a manipulação dos dados
session = Session(bind=engine)