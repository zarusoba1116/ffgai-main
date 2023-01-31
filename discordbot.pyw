import re
import random
import discord
from discord.ext import commands
import asyncio
import Word_list
from win11toast import toast_async
import requests
from PIL import Image
import time
import json

json_open = open('data.json', 'r')
json_data = json.load(json_open)

intents = discord.Intents.all()
intents.typing = False
guild = 852145141909159947

TOKEN = 'ODk5OTUyMTEyNjM1NjQxODU2.GR5_br.wTu3999-rYY4MUTxycKea83YUyJ_1ISw5I_DQ4'
bot = commands.Bot(command_prefix='$',help_command=None,case_insensitive=True,intents=intents)

@bot.event
async def on_member_join(member):
    guild = bot.get_guild(852145141909159947)
    channel = guild.get_channel(852145141909159950)
    await channel.send(f"{member.mention}がサーバーに参加したゾ～\nハイ、ヨロシクゥ！")

snipe_message_author = {}
snipe_message_content = {}

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
                
@bot.event
async def on_message_delete(message):
    snipe_message_author[message.channel.id] = message.author
    snipe_message_content[message.channel.id] = message.content
    await asyncio.sleep(60)
    del snipe_message_author[message.channel.id]
    del snipe_message_content[message.channel.id]

@bot.command(name = 'snipe')
async def snipe(ctx):
    channel = ctx.channel
    try: #This piece of code is run if the bot finds anything in the dictionary
        em = discord.Embed(title = snipe_message_content[channel.id], color=discord.Color.blue())
        em.set_footer(text = f"{snipe_message_author[channel.id]} が送信しました")

        await ctx.send(embed = em)
    except KeyError: #This piece of code is run if the bot doesn't find anything in the dictionary
        await ctx.send("最近削除されたメッセージはありません")

@bot.command(name = 'Prime')
async def Prime(ctx, x):
    y = int(x)
    if y <= 1:
        await ctx.send("No!! No!! No!!")
    else:
        for i in range(2, int(y**0.5)+1):
            if y % i == 0:
                await ctx.send("No!! No!! No!!")
                break
        else:
            await ctx.send("Yes!! Yes!! Yes!!")

@bot.command()
async def ping(ctx):
    raw_ping = bot.latency
    ping = round(raw_ping * 1000)
    embed_ping = discord.Embed(title="FF外から失礼するゾ～(謝罪)BOTの応答速度",description=f"```{ping}ms```",color=0xa1b3b5)
    embed_ping.set_author(name="Pong! This is the response speed.",icon_url="https://media.discordapp.net/attachments/889860265896722442/896781428350677022/084c6c1c62a26a59.png")
    await ctx.send(embed=embed_ping)

@bot.command()
async def tr(ctx):
    result = Translator.translate("hello", src="en", dest="ja").text
    await ctx.send(result)

@bot.command()
async def syamu(ctx):
    guild = bot.get_guild(852145141909159947)
    channel = guild.get_channel(852145141909159950)
    await channel.send("オッスお願いしま～す")

@bot.command()
@commands.has_permissions(ban_members=True)
async def delmsg(ctx, target:int):
    channel = ctx.message.channel
    deleted = await channel.purge(limit=target)
    delmsg = discord.Embed(title="メッセージの削除が完了しました。",description=f"```{len(deleted)}メッセージを削除しました。```",color=0xa1b3b5)
    delmsg.set_author(name="The message deletion is complete",icon_url="https://media.discordapp.net/attachments/889860265896722442/892047450754416650/Delete.png")
    await ctx.send(embed=delmsg)

