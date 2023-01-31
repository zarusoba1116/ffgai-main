import discord
import asyncio
from discord.ext import commands
from datetime import datetime

intents = discord.Intents.all()
intents.typing = False

TOKEN = 'ODk5OTUyMTEyNjM1NjQxODU2.GR5_br.wTu3999-rYY4MUTxycKea83YUyJ_1ISw5I_DQ4'
bot = commands.Bot(command_prefix='$',help_command=None,case_insensitive=True,intents=intents)
dt_now = datetime.now()

@bot.event
async def on_ready():
    guild = bot.get_guild(852145141909159947)
    member = guild.get_member(733646900481490976)
    await member.voice.channel.connect()
    now = datetime.now()
    now = datetime(now.year, now.month, now.day, now.hour, now.minute, now.second, now.microsecond)
    comp = datetime(now.year, now.month, now.day, now.hour, now.minute, 19, 0)
    diff = comp.timestamp() - now.timestamp()
    print(diff)
    if diff < 0:
        now = datetime.now()
        now = datetime(now.year, now.month, now.day, now.hour, now.minute, now.second, now.microsecond)
        comp = datetime(now.year, now.month, now.day, now.hour, now.minute+1, 19, 0)
        diff = comp.timestamp() - now.timestamp()
        print(diff)
        await asyncio.sleep(diff)
        loop = asyncio.get_event_loop()
        loop.create_task(play())
    else:
        await asyncio.sleep(diff)
        loop = asyncio.get_event_loop()
        loop.create_task(play())
    

async def play():
        guild = bot.get_guild(852145141909159947)
        guild.voice_client.play(discord.FFmpegPCMAudio("unicorn.mp3"))
        await asyncio.sleep(90)
        guild.voice_client.disconnect()

bot.run(TOKEN)