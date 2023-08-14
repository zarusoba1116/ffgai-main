import re
import random
import discord
from discord.ext import commands
import asyncio
from win11toast import toast_async
import time
import json
import requests
from PIL import Image
from Word_list import words
import datetime

kanji_regex = re.compile(r'[\u4e00-\u9fff]')
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
            buttons = [{'activationType': 'protocol', 'arguments': r'D:\Other\ffgai-main\ffgai-main\open.pyw', 'content': 'Discordを開く'},
                {'activationType': 'protocol', 'arguments': '', 'content': '閉じる'}]
            await toast_async(f"{member.display_name} (#{after.channel.name})", f"📞 通話に接続しました", icon=member.avatar.url, duration='short', audio={'silent': 'true'}, buttons=buttons)

        elif after.channel is None:
            if me.voice:
                await toast_async(f"{member.display_name} (#{before.channel.name})", f"📞 通話を切断しました", icon=member.avatar.url, duration='short', audio={'silent': 'true'}, button='閉じる', on_click=r'D:\Other\ffgai-main\ffgai-main\open.pyw')

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
                await toast_async(f"{member.display_name} (#{after.channel.name})", f"🔇ミュートしました", icon=r"D:\Other\ffgai-main\ffgai-main\icon_mute.png", duration='short', audio={'silent': 'true'}, button='閉じる', on_click=r'D:\Other\ffgai-main\ffgai-main\open.pyw')
                
        
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
                await toast_async(f"{member.display_name} (#{after.channel.name})", f"🔊 ミュートを解除しました", icon=r"D:\Other\ffgai-main\ffgai-main\icon_unmute.png", duration='short', audio={'silent': 'true'}, button='閉じる', on_click=r'D:\Other\ffgai-main\ffgai-main\open.pyw')

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

@bot.command()
@commands.has_permissions(ban_members=True)
async def delmsg(ctx, target:int):
    channel = ctx.message.channel
    deleted = await channel.purge(limit=target)
    delmsg = discord.Embed(title="メッセージの削除が完了しました。",description=f"```{len(deleted)}メッセージを削除しました。```",color=0xa1b3b5)
    delmsg.set_author(name="The message deletion is complete",icon_url="https://media.discordapp.net/attachments/889860265896722442/892047450754416650/Delete.png")
    await ctx.send(embed=delmsg)

previous_output = None

@bot.listen("on_message")
async def on_message(message):
    pattern = "https?://[\w/:%#\$&\?\(\)~\.=\+\-]+"
    url = message.content
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

    elif re.match(pattern, url) or message.attachments:
        if random.randint(1,100) < 25:
            reactions = ['❤️', '♻️']
            text_1 = "FF外から失礼するゾ～（突撃）この乱戦面白スギィ！！！！！"
            text_2 = "FF外から失礼するゾ～（謝罪）このリンク先面白スギィ！！！！！"
            text_3 = "FF外から失礼するゾ～（謝罪）この画像面白スギィ！！！！！"
            sentence_1 = "自分、漁夫いいっすか？ 秘密知ってそうだから収容所にブチ込んでやるぜー"
            sentence_2 = "自分、拡散いいっすか？ 淫夢知ってそうだから淫夢のリストにぶち込んでやるぜー"
            sentence_3 = "いきなり撃ってすいません！許して下さい、なんでもしますから！(なんでもするとは言ってない)"
            sentence_4 = "いきなりリプしてすみません！許してください！なんでもしますから！(なんでもするとは言ってない)"
            if message.attachments:
                for attachment in message.attachments:
                    if attachment.url.endswith(("png", "jpg", "jpeg")):
                        for reaction in reactions:
                            await message.add_reaction(reaction)
                        if random.randint(1,100) < 5:
                            async with message.channel.typing():
                                await asyncio.sleep(0.5)
                                await message.channel.send(text_1)
                                await asyncio.sleep(0.5)
                                await message.channel.send(sentence_1)
                                await asyncio.sleep(0.5)
                                await message.channel.send(sentence_3)      
                        else:
                            async with message.channel.typing():
                                await asyncio.sleep(0.5)
                                await message.channel.send(text_3)
                                await asyncio.sleep(0.5)
                                await message.channel.send(sentence_2)
                                await asyncio.sleep(0.5)
                                await message.channel.send(sentence_4)
            else:
                for reaction in reactions:
                    await message.add_reaction(reaction)
                if random.randint(1,100) < 5:
                    async with message.channel.typing():
                        await asyncio.sleep(0.5)
                        await message.channel.send(text_1)
                        await asyncio.sleep(0.5)
                        await message.channel.send(sentence_1)
                        await asyncio.sleep(0.5)
                        await message.channel.send(sentence_3)       
                else:
                    async with message.channel.typing():
                        await asyncio.sleep(0.5)
                        await message.channel.send(text_2)
                        await asyncio.sleep(0.5)
                        await message.channel.send(sentence_2)
                        await asyncio.sleep(0.5)
                        await message.channel.send(sentence_4)

    elif bot.user in message.mentions:
        await message.channel.send("ホモはせっかち、はっきりわかんだね")

    else:
        if random.randint(1,100) < 50:
            global previous_output
            if "$" in message.content:
                return
            test = random.randint(1,100)
            print(test)
            input_str = message.content
            print(input_str)
            kanji_list = kanji_regex.findall(input_str)
            print(kanji_list)
            kanji_str = ''.join(kanji_list)
            print(kanji_str)
            found_words = [word for word in words if any(char in kanji_str for char in word)]
            print(found_words)
            if found_words:
                random_word = random.choice(found_words)
                print(random_word)
                if random_word != previous_output and input_str not in words:
                    await message.reply(random_word, mention_author=False)
                    previous_output = random_word
                else:
                    random_word = random.choice(words)
                    print(random_word)
                    await message.reply(random_word, mention_author=False)
                    previous_output = random_word
            else: 
                random_word = random.choice(words)
                print(random_word)
                await message.reply(random_word, mention_author=False)
                previous_output = random_word

