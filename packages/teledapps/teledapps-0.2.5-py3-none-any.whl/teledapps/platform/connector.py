from web3 import Web3
from attrdict import AttrDict
from telegram.ext import CallbackContext
from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)

import os

from ..actions import Command
from ..utils import logger


class LocalConnector:
    def __init__(self):
        self.active_account = [
            os.environ.get('TELEDAPPS_ACCOUNT_ADDRESS', '0xbe0eb53f46cd790cd13851d5eff43d12404d33e8'),
            os.environ.get('TELEDAPPS_ACCOUNT_LABEL', 'Test account')
        ]

        self.passport = None
        self.bot = None
        self.callback_data = None

    def get_active_account(self, user_id):
        return self.active_account

    @property
    def web3(self):
        rpc = os.environ.get('TELEDAPPS_WEB3_RPC')

        if rpc is None:
            raise Exception('For local run, specify Web3 RPC in TELEDAPPS_WEB3_RPC')

        return Web3(Web3.HTTPProvider(rpc))

    @property
    def stages(self):
        return AttrDict({
            'basic': 0
        })

    def register_bot(self, passport, bot):
        self.passport = passport
        self.bot = bot

    def run(self):
        token = os.environ.get('TELEDAPPS_BOT_TOKEN')

        if token is None:
            raise Exception('For local run, specify Telegram bot token in TELEDAPPS_BOT_TOKEN')

        # Add simple entry point
        @self.bot.entry_point(action=Command('start'))
        def handle(update: Update, context: CallbackContext):
            keyboard = [
                [
                    InlineKeyboardButton(f'{self.passport.name}', callback_data=self.bot_inline_id)
                ]
            ]

            update.message.reply_text(
                f'Testing Teledapps bot locally. Categories - {",".join(self.passport.categories)}',
                reply_markup=InlineKeyboardMarkup(keyboard)
            )

            return self.stages.basic

        self.bot.setup(token)

        logger.info('Starting bot locally')
        self.bot.run()

    @property
    def bot_default_keyboard(self):
        return []

    @property
    def bot_inline_id(self):
        return 'dapp-111'
