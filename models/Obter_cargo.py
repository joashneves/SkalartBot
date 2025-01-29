from models.db import _Sessao, CargosSalvos

class Manipular_Cargo():
    def obter_Cargo(guild_id:str):
        with _Sessao() as sessao:
            cargos_db = sessao.query(CargosSalvos.cargo_id).filter_by(guild_id=guild_id).all()
            return [cargo.cargo_id for cargo in cargos_db] if cargos_db else []

    def criar_Cargo(guild_id: str, cargo_id: str):
        with _Sessao() as sessao:
            new_cargo = CargosSalvos(guild_id=guild_id, cargo_id=cargo_id)
            sessao.add(new_cargo)
            sessao.commit()

    def remover_Cargo(guild_id: str, cargo_id: str) -> bool:
        with _Sessao() as sessao:
            cargo = sessao.query(CargosSalvos).filter_by(
                guild_id=guild_id, cargo_id=cargo_id
            ).first()

            if cargo:
                sessao.delete(cargo)
                sessao.commit()
                return True
            return False
