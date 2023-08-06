from web3 import Web3
from attrdict import AttrDict
from telegram.ext import CallbackContext
from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)

import os
import re

from ..callback_data import CallbackData
from ..actions import Command
from ..utils import logger


class LocalConnector:
    def __init__(self):
        self.active_account = [
            os.environ.get('TELEDAPPS_ACCOUNT_ADDRESS', '0xbe0eb53f46cd790cd13851d5eff43d12404d33e8'),
            os.environ.get('TELEDAPPS_ACCOUNT_LABEL', 'Test account')
        ]

    def get_active_account(self, user_id):
        return self.active_account

    @property
    def web3(self):
        rpc = os.environ.get('TELEDAPPS_WEB3_RPC')

        if rpc is None:
            raise Exception('For local run, specify Web3 RPC in TELEDAPPS_WEB3_RPC')

        return Web3(Web3.HTTPProvider(rpc))

    @property
    def dapp_callback_data(self):
        return CallbackData(
            pattern='dapp-*',
            encoder=lambda dapp_id: f'dapp-{dapp_id}',
            decoder=lambda data: int(re.search('dapp-(?P<id>.*)', data).group('id'))
        )

    @property
    def stages(self):
        return AttrDict({
            'basic': 0
        })

    def register_bot(self, passport, bot):
        token = os.environ.get('TELEDAPPS_BOT_TOKEN')

        if token is None:
            raise Exception('For local run, specify Telegram bot token in TELEDAPPS_BOT_TOKEN')

        # Add simple entry point
        @bot.entry_point(action=Command('start'))
        def handle(update: Update, context: CallbackContext):
            keyboard = [
                [
                    InlineKeyboardButton(f'{passport.name}', callback_data=self.dapp_callback_data.encoder(111))
                ]
            ]

            update.message.reply_text(
                f'Testing Teledapps bot locally. Categories - {",".join(passport.categories)}',
                reply_markup=InlineKeyboardMarkup(keyboard)
            )

            return self.stages.basic

        bot.setup(token)

        logger.info('Starting bot locally')
        bot.run()
