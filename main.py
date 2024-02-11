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
    if message.author.bot:
        return

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

# クイズデータをリストで管理
quizzes = [
    {"question": "ワロタと同意義だが、何故かこっちを使いたくなる。\n出典は枕草子。", "answer": "わろし(古文)"},
    {"question": "聖地で生まれた伝説のワード。\n意味は詳しくは判らないが、恐らく「よく言うぜ」みたいな相手が過言を言ったときに使う言葉だと考察班は予想している。", "answer": "いうほどいう"},
    {"question": "考察班が一番好きなワード。意味は分からん。(絶望)\n恐らく、脅しのワードとして「キン○マ潰すぞ」という意味なのだろうが、謎の敬語と語呂の良さも相まって、人気を博している。", "answer": "しこたま踏ませて頂きます(迫真)"},
    {"question": "三角比に翻弄されたﾀｸが、怒りを露わにして放ったストレートな暴言。\n彼が反数学主義に傾倒し、数学大国・インドと戦争を始めるのも時間の問題だろう。", "answer": "sin180°、死ね"},
    {"question": "まさるさんの授業中、PCのスクリーンに映ったある文章がどこにあるかを探していたクラスメイトに対して、ﾀｸが放った一言。\n「左から2番目」を示そうとしていたらしいが、極端に簡略化された結果、こうなってしまった。", "answer": "左の右"},
    {"question": "クラスメイトに突如としてぶたれ、平和を希求したﾀｸが放った言葉。\n安易に「平和」という単語を使うことをあえて避け、パシフィストとして知られる■■■■の名を三回唱えることで、暴力への反対を唱える表現技法には感嘆せざるを得ない。\nきっと、喧嘩なんてしない寛大な心の持ち主なのだろう、彼は。", "answer": "ガンディー、ガンディー、ガンディー！"},
    {"question": "数学のテストにて、「18」という数字に惑わされてしまったﾀｸ。\n暴力による解決を強く求め、遂に宣戦を布告した。\n人間が相手なら持ち前のパワーでねじ伏せられそうだが、「18」という概念と戦うとなると話は変わってくる。\n一体、どのような頭脳戦が展開されるのだろうか。", "answer": "一回18と喧嘩するわ(宣戦)"},
    {"question": "またもや舌足らず語録。\nネクタイを3掛も付けたクラスメイトに対して放たれた。なんか、弱そうである。", "answer": "ケロベロス"},
    {"question": "舌足らず語録。\n「■■■■■■」と言いたかったのだろうが、「な」が入ってしまった。", "answer": "さなげすまれた"},
    {"question": "「羅生門」のあらすじを説明していたﾀｸによって生み出された。\n「屋根裏」や「天井裏」と同義であると考えられる。", "answer": "上裏"},
    {"question": "期末テストにて、直前に勉強した「羅生門」が範囲外であることを知ったﾀｸが、その著者である芥川龍之介に対して放った一言。\n「羅生門」を範囲に指定しなかった教師ではなく、その作品の著者に恨みを抱いているところが何ともﾀｸらしい。\n勉強した分野が範囲と違っていた場合に使ってみよう。", "answer": "芥川―！(絶叫)"},
    {"question": "「お前がy軸じゃ」の説明を求められたﾀｸが、それについて熱弁している際に放たれた言葉。\n再編版「お前がy軸じゃ」の「相手をy軸とみなした」という考察は正しかったということが判明したと同時に、自身をx軸とも認識していたということが分かる。\n語録考察界に激震をもたらした一言。", "answer": "俺がxでお前がy"},
    {"question": "方位磁針の呼び方が三つもあることに混乱したﾀｸが吐き捨てた台詞。\nどこか都市伝説的で、どこかノスタルジックな、そんな絶妙な印象を聞き手に持たせる、\"鏡\"という単語をものの数秒で繰り出すワードセンスには畏敬の念を示したい。", "answer": "三面鏡や(諦観)"},
    {"question": "「siuが女と歩いているのを目撃した」との情報に盛り上がっていた際に放たれた。\n「磁石」ならまだしも、「方位磁石」なのが理解できない。お相手は南極点なのだろうか。", "answer": "小瀧は方位磁石だって！(確信)"},
    {"question": "ﾀｸ's intonationによって歪められてしまった、悲劇の産物。\nアクセントは「時期尚早」と同じである。\n某先輩の語録と発音が酷似しているため、FF外BOTの影響であるという説が有力だ。", "answer": "気↑に↓せんの"},
    {"question": "突拍子もないことを言ったクラスメイトに対して、ﾀｸが放った一言。\n恐らく、「お前の知能指数はサボテンと同等だ」という意味だと考えられる。", "answer": "サボテンと知能、並ばってる"},
    {"question": "ﾀｸが特定のキャラに向けて放った、性的嗜好の奥深くから露呈した言葉。\nただのwant to構文に見えるが、その言葉を連呼するﾀｸが何故か悍ましい。\nあたかも\"舐めたい\"という感情を抱くのが当然であるかのように連呼する。連呼する。連呼する。\n正気の沙汰とは思えない、11/14の深夜であった。", "answer": "\"舐めたい\""},
    {"question": "前戯中、ベルトに棒が当たって出してしまった男性の話をしたﾀｸが、その男性に対して放った言葉。\n「いうほどいう」とどこか同じ香りがする。\n意味は「情けない」とそこまで変わらないと思われる。本人曰く、形容詞らしい。", "answer": "情けない情け"},
    {"question": "模試終了後、モンストの話をしている際に放たれた言葉。\n某ホストは「俺か、俺以外か」と語ったが、ﾀｸは違う。\nこの『しょうや』という人物は、ﾀｸと互角に戦える唯一の人物なのかもしれない。", "answer": "俺か、しょうやか、それ以外か"},
    {"question": "廊下にて、歪んだ鞄を見たﾀｸが呟いた一言。無論、中に人はいない。\n「死体が入っている」とは言わずに、「人殺してる」と形容するセンスにはどこか文豪のような一面を感じられる。", "answer": "鞄の中で人殺すな(糾弾)"},
    {"question": "ある一人の男子生徒が論理・表現の授業中、「これ■■だな」と何回も発言した。\n軽々しく■■という言葉を使ったクラスメイトに対して憤怒したﾀｸは「■■■■■■■」と彼を怒鳴りつけた。\n語録の中では珍しく、文法的にも表現的にも歪みが見られない。", "answer": "二択の保証しろ"},
    {"question": "指スマに勝利するも、恨みを買ってしまったがために腹パンされ地面に倒れ込んだﾀｸが発言した言葉。\n英語では「理解した」という意味であるが、もちろんﾀｸ's worldにおいてそんなものは通用しない。彼は常に文化を上書きしていく。", "answer": "I got it... (悶絶)"},
    {"question": "語録の中では比較的、常人が理解しやすいワード。\n「IQが高い」の誤用…ではなく、上位互換であると考えられている。\n汎用性も高いため、積極的に使っていきたい。彼の創造した言葉を使用することが、ﾀｸ's worldを理解することへの第一歩となるだろう。", "answer": "IQが良い"},
    {"question": "山地から何としてでもスマホを強奪しようとしていたﾀｸ。圧倒的な筋力と俊敏な動きに恐れ慄いた山地は、思わず息を漏らしてしまう。\nその息遣いが彼には妊婦の悲痛な喘ぎに聞こえたのだろう。狂気であるとしか形容できない隠喩法。16年もの間、磨かれ続けてきた彼の美的感覚は遂に禁じられた領域へと突入する。彼の深層心理に潜む異常性が垣間見える一言だ。\nこの危険すぎる表現方法を拡散させてはいけないという戒めとして、上記のような評価をさせて頂く。", "answer": "やまじ陣痛？(尋問)"},
    {"question": "山地とスマホ卓球を楽しんでいたﾀｸ。真正面に鋭いストレートを放つも、更に速いスピードで返されてしまう。山地が勝利を確信した瞬間、その言葉は唐突に現れた。\n少なくとも私には、彼が脊髄反射でかの言葉を発したかのように感じられた。前世はスラム街の売春婦だったのだろうか。真相は液晶に映るピンポン玉と共に消えていった。", "answer": "妊娠するって！(畏怖)"},
    {"question": "ビスコに課題を写したか、と疑われてしまったﾀｸ。「それはﾀｸだから...」と彼を嘲り笑うジョウバ。数秒の沈黙の後、事件は発生した。\n激昂したﾀｸは、ジョウバを窓際へと連行し、目にも留まらぬ速さで網戸を開け、大空を指さしてこう言い放った。", "answer": "今日から11HRは15人になります(通告)"},
    {"question": "次は選択授業。移動教室をしている際、突如として二人は口論をし始めた。俺はお前と同類じゃない、と熱く語るジョウバ。それに対し、お前は同類だと言って譲らないﾀｸ。五分五分かと思われた闘いは、常軌を逸した口頭表現によって一気に決着を付けられた。「■■■■■■■■■」時間が止まったかのような衝撃を受けた。いや、恐らく本当に止まっていただろう。唖然とするジョウバを気にも留めず、彼の足は颯爽と書写室のある別棟へ向かっていった。", "answer": "お前も同類項じゃ"},
    {"question": "「ドキドキ文芸部！」をプレイしている際、様子がおかしく詩を見せようとしないサヨリに対して放った言葉。けんは小一時間ほど虚無連打をしていた為、眠く、そして退屈であった。そんな中迎えた3回目の見せ合いタイム。私のもう飽きているだろうという偏見は、突然の一言により完璧に崩れ去ったのだ。心はすっかり文芸部になっていたけんせい。今後の展開にぜひご注目いただきたい。", "answer": "はやく詩をみせろよぉぉぉぉ！！！(迫真)"},
    {"question": "けんのギャンブル敗北によって突発で始まったエンドラRTA。順調なスタートダッシュを決めるざるそば選手だったが、ネザー要塞探索中にまさかの落下死。村にデスポーンし、エンドラ討伐は不可能かと思われたその時、半ばやけくそのように嘆いた。", "answer": "ここあるよ(断定)"},
    {"question": "稲葉宅へ向かっている道中、皆で思い出話に花を咲かせる中、感情を昂らせながら放った一言である。\nこの語録は研究が比較的進んでおり、最有力説では\"いずれかの感情が既存の言葉では表現しきれない程高揚した際、オーバーフローを防ぐための危機回避的な語録\"と唱えられている。", "answer": "危機毛髪"},
    {"question": "期末テスト当日の昼休み、5限目の理科に備えて各々が勉強している雰囲気に便乗しようとした私達に放った、容赦ない一言である。恐らく、\"直前に勉強しても意味がない\"という意味だろうが、これが分からない。何故\"■■\"なのか？何故この文字の羅列で表現しようと思ったのか？正にﾀｸ's world。我々常人には理解し難い領域である。", "answer": "はなに念仏(決然)"},
    {"question": "B組で過ごすﾀｸが、自分を活かせる環境を嘆いた一言。即ち、千陽先生ではなく山田先生がよかったとﾀｸのツンデレな一面が垣間見えているという事である。日本語の関係上、このような表現様式には限界がある為、語録の中ではかなりマシな方ではないだろうか。", "answer": "(しんじちはるに)踏み躙しされた"},
    {"question": "とある日の昼休み、屋外でバレーボールを楽しんでいた際、ﾀｸが打ったボールを拾えなかった時に生まれてしまった言葉。\n恐らく、ﾀｸ語録の中でもトップクラスのインパクトと不可解さを持つ語録であろう。\nこの言葉を見た時、頭の中が？で埋め尽くされたと思う。だが安心してほしい。私は語録の解説を始めて一年ほど経つが、これほど意図を汲み取れない語録と出会うのは初めてである。\nﾀｸの表現技法は常軌を逸している、一線を画していると再認識させられた、なんとも奇抜な一言だ。", "answer": "お前がy軸じゃ"},
    {"question": "麻雀対局中、ﾀｸが槓した時にヤケクソで放った一言。\n麻雀では手牌に同じ牌が4つあるときに槓をすることが出来るが、門前状態でなくなる所謂”鳴き”の一種である。鳴く事で立直できなくなるため、必然的にアガれる役がない”■■”という状態に陥ってしまう。だから■■■■、ある意味嘆きとも取れる言葉である。 \n必要ない槓をした時、ヤケクソになりながら使ってみよう。", "answer": "無役確定！"},
    {"question": "ﾀｸの友達が不祥事を起こし、問い詰められている時に放った言葉。\n普通語では無くこちらを使いたいが、一般会話で使用すると怪訝な目で見られる可能性があるため、使用はくれぐれも身内のみで。", "answer": "誤魔化せろ"},
    {"question": "久々の語録。小針氏との友情をアピールしたかったようだが、言語学者もビックリの迷言である。\n友情~YO-JYOのように、「手を握り合った」なら通じるだろう。■...?\n小針氏とけんがそれぞれ拳をギュッとしている場面を想像すると、なかなかにシュールである。", "answer": "拳を握り合った(自明)"},
    {"question": "けんの衝撃のジェノサイド発言。ガンダムかなろう系でしか聞いたことのない言葉がけんの口から飛び出した。この語録が生まれた経緯を説明する。考察班とsiuが天皇の家系について会話を咲かせていた。なんと天皇は124代も続いているそうである。だが、2000年も歴史がある中で、天皇が124回も入れ替わることに疑問を覚え、悶々としていた最中にその言葉は飛び出した。", "answer": "殺したんだよ、僕が"},
    {"question": "ﾀｸの紳士的な面が垣間見えた一言。昔は強かったけど今は...というキャラに向けて放った言葉である。環境の変化、所謂インフレはどのゲームにもつきものである。その変化についていけなかったキャラは、相対的に見て「弱い」と結論づけられ、プレイヤーの手から遠ざかってしまう。そんなキャラに向けて放った、この「■■■■」。決して見放す事なく、昔の功績を讃えて国宝と位置付け、敬う。1キャラ1キャラに真剣に向き合うその姿勢は、性能ばかりを追い求めている現代ソシャゲプレイヤーが見習うべきものではないだろうか。", "answer": "過去国宝"},
    {"question": "「超究極」カイドウにて、ギミックモンスターであるｲｯﾇに攻撃力減少(所謂デバフ)をかけられた時に発した、悔しさを滲ませた一言。FPS等で「痛っ」と言ってしまうのは良くある話だが、モンストにまで自分を没入させている人が居るなんて思いもしなかった。", "answer": "デバフを感じる"},
    {"question": "長きに渡る激戦の末、「超究極」カイドウを撃破した時に放った言葉。当時は3人とも膨大な達成感に包まれており、あまりの幸せさに文が乱れてしまったのだと考えられる。ﾀｸが感動する事は滅多にないので、この評価にしている。", "answer": "左目から涙"},
    {"question": "ざるそば絡みで放った一言。\n「■■■■■■」だけならまだ良かったものの、「■■■■■」が全てを台無しにしている。謎に語感がいいのが余計謎を深めている。\n用法は、主に悪口等自分が不満に思った時に使用する。", "answer": "ハラスメント・モーメント"},
    {"question": "聖地にて、しまじろう氏にセクハラをしていたﾀｸが放った、恐らくこの世に存在してはいけないワード。\n正直、このワードを言葉で解説する事すら許されないだろう。\nこれを聞いた瞬間、身体中に電撃が走ったのを今でも覚えている。\n\"■\"という少し和みのある二人称から、\"■■■■\"という方言じみた言葉に繋げるまでの流れが完璧で、語録の中でも常軌を逸する作品である。\n\"■\"　\"■■■\"　\"■■\"　\"■■■■\"\nこのワードセンスを持ち、ましてやこれを一瞬で言葉にできる人間など世界に存在するのだろうか。\n何から何まで美しいこの語録は、未来永劫受け継がれるだろう。", "answer": "君の白玉粉、純白に染めたる(迫真)"},
    {"question": "聖地にて、怒ったﾀｸが威厳のある声で放った一言。\nこの比喩表現には、考察班も思わず\"うつくしい…\"と声が出てしまった。\nﾀｸの才能が発揮された珍しい語録である。 ", "answer": "血液が暴れている…(戦慄)"},
    {"question": "聖地にて、ちょっかいをかけられたﾀｸが放った笑撃の一言。\n本人は\"■■にして返してやる\"\nと言いたかったのだろうが、滑舌の悪さが相まって生まれてしまった。\n本来の意味はﾀｸが言おうとしたことと変わりないが、年月が流れていくうちに\"■■にして返してみろよ・やってみろよ\"という挑発っぽい意味合いになってしまった。\n相手がイキったときに使ってみよう。", "answer": "ニ倍夜叉！(奥義)"},
    {"question": "聖地にて、ﾀｸが音割れで放った一言。\n生徒会長に鬱憤を晴らすときに言ってみよう。\nﾀｸが音割れで言葉を放つと、大抵面白くなるのである。", "answer": "ゆ゛る゛さ゛な゛い゛！"},
    {"question": "出ました意味不明単語。\nこれはもう ﾀｸ's wouldで生み出されたものなので、考察班はこれ以上深追いするのをやめた。", "answer": "心の底から心が痛い"},
    {"question": "間違っていた意見を矯正させるために使うワード。\n相手が間違っており、ﾀｸが合っている場面は少ないので、レアワードと化している。\nみんなも揚げ足を取るときに使ってみよう。", "answer": "やんな？(強調)"},
    {"question": "またもや三角比に弄ばれたﾀｸが、ジョウバに突っ込まれた際に放った言葉。なぜ■■■■■■なのか、なぜ「■■■■」のかは理解不能である。\n「今日から11HRは15人になります(通告)」と同様の意味を持つと考えられる。", "answer": "ド・モルガンと寝させるぞ(脅迫)"},
    {"question": "歴史総合で■■■■を学んだ直後の休み時間に、ﾀｸによって放たれたワード。残りの1割は何なのだろうか。\n極めてセンシティブな話題のため、十分注意を払って使用しよう。", "answer": "90%優生思想"},
    {"question": "現代国語の授業中、山地の解いているワークを見に来たﾀｸ。一つ一つの文字をまじまじと見つめた直後、その言葉は放たれた。\n丸付けの際、山地のワークに特に目立った間違いはなかったため、日本語とﾀｸ's vocabularyの乖離が見受けられる。", "answer": "お前接続詞知らないだろ(名推理)"},
    {"question": "まさるさんと好きなアーティストについて談笑していた際に放たれたワード。\n一体、彼はなぜ「■■■」を名字として捉えているのだろうか。（長いので割愛）", "answer": "タツヤに合う下の名前は存在しない(断言)"},
    {"question": "グループワーク中、突如としてﾀｸが放ったとされる言葉。しかしながら、このワードはﾀｸ本人から発言の否定がされており、存在自体の有無が議論されている。\nだが、私は確かに耳にしたのだ。隣のグループから「■■■■■■■■■■。」と意気揚々に語るﾀｸの声を。", "answer": "俺が最初の堂ヶ島じゃ(自白)"},
    {"question": "ツムツムのパチンコエルサに大敗北したﾀｸ。神に祈ることこそがパチエルで荒稼ぎする最適解だと判断したﾀｸは、エジプトの冥界神である■■■■にその身を捧げた。\n…が、「■」が抜けてしまった。「■■■」へと変わってしまった。冥界神ではなく、冥界そのものを崇拝してしまったﾀｸ。今後、彼の身に何か不幸が訪れないことをただ祈るばかりだ。", "answer": "アビス(奈落崇拝)"}
]


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


bot.run(TOKEN)
