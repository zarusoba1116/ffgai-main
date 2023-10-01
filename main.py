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

kanji_regex = re.compile(r'[\u4e00-\u9fff]')
json_open = open('data.json', 'r')
json_data = json.load(json_open)
TOKEN = os.getenv("DISCORD_TOKEN")
intents = discord.Intents.all()
intents.typing = False
guild = 852145141909159947

bot = commands.Bot(command_prefix='$',help_command=None,case_insensitive=True,intents=intents)

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

keep_alive()
bot.run(TOKEN)
