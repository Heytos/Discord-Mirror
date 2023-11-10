import io

import discord
import aiohttp

from discord.ext import commands

intents = discord.Intents.default()
intents.messages = True
intents.message_content = True
intents.guild_messages = True

bot = commands.Bot(command_prefix='!', intents=intents)

source_channel = 1137055512802906122
destination_channel = 1171772079872430101

@bot.event
async def on_message(message):
    if message.author.bot:
        return

    if message.channel.id == source_channel:
        target_channel = bot.get_channel(destination_channel)
        if target_channel:
            if message.content:
                await target_channel.send(message.content)

            for attachment in message.attachments:
                async with aiohttp.ClientSession() as session:
                    async with session.get(attachment.url) as resp:
                        if resp.status == 200:
                            data = io.BytesIO(await resp.read())
                            await target_channel.send(file=discord.File(data, attachment.filename))
        else:
            print(f"Канал с ID {destination_channel} не найден.")


@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')

@bot.command()
async def send_message(ctx, *, message):
    channel_id = 1171772079872430101
    channel = bot.get_channel(channel_id)
    if channel:
        await channel.send(message)
    else:
        await ctx.send("Канал не найден.")

bot.run('YOUR_DS_TOKEN')