@bot.listen("on_message")
async def on_message(message):
    pattern = "https?://[\w/:%#\$&\?\(\)~\.=\+\-]+"
    url = message.content
    x = random.randint(0,10)
    ff = random.randint(0,10)
    if message.author.bot:
        return
    elif message.channel.id == 1015272719606104064:
        if '<@' in message.content:
            guild = bot.get_guild(message.guild.id)
            user_id_list = re.findall(r'@[0-9]{18}', message.content)
            user_id_list = list(map(lambda x: int(x.replace('@', '')), user_id_list))
            for user_id in user_id_list:
                user = guild.get_member(user_id)
                count = json_data
                count.setdefault(str(user_id), 0)
                load_count = json_data[str(user_id)]
                count[str(user_id)] = 1 + load_count
                with open("data.json", "w") as f:
                    json.dump(count, f)
                t = int(time.time())
                print(user_id)
                print(user)
                embed=discord.Embed(title="寝落ち報告", color=0x2997ff)
                embed.set_thumbnail(url=user.avatar.url)
                embed.add_field(name="名前", value='<@' + str(user_id) + '>', inline=True)
                embed.add_field(name="チャンネル", value='<#' + str(user.voice.channel.id) + '>', inline=True)
                embed.add_field(name="時間", value='<t:' + str(t) + '>', inline=True)
                load_count = json_data[str(user_id)]
                embed.add_field(name="合計寝落ち回数", value='```' + str(load_count) + '回```', inline=True)
                embed.set_footer(text="いろんなともとも 寝落ち報告スレ")
                await message.channel.send(embed=embed)
                await message.delete()
        else:
            await message.delete()

    elif message.channel.id == 1045655314428608562:
        guild = bot.get_guild(852145141909159947)
        channel = guild.get_channel(852145141909159950)
        await channel.send(message.content)

    elif re.match(pattern, url):
        if x < 2.5:
            if ff < 0.5:
                await message.add_reaction('❤️')
                await message.add_reaction('♻️')
                async with message.channel.typing():
                    await asyncio.sleep(1)
                    await message.channel.send("FF外から失礼するゾ～（突撃）この乱戦面白スギィ！！！！！")
                    await asyncio.sleep(0.5)
                    async with message.channel.typing():
                        await asyncio.sleep(1)
                        await message.channel.send("自分、漁夫いいっすか？ 秘密知ってそうだから収容所にブチ込んでやるぜー")
                        await asyncio.sleep(0.5)
                        async with message.channel.typing():
                            await asyncio.sleep(1)
                            await message.channel.send("いきなり撃ってすいません！許して下さい、なんでもしますから！(なんでもするとは言ってない)")
            else:
                await message.add_reaction('❤️')
                await message.add_reaction('♻️')
                async with message.channel.typing():
                    await asyncio.sleep(1)
                    await message.channel.send("FF外から失礼するゾ～（謝罪）このリンク先面白スギィ！！！！！")
                    await asyncio.sleep(0.5)
                    async with message.channel.typing():
                        await asyncio.sleep(1)
                        await message.channel.send("自分、拡散いいっすか？ 淫夢知ってそうだから淫夢のリストにぶち込んでやるぜー")
                        await asyncio.sleep(0.5)
                        async with message.channel.typing():
                            await asyncio.sleep(1)
                            await message.channel.send("いきなりリプしてすみません！許してください！なんでもしますから！(なんでもするとは言ってない)")

    elif message.attachments:
        if x < 2.5:
            if ff < 0.5:
                for attachment in message.attachments:
                    if attachment.url.endswith(("png", "jpg", "jpeg")):
                        await message.add_reaction('❤️')
                        await message.add_reaction('♻️')
                        async with message.channel.typing():
                            await asyncio.sleep(1)
                            await message.channel.send("FF外から失礼するゾ～（突撃）この乱戦面白スギィ！！！！！")
                            await asyncio.sleep(0.5)
                            async with message.channel.typing():
                                await asyncio.sleep(1)
                                await message.channel.send("自分、漁夫いいっすか？ 秘密知ってそうだから収容所にブチ込んでやるぜー")
                                await asyncio.sleep(0.5)
                                async with message.channel.typing():
                                    await asyncio.sleep(1)
                                    await message.channel.send("いきなり撃ってすいません！許して下さい、なんでもしますから！(なんでもするとは言ってない)")
            else:
                await message.add_reaction('❤️')
                await message.add_reaction('♻️')
                async with message.channel.typing():
                    await asyncio.sleep(1)
                    await message.channel.send("FF外から失礼するゾ～（謝罪）このリンク先面白スギィ！！！！！")
                    await asyncio.sleep(0.5)
                    async with message.channel.typing():
                        await asyncio.sleep(1)
                        await message.channel.send("自分、拡散いいっすか？ 淫夢知ってそうだから淫夢のリストにぶち込んでやるぜー")
                        await asyncio.sleep(0.5)
                        async with message.channel.typing():
                            await asyncio.sleep(1)
                            await message.channel.send("いきなりリプしてすみません！許してください！なんでもしますから！(なんでもするとは言ってない)")

    elif bot.user in message.mentions:
        await message.channel.send("ホモはせっかち、はっきりわかんだね")

    else:
        if message.author.bot:
            return
        else:
            if x < 2.5:
                await message.reply(f"{random.choice(Word_list.word)}", mention_author=False)

bot.run(TOKEN)
