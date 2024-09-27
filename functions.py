import os
import requests
from telegram import Update
from telegram.ext import CallbackContext, ConversationHandler

START, END = range(2)


def get_exchange_rates() -> float:
    """Функция, получающая курс доллара."""
    exchange_rates_api_key = os.getenv("EXCHANGE_RATES_API_KEY")
    url = "https://api.apilayer.com/exchangerates_data/convert?to=RUB&from=USD&amount=1"
    headers = {
        "apikey": exchange_rates_api_key
    }
    response = requests.request("GET", url, headers=headers)
    data = response.json()
    return round(data["info"]["rate"], 2)


def lets_start(update: Update, context: CallbackContext):
    """Функция, вызывающая приветственное сообщение."""
    update.message.reply_text('Добрый день. Как вас зовут?')
    return START


def get_user_name_and_answer_rates(update: Update, context: CallbackContext):
    """Функция, принимающая имя пользователя и возвращающая курс"""
    user_name = update.message.text
    usd_price = get_exchange_rates()
    update.message.reply_text(f'Рад знакомству, {user_name}! Курс доллара сегодня {usd_price}р.'
                              f'Для завершения диалога введите "/end"')
    return END

def end_conversation(update: Update, context: CallbackContext):
    """Функция, завершающая диалог"""
    update.message.reply_text("До свидания! Если захотите узнать курс снова, просто напишите /start.")
    return ConversationHandler.END
