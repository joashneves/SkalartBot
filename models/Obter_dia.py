from models.db import _Sessao, DiaGuarda
from datetime import datetime

class Manipular_dia:
    @staticmethod
    def registrar_bomdia(id_discord: str):
        with _Sessao() as sessao:
            usuario = sessao.query(DiaGuarda).filter_by(id_discord=id_discord).first()
            if usuario:
                usuario.bomdia += 1
                usuario.bomdia_data = datetime.now()
                sessao.commit()
            else:
                novo_usuario = DiaGuarda(id_discord=id_discord, bomdia=1, bomdia_data=datetime.now(), boanoite=0, boanoite_data=datetime.now())
                sessao.add(novo_usuario)
                sessao.commit()

    @staticmethod
    def registrar_boanoite(id_discord: str):
        with _Sessao() as sessao:
            usuario = sessao.query(DiaGuarda).filter_by(id_discord=id_discord).first()
            if usuario:
                usuario.boanoite += 1
                usuario.boanoite_data = datetime.now()
                sessao.commit()
            else:
                novo_usuario = DiaGuarda(id_discord=id_discord, bomdia=0, bomdia_data=datetime.now(), boanoite=1, boanoite_data=datetime.now())
                sessao.add(novo_usuario)
                sessao.commit()

    @staticmethod
    def obter_bomdia(id_discord: str):
        with _Sessao() as sessao:
            usuario = sessao.query(DiaGuarda).filter_by(id_discord=id_discord).first()
            if usuario:
                return {
                    "numero_bomdia": usuario.bomdia,
                    "data_bomdia": usuario.bomdia_data
                }
            return None  # Retorna None caso o usuário não exista

    @staticmethod
    def obter_boanoite(id_discord: str):
        with _Sessao() as sessao:
            usuario = sessao.query(DiaGuarda).filter_by(id_discord=id_discord).first()
            if usuario:
                return {
                    "numero_boanoite": usuario.boanoite,
                    "data_boanoite": usuario.boanoite_data
                }
            return None  # Retorna None caso o usuário não exista
