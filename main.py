import pymysql
import discord
from datetime import datetime
from discord.ext import commands

database = "discordauth"
table = "player_auth_value"

connection = pymysql.connect(host="localhost", user="root", password="qlalfqjsgh", db=database, charset="utf8",
                             autocommit=True)

intents = discord.Intents.all()

bot = commands.Bot(command_prefix="!", intents=intents)

main_channel_id = 949892001355141123
test_channel_id = 1014858948559503481

token = "MTAxNzgyOTI4Mjg4MzU4MDA2NA.GTU6_w.m7J2OXye6dUE6VvcP-stTpdKOzziPnwwHDWYrw"

now = datetime.now()

@bot.event
async def on_ready():
    state_message = discord.Game("인증 시스템 동작")
    await bot.change_presence(status=discord.Status.online, activity=state_message)


@bot.event
async def on_message(message):
    member = message.author
    if member.bot:
        return
    if message.channel.id != 1017830426645123204:
        return

    now_time = f"{now.year}년 {now.month}월 {now.day}일 {now.hour}시 {now.minute}분 {now.second}초"
    embed = discord.Embed(title=f"인증 완료",
                          description=f"서버에 오신 것을 환영합니다!",
                          color=0xFF0000)

    await message.delete()
    select = f"select * from {table} where code = '{message.content}'"
    with connection.cursor() as cursor:
        success = cursor.execute(select)

        if success != 1:
            return

        result = cursor.fetchall()
        for value in result:
            embed.add_field(name="UUID", value=f"{value[0]}", inline=False)
            if value[2] == "인증":
                return

        update = f"update {table} set state = '인증' where code = '{message.content}'"
        success2 = cursor.execute(update)
        if success2 == 1:
            await member.add_roles(discord.utils.get(member.guild.roles, name="권한한"))
            dm = await member.create_dm()
            embed.add_field(name="코드", value=f"{value[1]}", inline=False)
            embed.set_footer(text=f"{message.guild.name} | {now_time}")
            await dm.send(embed=embed)

bot.run(token)
