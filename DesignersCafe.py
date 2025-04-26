import discord
from discord.ext import commands
from discord import app_commands
import matplotlib.pyplot as plt
import numpy as np
import io
from matplotlib import font_manager
import time
import dotenv
from keep_alive import keep_alive
import os


# .envファイルの読み込み
dotenv.load_dotenv()
keep_alive(port=8080)

intents = discord.Intents.all()
intents.members = True  # メンバー情報を取得可能にする
TOKEN = os.environ.get("TOKEN02")
bot = commands.Bot(command_prefix="!", intents=intents)

# 日本語フォントを設定する関数
def set_japanese_font():
    font_path = os.path.join(os.path.dirname(__file__), 'SourceHanSansJP-Heavy.otf')
    print(f"[DEBUG] フォントパス: {font_path}")
    if not os.path.exists(font_path):
        print("[ERROR] フォントファイルが見つかりません")
        return
    prop = font_manager.FontProperties(fname=font_path)
    print(f"[DEBUG] 読み込んだフォント名: {prop.get_name()}")
    plt.rcParams['font.family'] = prop.get_name()

# 棒グラフ画像を作成する関数
def create_bar_chart(data, title):
    labels = [x[0] for x in data]
    values = [x[1] for x in data]
    
    # 日本語フォントを適用
    set_japanese_font()

    fig, ax = plt.subplots(figsize=(16, 6))
    
    ax.barh(labels, values, color='skyblue')
    ax.set_xlabel('人数')
    ax.set_title(title)
    
    # 画像をメモリ上に保存して返す
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    return buf

@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f"Logged in as {bot.user}")

# 通話開始時間を記録するための辞書
call_start_times = {}

@bot.event
async def on_voice_state_update(member, before, after):
    # 参加時だけ反応するように条件を設定
    if before.channel is None and after.channel is not None:
        # 最初にボイスチャンネルに参加した時だけ通知を送る
        if len(after.channel.members) == 1:
            call_start_times[member.id] = time.time()  # 通話開始時間を記録

            # 通知を送るチャンネルID（テキストチャンネル）
            notify_channel_id = 1358429894719311912  # ←ご自身のチャンネルIDに置き換えてください
            notify_channel = bot.get_channel(notify_channel_id)
            ut = int(time.time())

            # 通話開始通知
            if notify_channel:
                embed = discord.Embed(
                    title="通話開始",
                    color=0x90b4de
                )
                embed.add_field(name="`チャンネル`", value=f"<#{after.channel.id}>")
                embed.add_field(name=f"`始めた人`", value=f"<@{member.id}>")
                embed.add_field(name="`開始時間`", value=f"<t:{ut}:f>")
                embed.set_thumbnail(url=member.avatar.url)
                await notify_channel.send("<@&1358431265396883707>", embed=embed)

    elif before.channel is not None and after.channel is None:
        # 通話が終了した時に通話時間を計算
        if member.id in call_start_times:
            start_time = call_start_times.pop(member.id)  # 通話開始時間を取得し削除
            end_time = time.time()  # 通話終了時間
            duration = end_time - start_time  # 通話時間（秒）

            # 時、分、秒に変換
            hours = int(duration // 3600)
            minutes = int((duration % 3600) // 60)
            seconds = int(duration % 60)

            # 通話時間を "00:00:00" 形式にフォーマット
            formatted_duration = f"{hours:02}:{minutes:02}:{seconds:02}"

            # 通話終了通知を送る
            notify_channel_id = 1358429894719311912
            notify_channel = bot.get_channel(notify_channel_id)

            if notify_channel:
                embed = discord.Embed(
                    title="通話終了",
                    color=0xd9a3cd
                )
                embed.add_field(name="`チャンネル`", value=f"<#{before.channel.id}>")
                embed.add_field(name="`通話時間`", value=formatted_duration)
                await notify_channel.send(embed=embed)

@bot.event
async def on_member_remove(member):
    # 通知を送るチャンネルID（テキストチャンネル）
    notify_channel_id = 1356114004845658284
    notify_channel = bot.get_channel(notify_channel_id)

    # 退出時刻の取得
    current_time = int(time.time())

    if notify_channel:
        embed = discord.Embed(
            title="サーバー退出通知",
            description=f"{member.name} さんがサーバーから退出しました。",
            color=0xd9a3cd  # 赤色
        )
        embed.add_field(name="`退出したユーザー`", value=f"<@{member.id}>")
        embed.add_field(name="`退出時間`", value=f"<t:{current_time}:f>")
        embed.set_thumbnail(url=member.avatar.url)  # 退出したユーザーのアイコン

        await notify_channel.send(embed=embed)

@bot.tree.command(name="send_charts", description="役職・性別の割合グラフを送信します")
@app_commands.describe(chart_type="送信するグラフの種類を選んでください（roles または gender）")
async def send_charts(interaction: discord.Interaction, chart_type: str):
    guild = interaction.guild

    if chart_type == "roles":
        role_names = [
            "サウンドクリエイター",
            "ビデオクリエイター",
            "プログラマー",
            "3Dアーティスト",
            "Webデザイナー",
            "イラストレーター",
            "UI/UXデザイナー",
            "グラフィックデザイナー"
        ]

        role_counts = []
        for role in guild.roles:
            if role.name in role_names:
                count = sum(1 for member in guild.members if role in member.roles)
                role_counts.append((role.name, count))

        chart_image = create_bar_chart(role_counts, "クリエイティブ分野割合")

        embed = discord.Embed(
            title="クリエイティブ分野割合",
            description="以下は各分野の割合を示した棒グラフです。",
            color=0x717fb0
        )
        embed.set_image(url="attachment://chart.png")

        await interaction.response.send_message(embed=embed, file=discord.File(chart_image, filename="chart.png"))

    elif chart_type == "gender":
        gender_roles = ["男性", "女性", "トランスジェンダー"]
        gender_counts = []
        for role in guild.roles:
            if role.name in gender_roles:
                count = sum(1 for member in guild.members if role in member.roles)
                gender_counts.append((role.name, count))

        chart_image = create_bar_chart(gender_counts, "性別割合")

        embed = discord.Embed(
            title="性別割合",
            description="以下は性別の割合を示した棒グラフです。",
            color=0x717fb0
        )
        embed.set_image(url="attachment://chart.png")

        await interaction.response.send_message(embed=embed, file=discord.File(chart_image, filename="chart.png"))

    else:
        await interaction.response.send_message("無効なグラフタイプです。roles または gender を指定してください。", ephemeral=True)

bot.run(TOKEN)  # 実際のBotトークンに置き換えてください
