from .connector import SimpleConnector


class Platform:
    def __init__(self):
        self.connector = SimpleConnector()

    def get_active_account(self, user_id):
        return self.connector.get_active_account(user_id)

    @property
    def web3(self):
        return self.connector.web3

    def register_bot(self, passport, bot):
        pass
