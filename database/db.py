from sqlalchemy import create_engine, Column, String, Integer, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker

engine = create_engine('sqlite:///dados.db')
Base = declarative_base()

class Usuario(Base):
    __tablename__ = 'Usuario'

    id = Column(Integer, primary_key=True)
    discord_id = Column(Integer)
    nome = Column(String)
    rede_social = Column(String)
    pronomes = Column(String)
    data_nascimento = Column(DateTime)

Base.metadata.create_all(engine)
