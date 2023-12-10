from asyncio import to_thread
from deep_translator import GoogleTranslator


class Translator(object):
    def __init__(self, language: str):
        self.google_translator = GoogleTranslator(source='auto', target=language)

    async def translate(self, text):
        translated_text = await to_thread(self.google_translator.translate, text)
        return translated_text.capitalize()
