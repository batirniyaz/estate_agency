from telebot.async_telebot import AsyncTeleBot
import telebot
from app.config import TOKEN
from app.config import CHANNEL_ID

bot = AsyncTeleBot(TOKEN)


class IsAdmin(telebot.custom_filters.SimpleCustomFilter):
    key = 'is_admin'

    @staticmethod
    def check(message: telebot.types.Message):
        return bot.get_chat_member('-100' + CHANNEL_ID, message.from_user.id).status in ['administrator', 'creator']


bot.add_custom_filter(IsAdmin())
