import discord
from discord.ext import commands
from win11toast import toast_async
import requests
from PIL import Image
import json

json_open = open('data.json', 'r')
json_data = json.load(json_open)

intents = discord.Intents.all()
intents.typing = False
guild = 852145141909159947

TOKEN = 'ODk5OTUyMTEyNjM1NjQxODU2.GR5_br.wTu3999-rYY4MUTxycKea83YUyJ_1ISw5I_DQ4'
bot = commands.Bot(command_prefix='$',help_command=None,case_insensitive=True,intents=intents)

@bot.event
async def on_voice_state_update(member, before, after): 
    guild = bot.get_guild(852145141909159947)
    me = guild.get_member(733646900481490976)
    if me != member:
        if before.channel is None:
            url = await after.channel.create_invite()
            buttons = [{'activationType': 'protocol', 'arguments': str(url), 'content': '通話に接続'},
                {'activationType': 'protocol', 'arguments': '', 'content': '閉じる'}]
            await toast_async(f"{member.display_name} (#{after.channel.name})", f"📞 通話に接続しました", icon=member.avatar.url, duration='short', audio={'silent': 'true'}, buttons=buttons)

        elif after.channel is None:
            if me.voice:
                await toast_async(f"{member.display_name} (#{before.channel.name})", f"📞 通話を切断しました", icon=member.avatar.url, duration='short', audio={'silent': 'true'}, button='閉じる')

        elif not before.self_mute and after.self_mute:
            if me.voice:
                file_name = "icon.png"
                response = requests.get(member.avatar.url)
                image = response.content
                with open(file_name, "wb") as f:
                    f.write(image)
                icon_path = 'icon.png'
                mute_path = 'mute.png'
                out_path = 'icon_mute.png'
                icon = Image.open(icon_path)
                mute = Image.open(mute_path)
                icon = icon.resize((600, 600))
                icon.paste(mute, (0, 0), mute)
                icon.save(out_path)
                await toast_async(f"{member.display_name} (#{after.channel.name})", f"🔇ミュートしました", icon=r"D:\Other\ffgai-main\ffgai-main\icon_mute.png", duration='short', audio={'silent': 'true'}, button='閉じる')
                
        
        elif before.self_mute and not after.self_mute:
            if me.voice:
                file_name = "icon.png"
                response = requests.get(member.avatar.url)
                image = response.content
                with open(file_name, "wb") as f:
                    f.write(image)
                icon_path = 'icon.png'
                unmute_path = 'unmute.png'
                out_path = 'icon_unmute.png'
                icon = Image.open(icon_path)
                unmute = Image.open(unmute_path)
                icon = icon.resize((600, 600))
                icon.paste(unmute, (0, 0), unmute)
                icon.save(out_path)
                await toast_async(f"{member.display_name} (#{after.channel.name})", f"🔊 ミュートを解除しました", icon=r"D:\Other\ffgai-main\ffgai-main\icon_unmute.png", duration='short', audio={'silent': 'true'}, button='閉じる')

bot.run(TOKEN)