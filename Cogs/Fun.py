from nextcord.ext import commands
import nextcord
from Cogs import Funcs as fc
import aiohttp
import requests
import random
import asyncio

class Fun(commands.Cog):
  def __init__(self, bot):
    self.bot = bot
  
  @commands.command()
  async def dog(self, ctx):
   async with aiohttp.ClientSession() as session:
      request = await session.get('https://some-random-api.ml/img/dog')
      dogjson = await request.json()
      # This time we'll get the fact request as well!
      request2 = await session.get('https://some-random-api.ml/facts/dog')
      factjson = await request2.json()

      embed = nextcord.Embed(title="Doggo!", color=ctx.author.color)
      link = dogjson['link']
      embed.set_image(url=link)
      embed.set_footer(text=factjson['fact'])
      await ctx.send(embed=embed)

  @commands.command()
  async def cat(self, ctx):
      response = requests.get('https://aws.random.cat/meow')
      data = response.json()
      embed = nextcord.Embed(
          title = 'Kitty Cat 🐈',
          description = 'Cats :star_struck:',
          colour = nextcord.Colour.purple()
          )
      embed.set_image(url=data['file'])            
      embed.set_footer(text="")
      await ctx.send(embed=embed)
  
  @commands.command(name='8ball',
            description="Answers a yes/no question.",
            brief="Answers from the beyond.",
            aliases=['eight_ball', 'eightball', '8-ball'],
            pass_context=True)
  async def eight_ball(self, ctx, *argv): 
    if not argv[0] is None:
      possible_responses = [
          '🎱 Totally no',
          '🎱 Not looking likely',
          '🎱 Too hard to tell',
          '🎱 Quite possible',
          '🎱 Definitely',
      ]  
      await ctx.channel.send(random.choice(possible_responses) + ', ' + ctx.author.mention)
    else:
      await ctx.send(ctx.author.mention + ' Nob you didn\'t say anything, so I won\'t give you any response >:D')

  @commands.command()
  async def meme(self, ctx):
    r = requests.get(f"https://ctk-api.herokuapp.com/meme/{random.randint(0,300)}")
    ulr = r.url
    embed = nextcord.Embed(title=f"Here is your meme, Enjoy <3")
    embed.set_image(url=ulr)
    embed.set_footer(text=f"By {self.bot.user}")
    await ctx.send(embed=embed)

  @commands.command()
  async def pun(self, ctx):
    r = requests.get("https://v2.jokeapi.dev/joke/Pun?blacklistFlags=nsfw,religious,political,racist,sexist,explicit")
    json_data = r.json()
    qs = str(json_data['setup'])
    ans = str(json_data['delivery']) + " <a:omgsoduni:926060647056306246>"
    embed = nextcord.Embed(title=qs, description=ans, color=ctx.author.color)
    await ctx.send(embed=embed)

  @commands.command()
  async def timer(self, ctx, type, time):
    s = ['seconds', 'second', 'sec', 's']
    m = ['minutes', 'minute', 'min', 'm']
    h = ['hours', 'hour', 'h']
    type = str(type).lower() 
    global timer_limit
    if type in s:
      time = int(time)
    elif type in m:
      time = int(time) * 60
    elif type in h:
      time = int(time) * 3600
    #capping the maximum time an alarm can be kept
    if time>1800:
      embed = nextcord.Embed(title="<a:aclock:924936806644989972> Timer",description="Time exceeds maximum limit. (30 minutes)",color=ctx.author.color)
      await ctx.send(embed=embed)
    elif time<5:
      embed = nextcord.Embed(title="<a:aclock:924936806644989972> Timer",description="Time set is less than the minimum required.",color=ctx.author.color)
      await ctx.send(embed=embed)
    else:
      if timer_limit == 1:
        await ctx.send("<a:aclock:924936806644989972> Maximum number of timers have been reached.")
      else:
        embed = nextcord.Embed(title="<a:aclock:924936806644989972> Timer",description="Timer set!",color=ctx.author.color)
        await ctx.send(embed=embed) 
        timer_limit+=1
        i = time
        while i>0:
          await asyncio.sleep(1)
          i-=1
        await ctx.author.send("<a:aclock:924936806644989972> Timer done.")
        timer_limit-=1

  @commands.command()
  async def giornotheme(self, ctx):
    embed = nextcord.Embed(title="You have summoned Giorno Giovanna", description="Kore ga.. **Requiem**.. da",color=ctx.author.color)
    embed.set_image(url="https://c.tenor.com/4DnpUyjoGn8AAAAd/ger-gold-experience-requiem.gif")
    await ctx.send(embed=embed)

  @commands.command()
  @commands.cooldown(1, 2, commands.BucketType.user)
  async def slap(self, ctx, member:nextcord.User=None):
    if (member == ctx.message.author or member == None):
        await ctx.send(f"{ctx.message.author.mention} slaps themselves!") 
    else:
        await ctx.send(f"{ctx.message.author.mention} slaps {member.mention}!")  

  @commands.command()
  async def simprate(self, ctx, member:nextcord.User=None):
    if member is None:
      member = ctx.message.author
    chance = random.randint(1, 9)
    half_emoji_chance = random.randint(0,1)
    content = "<:simp:925764745536106539>" * chance
    if half_emoji_chance == 1:
      content += "<:simpbutnotsimp:925958799574061117>"
      remain = 10-(chance+1)
      content += "<:notsimp:925956316164399125>" * remain
    else:
      remain = 10-chance
      content += "<:notsimp:925956316164399125>" * remain 
    embed = nextcord.Embed(title="Omg simp r8??", description=f"{member.mention} is {content}",color=ctx.author.color)
    await ctx.send(embed=embed)

  @commands.command(aliases=["dogfia", "doggofia"])
  async def doggus(self, ctx):
    class sixpillarButtons(nextcord.ui.View):
      def __init__(self):
        super().__init__(timeout=15)
        self.players = []
      
      @nextcord.ui.button(label="Join game", style=nextcord.ButtonStyle.blurple)
      async def join(self, button:nextcord.ui.Button, interaction=nextcord.Interaction):
        if interaction.user.id not in self.players:
          self.players.append(interaction.user.id)
          await interaction.response.send_message("Joined the game :thumbsup:", ephemeral=True)
        else:
          await interaction.response.send_message("You've already joined the game!", ephemeral=True)
      
      async def on_timeout(self):
        await self.message.edit("Time out! No more players can join, game will begin soon.", view=None)

    #actual command lines
    button = sixpillarButtons()
    button.message = await ctx.send("Initiating game, press the button to join.", view=button)
    await button.wait()
    if len(button.players)<6:
      imposter = random.choice(button.players)
    else:
      imposter = random.sample(button.players, 2)


def setup(bot):
    bot.add_cog(Fun(bot))