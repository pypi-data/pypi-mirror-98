class BotPassport:
    def __init__(self, **kwargs):
        self.name = kwargs['name']
        self.categories = kwargs['categories']
        self.id = kwargs['id']
