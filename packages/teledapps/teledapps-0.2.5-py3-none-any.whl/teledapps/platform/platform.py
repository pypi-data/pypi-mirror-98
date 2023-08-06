import os
import importlib
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
        return self.connector.register_bot(passport, bot)

    def run(self):
        return self.connector.run()

    @property
    def stages(self):
        return self.connector.stages

    @property
    def bot_default_keyboard(self):
        return self.connector.bot_default_keyboard

    @property
    def bot_inline_id(self):
        return self.connector.bot_inline_id
