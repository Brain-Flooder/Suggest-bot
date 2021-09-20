import os
import discord
from discord.ext import commands
from discord.ext.commands import has_permissions, MissingPermissions
import keep_alive

bot = commands.Bot(
	command_prefix="m!",  # Change to desired prefix
	case_insensitive=True,  # Commands aren't case-sensitive
  help_command = None
)

bot.author_id = 884289856325447680  # Change to your discord id!!!

yay=discord.Embed(color=0x70ff66)

@bot.event 
async def on_ready():  # When the bot is ready
    print("I'm in")
    print(bot.user)  # Prints the bot's username and identifier
    await bot.change_presence(activity=discord.Game(name=f"{bot.command_prefix}help"))
    
    
emoji = '\N{THUMBS UP SIGN}'
@bot.command(name = 'suggest',aliases=['sg'])
async def suggest(ctx,*,idea):
    embedVar = discord.Embed(title=f"{ctx.author}, ID: {ctx.author.id}", description=idea, color=0x6FB9FF)
    with open('channel.txt')as f:
        for hey in f:
          hey=int(hey)
          channel = ctx.guild.get_channel(hey)
          if channel is not None:
            hmm = await channel.send(embed=embedVar)
            cross = '\N{THUMBS DOWN SIGN}'
            checkM = '\N{THUMBS UP SIGN}'
            await hmm.add_reaction(checkM)
            await hmm.add_reaction(cross)
    embedBreh = discord.Embed(title='Sent',value='Your suggestion has been sent!')    
    await ctx.send(embed=embedBreh)
          
@bot.command()
@has_permissions(manage_messages=True)
async def approve(ctx,id:int):
    global yay
    huh = await ctx.fetch_message(id)
    await huh.reply(f'{ctx.author.mention} Your suggest has been approved!')
    await huh.edit(content='Approved!')
    

@bot.command()
@has_permissions(manage_messages=True)
async def decline(ctx,id:int):
    global yay
    huh = await ctx.fetch_message(id)
    await huh.reply(f'{ctx.author.mention} Your suggest has been declined!')
    await huh.edit(content='Declined.')

@bot.command()
async def help(ctx):
    embed=discord.Embed(title="My command", description="Yep, my command", color=0x8fabff)
    embed.add_field(name="m!suggest [idea]", value='Suggest idea to set up channel', inline=True)
    embed.add_field(name='m!setup {channel ID}', value='Set up to a specific channel (If no ID, it will set the channel you are in as post channel)', inline=True)
    embed.add_field(name='m!approve [message ID]', value='Approve a suggest and ping the author', inline=True)
    embed.add_field(name='m!decline [message ID]', value='Decline a suggest and ping the author', inline=True)
    embed.set_footer(text='{} is optional, [] is required')
    await ctx.send(embed=embed)

@bot.command()
@has_permissions(manage_channels=True)
async def setup(ctx,id=None):
    if id is None:
        with open('channel.txt','a') as f:
            f.write('\n')
            f.write(str(ctx.channel.id))
    else:
        with open('channel.txt','a') as f:
            f.write('\n')
            f.write(id)
    embedVar = discord.Embed(title="Set up done!",color=0x85C4FF)
    await ctx.send(embed=embedVar)

@bot.command(name='setapprove',aliases=['setAp'])
@has_permissions(manage_channels=True)
async def setupApprove(ctx,id=None):
    if id is None:
        with open('yay.txt','a') as f:
            f.write('\n')
            f.write(str(ctx.channel.id))
    else:
        with open('yay.txt','a') as f:
            f.write('\n')
            f.write(id)
    embedVar = discord.Embed(title="Set up done!",color=0x85C4FF)
    await ctx.send(embed=embedVar)

@bot.command()
async def info(ctx):
    embedVar = discord.Embed(title='Basic info',color=0x6FB9FF)
    embedVar.add_field(name='About bot', value="This bot made by <scoboo>#9985 (this guy is kinda suck). I want to help server can get suggestion from their user easier. That is why I'm here to help server owner and staffs what members think about their server",inline=False)
    embedVar.add_field(name='I got a bug', value="This bot made in a short time so it can have some bugs. You can join https://discord.gg/t9eH5yuMR4 for more help.")
    embedVar.set_thumbnail(url="https://cdn.discordapp.com/attachments/886161040247758878/888398168209895434/Untitled.png")
    await ctx.send(embed=embedVar)

@setup.error
async def error(ctx, error):
    if isinstance(error, MissingPermissions):
        text = f"Sorry {ctx.author.mention}, you do not have permissions to do that!"
        await ctx.send(text)

print(discord.__version__)
keep_alive.keep_alive()
my_secret = os.environ['token']
token = 0
bot.run(my_secret)  # Starts the bot