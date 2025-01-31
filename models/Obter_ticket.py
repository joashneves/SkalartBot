from models.db import _Sessao, TicketConfig


class Manipular_Ticket:
    @staticmethod
    def obter_config(guild_id: str):
        """Obtém a configuração de ticket de um servidor."""
        with _Sessao() as sessao:
            config = sessao.query(TicketConfig).filter_by(guild_id=guild_id).first()
            return config

    @staticmethod
    def adicionar_config(guild_id: str, categoria_id: str, cargo_id: str):
        """Adiciona ou atualiza a configuração de ticket de um servidor."""
        with _Sessao() as sessao:
            config = sessao.query(TicketConfig).filter_by(guild_id=guild_id).first()
            if config:
                config.categoria_id = categoria_id
                config.cargo_id = cargo_id
            else:
                config = TicketConfig(
                    guild_id=guild_id, categoria_id=categoria_id, cargo_id=cargo_id
                )
                sessao.add(config)
            sessao.commit()
            return config

    @staticmethod
    def remover_config(guild_id: str):
        """Remove a configuração de ticket de um servidor."""
        with _Sessao() as sessao:
            config = sessao.query(TicketConfig).filter_by(guild_id=guild_id).first()
            if config:
                sessao.delete(config)
                sessao.commit()
                return True
            return False
