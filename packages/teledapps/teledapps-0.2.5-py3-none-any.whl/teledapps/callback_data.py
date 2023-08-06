class CallbackData:
    def __init__(self, pattern: str, encoder, decoder):
        """
        Wraps logic about

        - Inline keyboard button callback data pattern
        - Encoding business-logic in callback data
        - Decoding business-logic from callback data

        :param pattern: Usually regex, used as pattern in CallbackQueryHandler
        :param encoder: Function that encode business-logic args into string
        which is used as callback_data in InlineKeyboardButton
        :param decoder: Function that takes data from query
        and decode it into business-logic vars
        """

        self.pattern = pattern
        self.encoder = encoder
        self.decoder = decoder
