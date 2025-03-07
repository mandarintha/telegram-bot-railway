import json
import random
import telebot
import logging
import io
from gtts import gTTS
from deep_translator import GoogleTranslator
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import requests
import os

# Logging Configuration
logging.basicConfig(level=logging.INFO)

# Token dari Environment Variable (Gunakan Railway ENV)
TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(TOKEN)

# Load HSK vocabulary data dari URL (Host di GitHub)
hsk_levels = {
    "HSK 1": "https://raw.githubusercontent.com/USERNAME/telegram-bot-railway/main/hsk-level-1.json",
    "HSK 2": "https://raw.githubusercontent.com/USERNAME/telegram-bot-railway/main/hsk-level-2.json",
    "HSK 3": "https://raw.githubusercontent.com/USERNAME/telegram-bot-railway/main/hsk-level-3.json",
	"HSK 4": "https://raw.githubusercontent.com/USERNAME/telegram-bot-railway/main/hsk-level-4.json",
	"HSK 5": "https://raw.githubusercontent.com/USERNAME/telegram-bot-railway/main/hsk-level-5.json",
	"HSK 6": "https://raw.githubusercontent.com/USERNAME/telegram-bot-railway/main/hsk-level-6.json"
}

def load_hsk_data(level):
    try:
        url = hsk_levels[level]
        response = requests.get(url)
        return response.json()
    except Exception as e:
        logging.error(f"Error loading HSK data: {e}")
        return []

# Generate TTS tanpa menyimpan file
def send_tts(chat_id, text, lang):
    try:
        tts = gTTS(text, lang=lang)
        audio_stream = io.BytesIO()
        tts.write_to_fp(audio_stream)
        audio_stream.seek(0)
        bot.send_audio(chat_id, audio_stream)
    except Exception as e:
        logging.error(f"TTS error: {e}")
        bot.send_message(chat_id, "Failed to generate audio.")

# Command handler
@bot.message_handler(commands=["start", "help"])
def send_welcome(message):
    bot.send_message(message.chat.id, "Welcome to HSK Bot! Please select an HSK level.")
    send_tts(message.chat.id, "Welcome to HSK Bot!", "en")

# Run bot
if __name__ == "__main__":
    logging.info("Bot is running...")
    bot.polling(none_stop=True, interval=0)
