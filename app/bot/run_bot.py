from app.bot import handlers
from app.bot.instance import bot


async def run_bot():
    try:
        print('Bot is running...')
        await bot.polling(
            none_stop=True,
            skip_pending=True,
            timeout=30,
        )
    except Exception as e:
        print(f"Bot polling error: {e}")
        import traceback
        traceback.print_exc()

