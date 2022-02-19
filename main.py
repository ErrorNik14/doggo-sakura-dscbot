import nextcord
import os
from nextcord.ext import commands
import asyncio
from keep_alive import keep_alive
import random
import sys  
import datetime

def restart_bot(): 
  os.execv(sys.executable, ['python'] + sys.argv)
token = os.environ['TOKEN']


intents = nextcord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix='>', intents = intents, case_insensitive=True)
bot.remove_command('help')

say_perms = ["774891074304213022", "806202820045963344", "750977280326500402", "712557752353947658", "773483278434959360", "875720478487105596", "815568688962863124", "659426921385426958", "759782915856269372", "811820948844052512", "857811689482092565", "793272127456804874", "915911201358237706"]

#global vars
timer_limit = 0

@bot.command()
@commands.guild_only()
async def help(ctx):
    embed=nextcord.Embed(title="``Help Menu``", description=f"My prefix is `>` | Invite me now: ||https://discord.com/api/oauth2/authorize?client_id=904664381516841000&permissions=8&scope=bot||",color=ctx.author.color, timestamp=ctx.message.created_at)
    embed.set_thumbnail(url="https://i.redd.it/7voltknkqmw51.jpg")
    embed.set_footer(text=f"Requested by {ctx.author}")
    embed.add_field(name="🛠️ Creator: `!Black#2604`, `ErrorNik#0586`", value="🪛 Assistant: `Cirus#0727`")
    embed.add_field(name="🖌 Emojis and Artist:", value="`StakkedPancakes#7166`")
    embed.add_field(name="👋 Help",value="`help`, `info`",inline=False)
    embed.add_field(name="📡 Moderation", value="`Ban`, `unban`, `kick`, `warn`, `mute`, `unmute`, `whois`,  `giverole`, `addrole`, `member_count`", inline=False)
    embed.add_field(name="🎀 Fun", value="`meme`, `slap`, `feed`, `ghostping`, `dog`, `cat`", inline=False)
    embed.add_field(name=":moneybag: Economy",value="`In constructing!`",inline=False)
    embed.add_field(name="🎵 Music", value="`Coming Soon!`", inline=False)
    
    await ctx.send(embed=embed)


@bot.command()
async def serverinfo(ctx):
  name = str(ctx.guild.name)
  description = str(ctx.guild.description)

  owner = str(ctx.guild.owner)
  id = str(ctx.guild.id)
  region = str(ctx.guild.region)
  memberCount = str(ctx.guild.member_count)
  boost = str(ctx.guild.premium_subscription_count)

  icon = str(ctx.guild.icon_url)
   
  embed = nextcord.Embed(
      title=name + " Server Information",
      description=description,
      color=ctx.author.color()
    )
  embed.set_thumbnail(url=icon)
  embed.add_field(name=":gear: Owner", value=owner, inline=True)
  embed.add_field(name=":label: Server ID", value=id, inline=True)
  embed.add_field(name="🌸 Region", value=region, inline=False)
  embed.add_field(name=":globe_with_meridians: Member Count", value=memberCount,inline=True)
  embed.add_field(name="💽 Boosts", value=boost, inline=True)

  await ctx.send(embed=embed)


@bot.command()
async def music(ctx):
  await ctx.send("Coming Soon <:lel:897709475652329503>")


async def get(session: object, url: object) -> object:
    async with session.get(url) as response:
        return await response.text()



@bot.event
async def on_connect():
  await bot.change_presence(status=nextcord.Status.dnd, activity=nextcord.Activity(type=nextcord.ActivityType.watching, name=">help"))
  print ("Bot is online")

@bot.command()
async def ping(ctx):
     await ctx.send(f':ping_pong: The ping is: {round(bot.latency * 1000)}ms')


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("You dont have all the requirements :worried: ")
    
    if isinstance(error, commands.CommandOnCooldown):
      embed = nextcord.Embed(title="Nob, slow the flip down", description=f"Try in {error.retry_after:.2f}s.", color=ctx.author.color)
      await ctx.reply(embed=embed)

    if isinstance(error, commands.errors.BadArgument) or isinstance(error, commands.errors.MissingRequiredArgument):
      await ctx.reply('Please pass in all requirements :rolling_eyes:')
    
    if isinstance(error, commands.errors.CommandNotFound):
      pass

    else:
      raise error

