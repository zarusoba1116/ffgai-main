# -*- coding: utf-8 -*-
import re
import random
import discord
from discord.ext import commands
import asyncio
import time
import json
from Word_list import words
from os import getenv
from keep_alive import keep_alive
import homo

TOKEN = getenv('DISCORD_BOT_TOKEN')
kanji_regex = re.compile(r'[\u4e00-\u9fff]')
intents = discord.Intents.all()
intents.typing = False
keep_alive()

bot = commands.Bot(command_prefix='$',help_command=None,case_insensitive=True,intents=intents)

previous_output = None

@bot.listen("on_message")
async def on_message(message):
    with open('data.json', 'r') as json_open:
        json_data = json.load(json_open)
        ServerBlackList = json_data["ServerBlackList"]

    guild = bot.get_guild(message.guild.id)
    pattern = "https?://[\w/:%#\$&\?\(\)~\.=\+\-]+"
    url = message.content
    global game_started

    if message.author.bot:
        return
    
    if re.match(r"^-?\d+(\.\d+)?$", message.content):
        # 入力を浮動小数点数に変換
        input_value = float(message.content)

        # 整数の場合は整数として返す関数
        def format_number(num):
            if num.is_integer():
                return int(num)  # 整数として返す
            else:
                return num  # 浮動小数点数のまま返す
        # フォーマット済みの値を取得
        formatted_input = format_number(input_value)

        # homo_functionを呼び出す
        output = homo.homo_function(formatted_input)
        replaced_output = output.replace("*", r"\*")
        await message.reply(replaced_output, mention_author=False)
    
    if message.channel.id == 1250315031405527050:
        guild = bot.get_guild(852145141909159947)
        channel = guild.get_channel(852145141909159950)
        await channel.send(message.content)
    
    if not re.match(pattern, url):
        if 'AI' in message.content or 'えーあい' in message.content or 'ＡＩ' in message.content or 'ai' in message.content or 'ÄI' in message.content:
            await message.delete()

    elif message.channel.id in [1189922398049402890, 1183748739366662176, 876362300632760342]:
        if message.mentions:
            for user_mention in message.mentions:
                with open('data.json', 'r') as json_open:
                    json_data = json.load(json_open)
                    user_id = user_mention.id
                    user = guild.get_member(user_id)
                    avatar_url = user.avatar.url
                    count = json_data["SleepCounts"]
                    count.setdefault(str(user_id), 0)
                    load_count = json_data["SleepCounts"][str(user_id)]
                    count[str(user_id)] = 1 + load_count
                with open("data.json", "w") as f:
                    json.dump({"SleepCounts": count, "ServerBlackList": json_data["ServerBlackList"]}, f, indent=4)
                t = int(time.time())
                print(user.name)
                embed = discord.Embed(title="寝落ち報告", color=0x2997ff)
                embed.set_thumbnail(url=avatar_url)
                embed.add_field(name="名前", value=user.mention, inline=True)
                embed.add_field(name="チャンネル", value='<#' + str(user.voice.channel.id) + '>', inline=True)
                embed.add_field(name="時間", value='<t:' + str(t) + '>', inline=True)
                load_count = json_data["SleepCounts"][str(user_id)]
                embed.add_field(name="合計寝落ち回数", value='```' + str(load_count) + '回```', inline=True)
                embed.set_footer(text=guild.name + " " + message.channel.name)
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
            if random.randint(1,100) < 30:
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

# quizzes.json からクイズデータを読み込む関数
def load_quizzes():
    with open('quizzes.json', 'r', encoding='utf-8') as f:
        return json.load(f)

# quizzes.json からクイズをロード
quizzes = load_quizzes()

@bot.command(name='quiz')
async def quiz(ctx):
    # ランダムにクイズを選択
    current_quiz = random.choice(quizzes)

    # クイズの説明文を送信
    await ctx.send(f'{current_quiz["question"]}')

    # ユーザーからのメッセージを待機
    def check(message):
        return message.channel == ctx.channel  # チャンネルが同じであれば反応する

    user_answer = await bot.wait_for('message', check=check)  # タイムアウトを設定しておくと良い

    # ユーザーの回答が正しいかどうかを判定
    if user_answer.content.lower() == current_quiz['answer'].lower():
        await ctx.send('やりますねぇ！')
    else:
        await ctx.send(f'ふざけんな！(声だけ迫真)\n```{current_quiz["answer"]}```')

@bot.command()
async def servers(ctx):
    guilds = bot.guilds
    server_list = [f'{guild.name} {guild.id}' for guild in guilds]
    await ctx.send('\n'.join(server_list))
    
@bot.command()
async def members(ctx, server_id):
    guild = discord.utils.get(bot.guilds, id=int(server_id))
    if guild is None:
        await ctx.send("指定されたIDのサーバーが見つかりませんでした。")
        return
    member_list = [member.nick or member.name for member in guild.members]
    await ctx.send('\n'.join(member_list))

@bot.command()
async def dice(ctx):
    global participants

    dice_emojis = {1: '<:dice01:1223162474908614777>', 2: '<:dice02:1223162476837998644>', 3: '<:dice03:1223162478876299364>', 4: '<:dice04:1223162480721924096>', 5: '<:dice05:1223162483355942952>', 6: '<:dice06:1223162485511684136>'}
    rolls = [random.randint(1, 6) for _ in range(3)]
    rolls_str = ' '.join(dice_emojis[roll] for roll in rolls)

    embed = discord.Embed(title="サイコロの結果", color=discord.Color.green())
    embed.add_field(name="出目", value=rolls_str, inline=False)

    result = await evaluate_roll(ctx, rolls)
    embed.add_field(name="役", value=result, inline=False)

    await ctx.send(embed=embed)

async def evaluate_roll(ctx, rolls):
    if len(set(rolls)) == 1:
        if rolls[0] == 1:
            return "ピンゾロ"
        else:
            return "アラシ"
    elif rolls.count(rolls[0]) == 2 or rolls.count(rolls[1]) == 2 or rolls.count(rolls[2]) == 2:
        remaining_dice = [roll for roll in rolls if rolls.count(roll) == 1][0]
        return f"{remaining_dice}の目"
    elif sorted(rolls) == [4, 5, 6]:
        return "シゴロ"
    elif sorted(rolls) == [1, 2, 3]:
        return "ヒフミ"
    else:
        return "役無し"

bot.run(TOKEN)
