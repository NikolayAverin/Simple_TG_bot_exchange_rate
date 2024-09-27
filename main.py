import os
from pathlib import Path
from dotenv import load_dotenv
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler
from functions import lets_start, get_user_name_and_answer_rates, end_conversation, START, END

BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env")


def main():
    """Основная функция"""
    tg_api_key = os.getenv("TG_API_KEY")
    tg_bot = Updater(tg_api_key)
    dispatcher = tg_bot.dispatcher
    definition_states = ConversationHandler(
        entry_points=[CommandHandler('start', lets_start)],
        states={
            START: [MessageHandler(Filters.text & ~Filters.command, get_user_name_and_answer_rates)],
            END: [CommandHandler('start', lets_start), CommandHandler('end', end_conversation)]
        },
        fallbacks=[CommandHandler('end', end_conversation)]
    )
    dispatcher.add_handler(definition_states)
    tg_bot.start_polling()
    tg_bot.idle()

if __name__ == '__main__':
    main()