def calculate_percentage_of_year():
    current_date = datetime.date.today()
    year_start_date = datetime.date(current_date.year, 1, 1)
    year_end_date = datetime.date(current_date.year, 12, 31)
    days_passed = (current_date - year_start_date).days
    total_days_in_year = (year_end_date - year_start_date).days + 1
    percentage = (days_passed / total_days_in_year) * 100
    return percentage

def calculate_percentage_of_day():
    now = datetime.datetime.now()
    midnight = now.replace(hour=0, minute=0, second=0, microsecond=0)
    total_day_time = datetime.timedelta(days=1)
    time_passed = now - midnight
    percentage = (time_passed.total_seconds() / total_day_time.total_seconds()) * 100
    return percentage

def create_progress_bar(value, max_value, bar_length=25):
    progress = value / max_value
    num_bar_hashes = int(round(bar_length * progress))
    bar = '#' * num_bar_hashes + '-' * (bar_length - num_bar_hashes)
    return f"[{bar}] {value:.2f}%"

max_value = 100
percentage_of_year = calculate_percentage_of_year()
percentage_of_day = calculate_percentage_of_day()

async def animate_progress(ctx, channel):
    num_frames = 5
    percentage_of_year = calculate_percentage_of_year()
    percentage_of_day = calculate_percentage_of_day()
    embed = discord.Embed(color=0x2997ff ,description="")
    embed.set_footer(text="開始")
    msg = await channel.send(embed=embed)

    for frame in range(num_frames + 1):
        current_percentage_year = (percentage_of_year * frame) / num_frames
        current_percentage_day = (percentage_of_day * frame) / num_frames
        channel = ctx.channel
        animation_chars = ['.', '..', '...']
        animation = animation_chars[frame % len(animation_chars)]
        progress_bar1 = create_progress_bar(current_percentage_year, max_value)
        progress_bar2 = create_progress_bar(current_percentage_day, max_value)
        embed = discord.Embed(color=0x2997ff)
        embed.add_field(name="1年の進行状況", value=f"```{progress_bar1}```", inline=False)
        embed.add_field(name="1日の進行状況", value=f"```{progress_bar2}```", inline=False)
        embed.set_footer(text=f"進行中{animation}")
        await msg.edit(embed=embed)

    embed1 = discord.Embed(color=0x2997ff ,description="")
    progress_bar1 = create_progress_bar(current_percentage_year, max_value)
    progress_bar2 = create_progress_bar(current_percentage_day, max_value)
    embed1 = discord.Embed(color=0x2997ff)
    embed1.add_field(name="1年間の進行状況", value=f"```fix\n{progress_bar1}\n```", inline=False)
    embed1.add_field(name="1日の進行状況", value=f"```fix\n{progress_bar2}\n```", inline=False)
    await msg.edit(embed=embed1)

@bot.command(name='time')
async def progress(ctx):
    # Start the animation when the command is executed
    await animate_progress(ctx, ctx.channel)

bot.run(TOKEN)
