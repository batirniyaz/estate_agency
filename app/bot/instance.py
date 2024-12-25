from telebot.async_telebot import AsyncTeleBot
import telebot
from app.config import TOKEN
from app.config import CHANNEL_RENT_ID, CHANNEL_SALE_ID

bot = AsyncTeleBot(TOKEN)


class IsAdmin(telebot.custom_filters.SimpleCustomFilter):
    key = 'is_admin'

    @staticmethod
    def check(message: telebot.types.Message):
        for channel_id in ['-100' + CHANNEL_RENT_ID, '-100' + CHANNEL_SALE_ID]:
            status = bot.get_chat_member(channel_id, message.from_user.id).status
            if status in ['administrator', 'creator']:
                return True
        return False

bot.add_custom_filter(IsAdmin())