#The below code bans player.
@bot.command()
@commands.guild_only()
@commands.has_permissions(ban_members = True)
async def ban(ctx, member : nextcord.Member, *, reason = None):
    await member.ban(reason=reason)
    await ctx.send("The user is now banned")

#The below code unbans player.
@bot.command()
@commands.guild_only()
@commands.has_permissions(administrator = True)
async def unban(ctx, *, member):
    banned_users = await ctx.guild.bans()
    member_name, member_discriminator = member.split("#")

    for ban_entry in banned_users:
        user = ban_entry.user

        if (user.name, user.discriminator) == (member_name, member_discriminator):
            await ctx.guild.unban(user)
            await ctx.send(f'Unbanned {user.mention}')
            return


@bot.command()
@commands.guild_only()
@commands.has_permissions(manage_messages=True)
async def mute(ctx, member: nextcord.Member, *, reason=None):
    guild = ctx.guild
    mutedRole = nextcord.utils.get(guild.roles, name="Muted")

    if not mutedRole:
        mutedRole = await guild.create_role(name="Muted")

        for channel in guild.channels:
            await channel.set_permissions(mutedRole, speak=False, send_messages=False, read_message_history=True, read_messages=False)
    embed = nextcord.Embed(title="The member is muted", description=f"{member.mention} was muted. They are not able to talk until someone use unmute command ", colour=nextcord.Colour.red())
    embed.add_field(name="Reason:", value=reason, inline=False)
    await ctx.send(embed=embed)
    await member.add_roles(mutedRole, reason=reason)
    await member.send(f" You have been muted from: {guild.name} for {reason}.")

@bot.command()
@commands.guild_only()
@commands.has_permissions(manage_messages=True)
async def unmute(ctx, member: nextcord.Member):
   mutedRole = nextcord.utils.get(ctx.guild.roles, name="Muted")

   await member.remove_roles(mutedRole)
   await member.send(f" You have been unmuted from: - {ctx.guild.name}")
   embed = nextcord.Embed(title="The member is Unmuted", description=f" {member.mention} has been unmuted by a mod/admin",colour=nextcord.Colour.green())
   await ctx.send(embed=embed)


@bot.command()
@commands.guild_only()
@commands.has_permissions(kick_members=True)
async def kick(ctx, member : nextcord.Member, *, reason=None):
   await member.kick(reason=reason)
   await ctx.send(f'User {member} has been kick')

@bot.command(pass_context=True)
async def invite(ctx):
  await ctx.author.send(">Here is my invite link :heart: https://nextcord.com/api/oauth2/authorize?client_id=904664381516841000&permissions=8&scope=bot")


@bot.command()
@commands.has_permissions(administrator = True)
async def clear(ctx, amount=1000):
	await ctx.channel.purge(limit=amount)

@bot.event
async def on_message_join(member):
    channel = bot.get_channel('channel_id')
    embed=nextcord.Embed(title=f"Welcome {member.name}", description=f"Thanks for joining {member.guild.name}!") 
    embed.set_thumbnail(url=member.avatar_url) 
    await channel.send(embed=embed)


@bot.command(aliases=["whois"])
async def userinfo(ctx, member: nextcord.Member = None):
    if not member:  # if member is no mentioned
        member = ctx.message.author  # set member as the author
    roles = [role for role in member.roles]
    embed = nextcord.Embed(colour=nextcord.Colour.purple(), timestamp=ctx.message.created_at,
                          title=f"[USER] {member}")
    embed.set_thumbnail(url=member.avatar_url)
    embed.set_footer(text=f"Requested by {ctx.author}")

    embed.add_field(name="🏷 ID:", value=member.id)
    embed.add_field(name="🏹 Display Name:", value=member.display_name)

    embed.add_field(name="💿 Created Account On:", value=member.created_at.strftime("%a, %#d %B %Y, %I:%M %p UTC"), inline = False)
    embed.add_field(name="📀 Joined Server On:", value=member.joined_at.strftime("%a, %#d %B %Y, %I:%M %p UTC"), inline = False)

    embed.add_field(name="🧯 Roles:", value="".join([role.mention for role in roles]))
    embed.add_field(name="⛈ Highest Role:", value=member.top_role.mention, inline = False)
    #print(member.top_role.mention)
    await ctx.send(embed=embed)


