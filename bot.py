import os
import discord
from asyncio import sleep as s
from discord.ext import commands
import platform
from datetime import datetime


TOKEN = os.getenv('DISCORD_TOKEN')
bot = commands.Bot(command_prefix='!')
launch_time = datetime.datetime.utcnow()
status = 'pasta'

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user.name}")
    print(f"Discord.py API version: {discord.__version__}")
    print(f"Python version: {platform.python_version()}")
    print(f"Running on: {platform.system()} {platform.release()} ({os.name})")
    print("-------------------")

@bot.command()
async def ping(ctx):
    await ctx.send(f':upside_down: Pong! {round(bot.latency*1000)}ms')
    
@bot.command(name="Whois",aliases=["userinfo"], help=f'Shows information of a user')
async def whois(ctx,user:discord.Member=None):
    user_mention = user or ctx.author
    embed=discord.Embed(title = f"{user_mention}", timestamp=ctx.message.created_at)
    embed.add_field(name="Status:",value=f"{user_mention.raw_status.capitalize()}",inline=True)
    embed.add_field(name="Nickname:",value=f"{str(user_mention.nick)}",inline=True)
    embed.add_field(name="User ID:",value=f"{user_mention.id}",inline=False)
    embed.add_field(name="Joined server:",value=f"{user_mention.joined_at}",inline=False)
    embed.add_field(name="Account made:",value=f"{user_mention.created_at} ago",inline=False)
    embed.set_thumbnail(url=str(user_mention.avatar_url)) 
    author_avatar=ctx.author.avatar_url
    embed.set_footer(icon_url= author_avatar,text=f"Requested by {ctx.message.author} • {bot.user.name} ")
    await ctx.reply(embed=embed)

@bot.command(name="ServerInfo",aliases=['serverstats','server'], help=f'Finds server stats')
async def stats(ctx):
        embed=discord.Embed(title=f"{ctx.guild.name}",timestamp=ctx.message.created_at)
        embed.add_field(name="Name",value=f"{ctx.guild.name}",inline=False)
        embed.add_field(name="Region",value =f"{str(ctx.guild.region).capitalize()}" ,inline=False)
        embed.add_field(name="Owner",value =f" {str(ctx.guild.owner)}" ,inline=False)
        embed.add_field(name="ID",value =f"{ctx.guild.id}",inline=False)
        embed.add_field(name="Roles",value=f"{len(ctx.guild.roles)}",inline=False)
        embed.add_field(name="Features" ,value= f"{(', '.join(x.lower().capitalize().replace('_',' ') for y, x in enumerate(ctx.guild.features))) or 'None'} ",inline=False)
        embed.add_field(name="Created" ,value= f"{ctx.guild.created_at} ago",inline=False)
        embed.set_thumbnail(url=str(ctx.guild.icon_url)) 
        embed.set_footer(icon_url=ctx.author.avatar_url,text=f"Requested by {ctx.message.author} • {bot.user.name} ")
        await ctx.reply(embed=embed)

@bot.command(name="Uptime",help=f"Shows the amount of time the bot has been up.")
async def uptime(ctx):
    await ctx.reply("I have been up from",launch_time.strftime("%b %d %Y %H:%M:%S"))

@bot.command(name="Avatar",aliases=['dp', 'pfp','av'], help=f'Shows the avatar of a user')
async def pfp(ctx,user:discord.Member=None):
    user_mention= user or ctx.author 
    embed=discord.Embed(title = f"Avatar of {user_mention.name}", timestamp=ctx.message.created_at)
    embed.set_image(url=user_mention.avatar_url)
    author_avatar=ctx.author.avatar_url
    embed.set_footer(icon_url= author_avatar,text=f"Requested by {ctx.message.author} • {bot.user.name} ")
    await ctx.send(embed=embed) 



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

@bot.command(help = "Syntax : !remind <insert time here(use s/m/h/d)> <insert reminder here>")
async def remind(ctx, time, *content):
    seconds = int(convert(time))
    list_content = list(content)
    listToStr = ' '.join(map(str, list_content)) 
    await s(seconds)
    embed = discord.Embed(title = "Reminder:", description = f'**```{listToStr}```**', color = ctx.author.color)
    embed.set_footer(icon_url = ctx.author.avatar_url, text = f"Requested by {ctx.author.name}")
    await ctx.send(ctx.author.mention, embed=embed)

@bot.command(help = "Syntax : !embed <insert title here> ^ <insert description here>")
async def embed(ctx):
    g = ctx.message.content
    a = g.replace('!embed','')
    title, desc = a.split('^')  
    embed = discord.Embed(title = title, description = desc, color = ctx.author.color)
    embed.set_footer(icon_url = ctx.author.avatar_url, text = f"Requested by {ctx.author.name}")
    await ctx.send(embed=embed)

bot.run(TOKEN)
