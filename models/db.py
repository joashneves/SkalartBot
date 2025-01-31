from sqlalchemy import create_engine, Column, String, Integer, ForeignKey, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker

engine = create_engine("sqlite:///dados.db")
Base = declarative_base()
_Sessao = sessionmaker(engine)


class Usuario(Base):
    __tablename__ = "Usuario"
    id = Column(Integer, primary_key=True)
    id_discord = Column(String)
    apelido = Column(String, default="apelido")
    usuario = Column(String, default="usuario")
    rede_social = Column(String, default="url")
    descricao = Column(String, default="descrição")
    pronome = Column(String, default="N/a")
    caminho_arquivo = Column(String, nullable=True)
    level = Column(Integer, default=0)
    xp = Column(Integer, default=0)
    saldo = Column(Integer, default=0)
    data_criacao = Column(Integer, default=0)


class ServidorConfig(Base):
    __tablename__ = "servidorConfig"
    id = Column(Integer, primary_key=True, index=True)
    guild_id = Column(String, nullable=False, index=True)
    channel_id = Column(String, nullable=False, index=True)


class AvatarSalvo(Base):
    __tablename__ = "AvataresDiscord"
    id = Column(Integer, primary_key=True)
    id_discord = Column(String, nullable=False)
    caminho_arquivo = Column(String, nullable=False)
    hash_avatar = Column(String, nullable=False)
    data_arquivo = Column(DateTime, nullable=False)


class CargosSalvos(Base):
    __tablename__ = "cargosSalvos"
    id = Column(Integer, primary_key=True, index=True)
    guild_id = Column(String, nullable=True)
    cargo_id = Column(String, nullable=True)


class ImagemGuarda(Base):
    __tablename__ = "imagemGuarda"
    id = Column(Integer, primary_key=True, index=True)
    id_discord = Column(String, nullable=True)
    caminho_arquivo = Column(String, nullable=True)
    descricao = Column(String, nullable=True)
    data_arquivo = Column(DateTime, nullable=False)


class DiaGuarda(Base):
    __tablename__ = "diaGuarda"
    id = Column(Integer, primary_key=True, index=True)
    id_discord = Column(String, nullable=True)
    bomdia = Column(Integer, default=0, nullable=False)
    boanoite = Column(Integer, default=0, nullable=False)
    bomdia_data = Column(DateTime, nullable=False)
    boanoite_data = Column(DateTime, nullable=False)


class FeedConfig(Base):
    __tablename__ = "feedConfig"
    id = Column(Integer, primary_key=True, index=True)
    guild_id = Column(String, nullable=False, index=True)
    channel_id = Column(String, nullable=False, index=True)


class TicketConfig(Base):
    __tablename__ = "ticket_Config"
    id = Column(Integer, primary_key=True, index=True)
    guild_id = Column(String, nullable=True)
    categoria_id = Column(String, nullable=True)
    cargo_id = Column(String, nullable=True)


Base.metadata.create_all(engine)