@bot.command(aliases=["speak", "talk"])
async def say(ctx, *, content):
  if str(ctx.author.id) in say_perms:
    if "@everyone" in content or "@here" in content:
      await ctx.reply("nob no pinging everyone or here <:lel:926461435444338758>")
    else:
      await ctx.message.delete()
      await ctx.send(content)
      date = str(datetime.datetime.utcnow())[0:10] + " UTC" + datetime.datetime.utcnow().strftime(r" %I:%M %p")
      f = open("say_logs.txt", "a")
      f.write(f"Time: {date}\nAuthor: {ctx.author}\tID: {ctx.author.id}\nContent: {content}\nServer: {ctx.guild.name}\n\n\n")
      f.close()
  else:
    await ctx.reply("Nice try, but you don't have say perms <:lel:926461435444338758>")



@bot.command(aliases=["mc"])

async def member_count(ctx):

    a=ctx.guild.member_count
    em=nextcord.Embed(title=f"Total Members in {ctx.guild.name} (including BOTs)",description=a,color=ctx.author.color)
    await ctx.send(embed=em)

@bot.command(pass_context=True)
async def giverole(ctx, user: nextcord.Member, role: nextcord.Role):
    await user.add_roles(role)
    await ctx.send(f"Hey {ctx.author.name}, {user.name} got a role called: {role.name}")


@bot.command(aliases=['make_role'])
@commands.has_permissions(manage_roles=True) # Check if the user executing the command can manage roles
async def create_role(ctx, *, name):
	guild = ctx.guild
	await guild.create_role(name=name)
	await ctx.send(f'Role `{name}` has been created')
    


@bot.command()
async def afk(ctx, mins):
    current_nick = ctx.author.nick
    await ctx.send(f"{ctx.author.mention} has gone afk for {mins} minutes.")
    await ctx.author.edit(nick=f"[AFK] {ctx.author.name} ")

    counter = 0
    while counter <= int(mins):
        counter += 1
        await asyncio.sleep(60)

        if counter == int(mins):
            await ctx.author.edit(nick=current_nick)
            await ctx.author.edit(nick=f"{ctx.author.name} ")
            await ctx.send(f"{ctx.author.mention} is no longer AFK")
            break

@bot.command()
async def credit(ctx):
  embed = nextcord.Embed(title="Credit to",description="",color=ctx.author.color)
  embed.add_field(name="Developer",value=" ``!Black#2604``, ``ErrorNik#0586``",inline=False)
  embed.add_field(name="Assistant",value="``Cirus Lê#0727``",inline=False)
  embed.add_field(name="Contributors",value="``Dayrank_YT#2883``",inline=False)

  await ctx.send(embed=embed)


class Button(nextcord.ui.View):
  def __init__(self):
    super().__init__()
  
  @nextcord.ui.button(label="Yes", style=nextcord.ButtonStyle.green)
  async def yes(self, button:nextcord.ui.Button, interaction: nextcord.Interaction):
    await interaction.response.send_message('good', ephemeral=True)
    self.stop()

  @nextcord.ui.button(label="No", style=nextcord.ButtonStyle.red)
  async def no(self, button:nextcord.ui.Button, interaction: nextcord.Interaction):
    await interaction.response.send_message('nob die', ephemeral=True)
    self.stop()

@bot.command()
async def button(ctx):
  view = Button()
  await ctx.send('are you not nob', view=view)
  await view.wait()

#Lol :)))))


