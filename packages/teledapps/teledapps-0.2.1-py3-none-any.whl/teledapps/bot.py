from telegram.ext import Updater, ConversationHandler
from collections import defaultdict

from .actions import BasicAction


class Bot:
    def __init__(self):
        self.updater = None

        self.entry_points = []
        self.fallbacks = []
        self.states = defaultdict(list)

    def state(self, action, stage):
        """
        Specify handler as state handler

        :param action:
        :param stage:
        :return:
        """

        def decorator(function):
            self.states[stage].append(action.get_handler(function))

            def wrapped(*args, **kwargs):
                return function(*args, **kwargs)

            return wrapped

        return decorator

    def entry_point(self, action: BasicAction):
        """
        Specify handler as entry point

        :param action:
        :return:
        """

        def decorator(function):
            self.entry_points.append(action.get_handler(function))

            def wrapped(*args, **kwargs):
                return function(*args, **kwargs)

            return wrapped

        return decorator

    def setup(self, token):
        """
        Setup conversation handler according to the specified entry points,
        states and fallbacks.

        :return:
        """

        self.updater = Updater(token, use_context=True)

        conversation = ConversationHandler(
            entry_points=self.entry_points,
            states=self.states,
            fallbacks=self.fallbacks
        )

        self.updater.dispatcher.add_handler(conversation)

    def register_bot(self, bot: 'Bot'):
        """
        Register another bot entry points, states and fallbacks in the parent bot.
        Allows to write modular bots.

        :param bot:
        :return:
        """

        self.entry_points += bot.entry_points
        self.fallbacks += bot.fallbacks

        for k, v in bot.states.items():
            self.states[k] += v

    def run(self):
        """
        Run bot

        :return:
        """

        self.updater.start_polling()
        self.updater.idle()


