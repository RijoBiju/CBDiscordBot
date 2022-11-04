import random
import youtube_dl
import discord
from discord.ext import commands, tasks
from itertools import cycle

client = commands.Bot(command_prefix = ';')
game = cycle(['Bakemonogatari'])

@client.event
async def on_ready():
    status.start()
    print("I'm here!!")

@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Statement incorrect")

@tasks.loop(seconds = 10)
async def status():
    await client.change_presence(activity = discord.Game(next(game)))

@client.command()
async def tasuketae(ctx):
    embed = discord.Embed(title = 'MyAnimeList BOT', color = discord.Colour.green())
    embed.add_field(name = 'Commands', value = ''';ping
                                                    ;convo
                                                    ;clear
                                                    ;kick
                                                    ;ban
                                                    ;unban''')
    embed.add_field(name = 'Function', value = '''Displays ping of bot
                                                    Play 8ball
                                                    Clear a set of messages in a channel
                                                    Kick a certain member from server
                                                    Ban a certain member from server
                                                    Unban a certain member from server''')
    await ctx.send(embed = embed)

@client.command()
async def ping(ctx):
    await ctx.send(f'{round(client.latency * 1000)}ms')

@client.command(aliases = ['convo'])
async def _8ball(ctx, *, question):
    response = ['As I see it, yes',
                'Ask again later',
                'Better not tell you now',
                'Cannot predict now',
                'Concentrate and ask again',
                'Don’t count on it',
                'It is certain',
                'It is decidedly so',
                'Most likely',
                'My reply is no',
                'My sources say no',
                'Outlook not so good',
                'Outlook good',
                'Reply hazy, try again',
                'Signs point to yes',
                'Very doubtful',
                'Without a doubt',
                'Yes',
                'Yes – definitely',
                'You may rely on it']
    await ctx.send(f'Question : {question}\nAnswer : {random.choice(response)}')

@client.command()
@commands.has_permissions(manage_messages = True)
async def clear(ctx, amount : int): 
    await ctx.channel.purge(limit = amount)

@client.command()
@commands.check(commands.has_permissions)
async def kick(ctx, member : discord.Member, *, reason = "No reason"):
    await member.kick(reason = reason)

@client.command()
async def ban(ctx, member : discord.Member, *, reason = "No reason"):
    await member.ban(reason = reason)

@client.command()
async def unban(ctx, *, member):
    banned_users = await ctx.guild.bans()
    member_name, member_discriminator = member.split('#')
    
    for ban_entry in banned_users:
        user = ban_entry.user
        if (user.name, user.discriminator) == (member_name, member_discriminator):
            await ctx.guild.unban(user)

@client.command()
async def mute(ctx, member : discord.Member, *, reason = "You're annoying"):
    guild = ctx.guild

    for role in guild.roles:
        if role.name == "Muted":
            await member.add_roles(role)
            await ctx.send(f'{member_name} has been muted')
            return

            overwrite = discord.PermissionOverwrite(send_messages = False)
            newrole = await guild.create_role(name="Muted")

            for channel in guild.text_channels:
                await channel.set_permissions(newRole, overwrite = overwrite)

            await member.add_roles(newRole)
            await ctx.send(f'{member_name} has been muted')

@client.command()
async def unmute(ctx, member : discord.Member):
    guild = ctx.guild

    for role in guild.roles:
        if role.name == "Muted":
            await member.remove_roles(role)
            await ctx.send(f'{member_name} has been unmuted')
            return


@client.command()
async def load(ctx, extension):
    client.load_extension()

client.run('NzczMjA4MzI0NjIzMzAyNjk4.X6F4Xg.nU0L8ZwtViSxZghNsjpxjtFSF_M')   