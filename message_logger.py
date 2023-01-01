import telebot
from datetime import datetime
from bot_mode import BotModes


def log(message, handler_name, mode: BotModes):
    with open('log.csv', 'a') as f:
        f.write(f'{datetime.now().strftime("%Y-%m-%d, %H:%M:%S")},{mode.name},{handler_name},'
                f'{message.chat.id},{message.from_user.id},{message.from_user.username},{message.text}\n')
