from telegram import Bot
from io import BytesIO

from ..utils import BOT_TOKEN


class BOT(object):
    def __init__(self, bot_token: str = BOT_TOKEN):
        self.bot = Bot(bot_token)

    async def send_document_to_bot(self, telegram_id: int, file, filename: str) -> None:
        await self.bot.send_document(chat_id=telegram_id, document=BytesIO(file), filename=filename)
