import os
import discord
import random
import asyncio
from asyncio import sleep as s
from discord.ext import commands, tasks
from discord import member

TOKEN = os.getenv('DISCORD_TOKEN')
bot = commands.Bot(command_prefix='!')
status = 'pasta'

@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')

@bot.command()
async def ping(ctx):
    await ctx.send(f':upside_down: Pong! {round(bot.latency*1000)}ms')

def convert(time):
    units = ["s", "m", "h", "d"]
    convertt = {"s" : 1, "m" : 60, "h" : 3600,"d" : 3600*24}
    unit = time[-1]
    if unit not in units:
        return -1
    try:
        v = int(time[:-1])
    except:
        return -2
    
    return v * convertt[unit]

@bot.command()
async def remind(ctx, time, *content):
    seconds = int(convert(time))
    list_content = list(content)
    listToStr = ' '.join(map(str, list_content)) 
    await s(seconds)
    embed = discord.Embed(title = "Reminder:", description = f'**```{listToStr}```**', color = ctx.author.color)
    embed.set_footer(icon_url = ctx.author.avatar_url, text = f"Requested by {ctx.author.name}")
    await ctx.send(ctx.author.mention, embed=embed)

bot.run(TOKEN)
