from .connector import LocalConnector


class Platform:
    def __init__(self):
        self.connector = LocalConnector()

    def get_active_account(self, user_id):
        return self.connector.get_active_account(user_id)

    @property
    def web3(self):
        return self.connector.web3

    def register_bot(self, passport, bot):
        self.connector.register_bot(passport, bot)

    @property
    def dapp_callback_data(self):
        return self.connector.dapp_callback_data

    @property
    def stages(self):
        return self.connector.stages
