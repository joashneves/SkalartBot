from sqlalchemy import create_engine, Column, String, Integer, ForeignKey, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker

engine = create_engine('sqlite:///dados.db')
Base = declarative_base()
_Sessao = sessionmaker(engine)

class Usuario(Base):
    __tablename__ = 'Usuario'
    id = Column(Integer, primary_key=True)
    id_discord = Column(String)
    apelido = Column(String, default='apelido')
    usuario = Column(String, default='usuario')
    rede_social = Column(String, default='url')
    descricao = Column(String, default='descrição')
    pronome = Column(String, default='N/a')
    caminho_arquivo = Column(String, nullable=True)
    level = Column(Integer, default=0)
    xp = Column(Integer, default=0)
    saldo = Column(Integer, default=0)
    data_criacao = Column(Integer, default=0)

class ServidorConfig(Base):
    __tablename__ = 'servidorConfig'
    id = Column(Integer, primary_key=True, index=True)
    guild_id = Column(String, nullable=False, index=True)
    channel_id = Column(String, nullable=False, index=True)

class AvatarSalvo(Base):
    __tablename__ = 'AvataresDiscord'
    id = Column(Integer, primary_key=True)
    id_discord = Column(String, nullable=False)
    caminho_arquivo = Column(String, nullable=False)
    hash_avatar = Column(String, nullable=False)
    data_arquivo = Column(DateTime, nullable=False)

class CargosSalvos(Base):
    __tablename__ = 'cargosSalvos'
    id = Column(Integer, primary_key=True, index=True)
    guild_id = Column(String, nullable=True)
    cargo_id = Column(String, nullable=True)

Base.metadata.create_all(engine)
