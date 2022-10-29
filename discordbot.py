import discord
import traceback
from discord.ext import commands
from os import getenv
import os
import psycopg2

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='/', intents=intents)

DATABASE_URL = os.environ.get('DATABASE_URL')
conn = psycopg2.connect(DATABASE_URL)
cur = conn.cursor()

cur.execute("select * from kaikei")
results = cur.fetchall()
member_payment_dict = {}
for (member, payment) in results:
    member_payment_dict[member] = payment
    
async def get_member_payment_srt():
    return '\n'.join("{0}:{1}".format(member,payment) for (member,payment) in member_payment_dict.items())

@bot.event
async def on_command_error(ctx, error):
    orig_error = getattr(error, "original", error)
    error_msg = ''.join(traceback.TracebackException.from_exception(orig_error).format())
    await ctx.send(error_msg)

@bot.command()
async def ping(ctx):
    await ctx.send('pong')

@bot.command()
async def add(ctx, arg):
    member = str(ctx.author.name)
    if member not in member_payment_dict.keys():
        cur.execute("INSERT INTO kaikei values ('{0}', {1})".format(member,0))
    else:
        new_payment = member_payment_dict[member] + int(arg)
        member_payment_dict[member] = new_payment
        cur.execute("update kaikaie set paymenr = {1}, where name = '{0}'".format(member,new_payment))
    await ctx.send(get_member_payment_srt())
    
@bot.command()
async def test(ctx):
    await ctx.send(ctx.author.name)
    
@bot.command()
async def read(ctx):
    cur.execute("select * from kaikei")
    results = cur.fetchall()
    member_payment_dict = {}
    for (member, payment) in results:
        member_payment_dict[member] = payment
        
@bot.command()
async def show(ctx):
    await ctx.send(get_member_payment_srt())

token = getenv('DISCORD_BOT_TOKEN')
bot.run(token)

