import os
import discord
from discord.ext import commands
from discord.ext.commands import has_permissions, MissingPermissions
import keep_alive
from discord_slash import SlashCommand, SlashContext

bot = commands.Bot(
	command_prefix="m!",  # Change to desired prefix
	case_insensitive=True,  # Commands aren't case-sensitive
  help_command = None,
  intents=discord.Intents.default()
)

slash = SlashCommand(bot, sync_commands=True)

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
    embedVar = discord.Embed(title=f"User with ID: {ctx.author.id} suggest: ", description=idea, color=0x6FB9FF)
    with open('channel.txt')as f:
        for hey in f:
          hey=int(hey)
          channel = ctx.guild.get_channel(hey)
          if channel is not None:
            hmm = await channel.send(content=ctx.author.id,embed=embedVar)
            cross = '\N{THUMBS DOWN SIGN}'
            checkM = '\N{THUMBS UP SIGN}'
            await hmm.add_reaction(checkM)
            await hmm.add_reaction(cross)
            await ctx.message.delete()
    embedBreh = discord.Embed(title='Sent',value='Your suggestion has been sent!')    
    await ctx.send(embed=embedBreh)
          
@bot.command(name='approve',aliases=['ap'])
@has_permissions(manage_messages=True)
async def approve(ctx,id:int):
    global yay
    huh = await ctx.fetch_message(id)
    member = huh.content
    member = int(member)
    user = await bot.fetch_user(member)
    await huh.reply(f'Suggest is approved!')
    await huh.edit(content=f'{user.mention} Your suggest has been approved!')
    

@bot.command(name='decline',aliases=['dc'])
@has_permissions(manage_messages=True)
async def decline(ctx,id:int):
    global yay
    huh = await ctx.fetch_message(id)
    await huh.reply(f'{huh.author.mention} Your suggest has been declined!')
    await huh.edit(content='Declined.')

@bot.command()
async def help(ctx):
    embed=discord.Embed(title="My command", description="Yep, my command", color=0x8fabff)
    embed.add_field(name="m!suggest [idea]", value='Suggest idea to set up channel',inline=False)
    embed.add_field(name='m!setup {channel ID}', value='Set up to a specific channel (If no ID, it will set the channel you are in as post channel)',inline=False)
    embed.add_field(name='m!approve [message ID]', value='Approve a suggest and ping the author',inline=False)
    embed.add_field(name='m!decline [message ID]', value='Decline a suggest and ping the author',inline=False)
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

@bot.command()
async def info(ctx):
    embedVar = discord.Embed(title='Basic info',color=0x6FB9FF)
    embedVar.add_field(name='About bot', value="This bot made by Brain Flooder#9985 (this guy is kinda suck). I want to help server can get suggestion from their user easier. That is why I'm here to help server owner and staffs what members think about their server",inline=False)
    embedVar.add_field(name='I got a bug', value="This bot made in a short time so it can have some bugs. You can join [this] (https://discord.gg/t9eH5yuMR4 for more help).")
    embedVar.set_thumbnail(url="https://cdn.discordapp.com/attachments/886161040247758878/888398168209895434/Untitled.png")
    await ctx.send(embed=embedVar)

@setup.error
async def error(ctx, error):
    if isinstance(error, MissingPermissions):
        text = f"Sorry {ctx.author.mention}, you do not have permissions to do that!"
        await ctx.send(text)

@slash.slash(name='suggest',description='Suggest your idea')
async def _suggest(ctx,idea):
    embedVar = discord.Embed(title=f"Suggest from user with ID: {ctx.author.id}", description=f'{idea}', color=0x6FB9FF)
    with open('isban.txt')as file:
      for isBanned in file:
        isBanned = int(isBanned)
        if ctx.author.id != isBanned:
          with open('channel.txt')as f:
              for hey in f:
                hey=int(hey)
                channel = ctx.guild.get_channel(hey)
                if channel is not None:
                  hmm = await channel.send(content=ctx.author.id,embed=embedVar)
                  cross = '\N{THUMBS DOWN SIGN}'
                  checkM = '\N{THUMBS UP SIGN}'
                  await hmm.add_reaction(checkM)
                  await hmm.add_reaction(cross)
          embedBreh = discord.Embed(title='Sent',value='Your suggestion has been sent!')
          await ctx.send(embed=embedBreh)
        else:
          ctx.send("You have been banned from our system.")
          return 0

@slash.slash(name='info',description='Information about this bot')
async def _info(ctx):
    embedVar = discord.Embed(title='Basic info',color=0x6FB9FF)
    embedVar.add_field(name='About bot', value="This bot made by Brain Flooder#9985 (this guy is kinda suck). I want to help server can get suggestion from their user easier. That is why I'm here to help server owner and staffs what members think about their server",inline=False)
    embedVar.add_field(name='I got a bug', value="This bot made in a short time so it can have some bugs. You can join [this](https://discord.gg/t9eH5yuMR4) for more help.")
    embedVar.set_thumbnail(url="https://cdn.discordapp.com/attachments/886161040247758878/888398168209895434/Untitled.png")
    await ctx.send(embed=embedVar)

@slash.slash(name='approve', description='Approve a suggestion')
@has_permissions(manage_messages=True)
async def _approve(ctx,id):
    id=int(id)
    global yay
    huh = await ctx.fetch_message(id)
    member = huh.content
    member = int(member)
    user = await bot.fetch_user(member)
    await huh.reply(f'Suggest is approved!')
    await huh.edit(content=f'{user.mention} Your suggest has been approved!')
    

@slash.slash(name='decline', description='Decline a suggestion')
@has_permissions(manage_messages=True)
async def _decline(ctx,id):
    id=int(id)
    global yay
    huh = await ctx.fetch_message(id)
    await huh.reply(f'{huh.author.mention} Your suggest has been declined!')
    await huh.edit(content='Declined.')

@slash.slash(name='Help',description='Help')
async def _help(ctx):
    embed=discord.Embed(title="My command", description="Yep, my command", color=0x8fabff)
    embed.add_field(name="m!suggest [idea]", value='Suggest idea to set up channel',inline=False)
    embed.add_field(name='m!setup {channel ID}', value='Set up to a specific channel (If no ID, it will set the channel you are in as post channel)',inline=False)
    embed.add_field(name='m!approve [message ID]', value='Approve a suggest and ping the author',inline=False)
    embed.add_field(name='m!decline [message ID]', value='Decline a suggest and ping the author',inline=False)
    embed.set_footer(text='{} is optional, [] is required')
    await ctx.send(embed=embed)

@slash.slash(name='Setup', description='Set up channel that suggestions will be sent to it')
@has_permissions(manage_channels=True)
async def _setup(ctx,id=None):
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

@slash.slash(name='invite',description='My invite link')
async def _invite(ctx):
    embedVar=discord.Embed(color=0xfcff66)
    embedVar.add_field(name='Invite link', value='Click [me](https://discord.com/api/oauth2/authorize?client_id=853230803339968552&permissions=2147839040&scope=bot%20applications.commands) to invite')
    await ctx.send(embed=embedVar)

@slash.slash(name='report',description='Report asuggestion')
async def _report(ctx,messagelink):
    re = await bot.fetch_channel(883956344472895529)
    await re.send(content=messagelink)
    await ctx.send(content='Sent')

@bot.command(name='report')
async def report(ctx,messagelink):
    re = await bot.fetch_channel(883956344472895529)
    await re.send(content=messagelink)
    await ctx.send(content='Sent')

keep_alive.keep_alive()
my_secret = os.environ['token']
token = 0
bot.run(my_secret)  # Starts the bot