import re
import random
import discord
from discord.ext import commands
import asyncio
import time
import json
from Word_list import words
from os import getenv

TOKEN = getenv('DISCORD_BOT_TOKEN')
kanji_regex = re.compile(r'[\u4e00-\u9fff]')
intents = discord.Intents.all()
intents.typing = False

bot = commands.Bot(command_prefix='$', help_command=None, case_insensitive=True, intents=intents)

def load_data():
    try:
        with open('data.json', 'r') as json_open:
            return json.load(json_open)
    except FileNotFoundError:
        # 初回起動時など、ファイルが存在しない場合は空のデータを返す
        return {"SleepCounts": {}, "ServerBlackList": []}

def save_data(data):
    with open("data.json", "w") as f:
        json.dump(data, f, indent=4)

@bot.listen("on_message")
async def on_message(message):
    data = load_data()
    ServerBlackList = data["ServerBlackList"]

    guild = bot.get_guild(message.guild.id)
    pattern = "https?://[\w/:%#\$&\?\(\)~\.=\+\-]+"
    url = message.content

    if message.author.bot:
        return
    elif message.channel.id in [1189922398049402890, 1183748739366662176, 876362300632760342]:
        if message.mentions:
            for user_mention in message.mentions:
                user_id = user_mention.id
                user = guild.get_member(user_id)
                avatar_url = user.avatar.url

                count = data["SleepCounts"]
                count.setdefault(str(user_id), 0)
                load_count = count[str(user_id)]
                count[str(user_id)] = 1 + load_count

                data["SleepCounts"] = count
                save_data(data)

                t = int(time.time())
                print(user.name)
                embed = discord.Embed(title="寝落ち報告", color=0x2997ff)
                embed.set_thumbnail(url=avatar_url)
                embed.add_field(name="名前", value=user.mention, inline=True)
                embed.add_field(name="チャンネル", value='<#' + str(user.voice.channel.id) + '>', inline=True)
                embed.add_field(name="時間", value=f'<t:{t}>', inline=True)
                embed.add_field(name="合計寝落ち回数", value=f'```{load_count}回```', inline=True)
                embed.set_footer(text=f'{guild.name} {message.channel.name}')
                await message.channel.send(embed=embed)
                await message.delete()
        else:
            await message.delete()

            
    if message.guild.id not in ServerBlackList:
        
        if re.match(pattern, url) or message.attachments:
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

        else:
            if random.randint(1,100) < 50:
                global previous_output
                if "$" in message.content:
                    return
                input_str = message.content
                kanji_list = kanji_regex.findall(input_str)
                kanji_str = ''.join(kanji_list)
                found_words = [word for word in words if any(char in kanji_str for char in word)]
                if found_words:
                    random_word = random.choice(found_words)
                    if random_word != previous_output and input_str not in words:
                        await message.reply(random_word, mention_author=False)
                        previous_output = random_word
                    else:
                        random_word = random.choice(words)
                        await message.reply(random_word, mention_author=False)
                        previous_output = random_word
                else: 
                    random_word = random.choice(words)
                    await message.reply(random_word, mention_author=False)
                    previous_output = random_word
                    
@bot.event
async def on_reaction_add(reaction, user):
    if reaction.message.author == bot.user:  # リアクションがつけられたメッセージの送信者がボット自身なら
        await reaction.message.delete()


bot.run(TOKEN)
