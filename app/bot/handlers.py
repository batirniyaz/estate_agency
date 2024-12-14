from telebot import types

from .instance import bot

from app.config import CHANNEL_ID

id_channel = '-100' + CHANNEL_ID


@bot.message_handler(commands=['start', 'help'])
async def bot_start(message: types.Message):
    await bot.reply_to(message, 'Hi, Estate Agency bot to post objects to channel')


@bot.message_handler(commands=['get_id'])
async def get_id(message: types.Message):
    cid = message.chat.id
    mid = message.message_id
    fid = message.from_user.id
    await bot.send_message(message.chat.id, '\n'.join([f'cid: {cid}', f'mid: {mid}', f'fid: {fid}']))


async def send_message_to_channel(message: str):
    await bot.send_message(id_channel, message, parse_mode='HTML')
