from models.db import _Sessao, Usuario

class Manipular_Usuario:
    def obter_usuario(id_discord: str):
        with _Sessao() as sessao:
            usuario = sessao.query(Usuario).filter_by(id_discord=id_discord).first()
            if not usuario:
                print(f"Usuário não existe.")
                return
            return usuario

    def atualizar_usuario(id_discord: int, apelido: str, descricao: str, rede_social:str ,pronome: str = "N/a"):
        with _Sessao() as sessao:
            usuario = sessao.query(Usuario).filter_by(id_discord=id_discord).first()
            if usuario:
                usuario.apelido = apelido
                usuario.descricao = descricao
                usuario.rede_social = rede_social or usuario.rede_social
                usuario.pronome = pronome or usuario.pronome
                print(f"Usuário {id_discord} atualizado com sucesso.")
                return usuario
            return "Usuario não existe"

    def criar_usuario(id_discord: int, apelido: str, descricao: str, rede_social:str ,pronome: str = "N/a"):
        with _Sessao() as sessao:
            usuario = sessao.query(Usuario).filter_by(id_discord=id_discord).first()
            if not usuario:
                usuario = Usuario(
                        id_discord=id_discord,
                        apelido=apelido,
                        rede_social=rede_social,
                        descricao=descricao,
                        pronome=pronome
                )
                sessao.add(usuario)
                print(f"Usuário {id_discord} registrado com sucesso.")
                sessao.commit()
                return usuario
            return "Usuario ja existe"
