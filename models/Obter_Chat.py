from models.db import _Sessao, ServidorConfig


class Manipular_Chat:
    @staticmethod
    def obter_chat(channel_id: str):
        with _Sessao() as sessao:
            chat = sessao.query(ServidorConfig).filter_by(channel_id=channel_id).first()
            if not chat:
                print(f"Chat não existe.")
                return None
            return chat

    @staticmethod
    def adicionar_chat(guild_id: str, channel_id: str):
        with _Sessao() as sessao:
            chat = sessao.query(ServidorConfig).filter_by(channel_id=channel_id).first()
            if chat:
                print(f"Chat já existe.")
                return chat
            novo_chat = ServidorConfig(guild_id=guild_id, channel_id=channel_id)
            sessao.add(novo_chat)
            sessao.commit()
            return novo_chat

    @staticmethod
    def remover_chat(channel_id: str):
        with _Sessao() as sessao:
            chat = sessao.query(ServidorConfig).filter_by(channel_id=channel_id).first()
            if chat:
                sessao.delete(chat)
                sessao.commit()
                return True
            return False

    @staticmethod
    def listar_chats(guild_id: str):
        with _Sessao() as sessao:
            chats = sessao.query(ServidorConfig).filter_by(guild_id=guild_id).all()
            return chats