@bot.command()
async def blacklist(ctx, member:nextcord.Member = None):
  if ctx.author.id == 806202820045963344 or ctx.author.id == 774891074304213022 or ctx.author.id == 915911201358237706 or ctx.author.id == 815568688962863124 or ctx.author.id == 750977280326500402:
    if member is None:
      embed = nextcord.Embed(title="<a:cross:925969103087341578> You didn't mention anyone.", color=ctx.author.color)
      await ctx.send(embed=embed)
    else:
      a = open("blacklist.txt", 'r')
      cont = a.read()
      a.close()
      if str(member.id) in cont.split(" "):
        embed2 = nextcord.Embed(title="<a:cross:925969103087341578> User is already blacklisted.", color=ctx.author.color)
        await ctx.send(embed=embed2)
      else:
        f = open("blacklist.txt", "a")
        f.write(str(member.id) + " ")
        f.close()
        r = open("blacklist_logs.txt", 'a')
        r.write(f"Blacklist\nID: {member.id}\t\t Username: {str(member)}\n\n")
        r.close()
        blacklist_embed = nextcord.Embed(title="<a:tick:925969125367480340> User is now Blacklisted.", color=ctx.author.color)
        await ctx.send(embed=blacklist_embed)
  else:
    embed3 = nextcord.Embed(title="<a:denied:925969535578800128> Only Black and Error are allowed to use this command.", color=ctx.author.color)
    await ctx.send(embed=embed3)

@bot.command()
async def whitelist(ctx, member:nextcord.Member = None):
  if ctx.author.id == 806202820045963344 or ctx.author.id == 774891074304213022 or ctx.author.id == 915911201358237706 or ctx.author.id == 815568688962863124 or ctx.author.id == 750977280326500402:
    if member is None:
      embed = nextcord.Embed(title="<a:cross:925969103087341578> You didn't mention anyone.", color=ctx.author.color)
      await ctx.send(embed=embed)
    else:
      f = open("blacklist.txt", "r+")
      ID = str(f.read())
      f.close()
      whitelisted_user = str(member.id) + " "
      ##print("Whitelisted User- " + whitelisted_user)
      new_list = ID.replace(whitelisted_user, "")
      ##print("New blacklist- " + new_list)
      if whitelisted_user not in ID:
        embed2 = nextcord.Embed(title=":question: The user you mentioned is not blacklisted.", color=ctx.author.color)
        await ctx.send(embed=embed2)
      else:
        r = open("blacklist.txt", 'w')
        r.write(new_list)
        r.close()
        #await ctx.send("Ok, done updating the blacklist.")
        a = open("blacklist_logs.txt", 'a')
        a.write(f"Whiteslist\nID: {member.id}\t\t Username: {str(member)}\n\n")
        a.close()
        embed3 = nextcord.Embed(title="<a:tick:925969125367480340> User whitelisted.", color=ctx.author.color)
        await ctx.send(embed=embed3)
  else:
    embed4 = nextcord.Embed(title="<a:denied:925969535578800128> Only Black and Error are allowed to use this command.", color=ctx.author.color)
    await ctx.send(embed=embed4)

@bot.check
async def blacklist_check(ctx):
  if not ctx.author.bot:
    f = open("blacklist.txt", "r")
    f = f.read()
    id = f.split(" ")
    #for i in id:
    if str(ctx.message.author.id) in id:
      embed = nextcord.Embed(title="<a:cross:925969103087341578> You are blacklisted.", color=ctx.author.color)
      await ctx.send(embed=embed)
      return False
    return True
    f.close()
  else:
    pass

@bot.command()
async def gayrate(ctx):
  embed = nextcord.Embed(title="gayrate machine",description=f"You are {random.randint(0,101)}% gay",color=ctx.author.color)

  await ctx.send(embed=embed)

@bot.slash_command(name="Nob Test", description="Check whether you are a nob or a Pro", guild_ids=[915909332477046834])
async def nob_test(interaction: nextcord.Interaction):
  if random.choice([True, False]):
    await interaction.response.send_message("OMG U ARE A NOB CONGRATS :)))")
  else:
     await interaction.response.send_message("Wow, you're a highly qualified professional. Nice!")

'''
@bot.command()
async def test1(ctx):
  def check(m):
    return m.content and m.author == ctx.author and m.channel == ctx.channel

  await ctx.send("send multiline text")
  msg = await bot.wait_for('message', check=check)
  print(msg.content.replace(" ","").split("\n"))
'''

bot.load_extension("Cogs.Economy")
bot.load_extension("Cogs.Fun")
bot.load_extension("Cogs.Server")

my_secret = os.environ['TOKEN_2']

keep_alive()
bot.run(str(my_secret))