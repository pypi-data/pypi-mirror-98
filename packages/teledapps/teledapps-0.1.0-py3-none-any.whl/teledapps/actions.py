from telegram.ext import (
    CommandHandler,
    MessageHandler,
    Filters,
    CallbackQueryHandler
)


class BasicAction:
    def get_handler(self, callback):
        raise Exception('No handler specified')


class KeyboardButton(BasicAction):
    def __init__(self, text):
        self.text = text

    def get_handler(self, callback):
        return MessageHandler(Filters.regex(self.text), callback)


class Input(BasicAction):
    def __init__(self, pattern):
        self.pattern = pattern

    def get_handler(self, callback):
        return MessageHandler(Filters.regex(self.pattern), callback)


class Command(BasicAction):
    def __init__(self, command):
        self.command = command

    def get_handler(self, callback):
        return CommandHandler(self.command, callback)


class InlineKeyboardButton(BasicAction):
    def __init__(self, pattern):
        self.pattern = pattern

    def get_handler(self, callback):
        return CallbackQueryHandler(callback, pattern=self.pattern)
