class TranslationError(Exception):
    def __init__(self, message):
        super().__init__(f'Translation error: {message}')
