from models.db import _Sessao, CargosSalvos

class Manipular_Cargo():
    def obter_Cargo(guild_id:str):
        with _Sessao() as sessao:
            # Filtra os registros pelo guild_id fornecido
            cargos_db = sessao.query(CargosSalvos.cargo_id).filter_by(guild_id=guild_id).all()
            # Retorna uma lista de cargo_id (ou uma lista vazia se não houver registros)
            return [cargo.cargo_id for cargo in cargos_db] if cargos_db else []

    def criar_Cargo(guild_id: str, cargo_id: str):
        with _Sessao() as sessao:
            new_cargo = CargosSalvos(
                guild_id=guild_id,
                cargo_id=cargo_id
            )
            sessao.add(new_cargo)
            sessao.commit()
            return


    def verificar_chat(guild_id: str, channel_id: str) -> bool:
        with _Sessao() as sessao:
            chat = sessao.query(CargosSalvos).filter_by(
                guild_id=guild_id, channel_id=channel_id
            ).first()
            return chat is not None  # Retorna True se o chat já existir
