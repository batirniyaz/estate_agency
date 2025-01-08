import asyncio

from telebot import types, asyncio_helper

from .instance import bot

from app.config import BASE_URL


@bot.message_handler(commands=['start', 'help'])
async def bot_start(message: types.Message):
    await bot.reply_to(message, 'Hi, Estate Agency bot to post objects to channel')


@bot.message_handler(commands=['get_id'])
async def get_id(message: types.Message):
    cid = message.chat.id
    mid = message.message_id
    fid = message.from_user.id
    await bot.send_message(message.chat.id, '\n'.join([f'cid: {cid}', f'mid: {mid}', f'fid: {fid}']))


async def send_message_to_channel(message: str, media: list, channel_id: str):
    media_list = []
    id_channel = '-100' + channel_id

    for index, obj in enumerate(media):
        if obj.media_type == 'image':
            if index == 0:
                media_list.append(types.InputMediaPhoto(f'{BASE_URL}/{obj.url}', caption=message, parse_mode='HTML'))
            else:
                media_list.append(types.InputMediaPhoto(f'{BASE_URL}/{obj.url}'))
        elif obj.media_type == 'video':
            if index == 0:
                media_list.append(types.InputMediaVideo(f'{BASE_URL}/{obj.url}', caption=message, parse_mode='HTML'))
            else:
                media_list.append(types.InputMediaVideo(f'{BASE_URL}/{obj.url}'))
        else:
            ...

    while True:
        try:
            if media_list:
                await bot.send_media_group(id_channel, media_list)
            else:
                await bot.send_message(id_channel, message, parse_mode='HTML', disable_web_page_preview=True)
            break
        except asyncio_helper.ApiTelegramException as e:
            if e.error_code == 429:
                retry_after = int(e.result_json['parameters']['retry_after'])
                print(f"Rate limit exceeded. Retrying after {retry_after} seconds.")
                await asyncio.sleep(retry_after)
            else:
                raise
