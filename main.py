import discord
import datetime
import sys
import asyncio

from discord.ext import commands
from loguru import logger

# Настройки бота
TOKEN = "Токен"  # Замените на ваш токен
PREFIX = "!"
DEBUG = True

# Словарь маппинга каналов
CHANNEL_MAPPINGS = {
    1173017625886998678: 1171772079872430101,  # ID исходного канала: ID целевого канала
    # Добавьте дополнительные каналы здесь
}

# Настройка логирования
logger.remove()
log_file_name = f'{datetime.datetime.now().strftime("%d-%m-%Y")}.log'
logger.add(log_file_name, level="DEBUG" if DEBUG else "INFO", rotation='1 day')
logger.add(sys.stderr, colorize=True, level='DEBUG' if DEBUG else 'INFO')

# Настройка интентов
intents = discord.Intents.default()  # Инициализация интентов
intents.messages = True  # Разрешение для обработки сообщений
intents.members = True   # Разрешение для работы с участниками сервера

#Проблема возникает именно в интентах (кусок кода выше). Они конфликтуют с токеном юзера, но адекватно работают с токеном бота

# Класс для мирроринга сообщений
class ServerMirror:
    def __init__(self, bot):
        self.bot = bot

    async def on_message(self, message):
        if message.channel.id in CHANNEL_MAPPINGS:
            target_channel_id = CHANNEL_MAPPINGS[message.channel.id]
            target_channel = self.bot.get_channel(target_channel_id)
            if target_channel:
                # Создание копии embeds
                embeds = [discord.Embed.from_dict(embed.to_dict()) for embed in message.embeds]
                # Отправка сообщения с тем же содержимым и embeds
                await target_channel.send(content=message.content, embeds=embeds)

# Инициализация бота
bot = commands.Bot(command_prefix=PREFIX, case_insensitive=True, intents=intents)  # Исправлено здесь

@bot.event
async def on_connect():
    logger.success("Logged on as {0.user}".format(bot))

@bot.event
async def on_message(message):
    await bot.process_commands(message)
    await server_mirror.on_message(message)

# Запуск бота
if __name__ == '__main__':
    bot.run(TOKEN)


