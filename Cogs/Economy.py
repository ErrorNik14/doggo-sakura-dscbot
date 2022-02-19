from nextcord.ext import commands
import json
import nextcord
from Cogs import Funcs as fc
import random
import asyncio

class Economy(commands.Cog):
  def __init__(self, bot):
    self.bot = bot
  
  #buttons
  class Work1(nextcord.ui.View):
    def __init__(self):
      super().__init__(timeout=15)
      self.list = []
    
    #["bricks", "buildings", "cement", 'tools']

    @nextcord.ui.button(label="Bricks", style=nextcord.ButtonStyle.blurple)
    async def one(self, button:nextcord.ui.Button, interaction: nextcord.Interaction):
      self.list.append("bricks")
      self.stop()

    @nextcord.ui.button(label="Buildings", style=nextcord.ButtonStyle.blurple)
    async def two(self, button:nextcord.ui.Button, interaction: nextcord.Interaction):
      self.list.append("buildings")
      self.stop()

    @nextcord.ui.button(label="Cement", style=nextcord.ButtonStyle.blurple)
    async def three(self, button:nextcord.ui.Button, interaction: nextcord.Interaction):
      self.list.append("cement")
      self.stop()

    @nextcord.ui.button(label="Tools", style=nextcord.ButtonStyle.blurple)
    async def four(self, button:nextcord.ui.Button, interaction: nextcord.Interaction):
      self.list.append("tools")
      self.stop()
  





  #commands
  async def cog_check(self, ctx):
    f = open("economy.json", 'r')
    read = json.load(f)
    f.close()
    if str(ctx.author.id) not in read:
      read[str(ctx.author.id)] = {"username": str(ctx.author), "money": 0, "items": [], "job": None}
      r = open("economy.json", 'w')
      json.dump(read, r, indent=1)
    return True

  @commands.command(aliases=["bal"])
  @commands.cooldown(1, 3, commands.BucketType.user)
  async def balance(self, ctx, member:nextcord.Member=None):
    if member is None:
      member = ctx.author
    
    fc.memberReg(member)
    read = fc.economyInfo()
    amount = read[str(member.id)]["money"]
    money = "{:,}".format(amount)
    embed = nextcord.Embed(title=f"{member.name}'s Balance", description=f"`{money}` <:floofbred:928880102014590996>", color=ctx.author.color)
    await ctx.reply(embed=embed)

  @commands.command(aliases=["freemoney"])
  @commands.cooldown(1, 10, commands.BucketType.user)
  async def beg(self, ctx):
    read = fc.economyInfo()
    beggedAmount = random.randint(16,150)
    if beggedAmount <75:
      embed = nextcord.Embed(title=f"You got {beggedAmount} <:floofbred:928880102014590996>", description="Get better at begging lol")
    else:
      embed = nextcord.Embed(title=f"You got {beggedAmount} <:floofbred:928880102014590996>", description="Still sucks at begging <:lel:926461435444338758>")
    read[str(ctx.author.id)]["money"]+=beggedAmount
    fc.writeEconomy(read)
    await ctx.reply(embed=embed)
  
  @commands.command()
  @commands.cooldown(1, 10, commands.BucketType.user)
  async def give(self, ctx, member:nextcord.Member=None, amount=1):
    if member is None:
      await ctx.reply("nob give money to who <:lel:926461435444338758>")
    else:
      fc.memberReg(member)
      id1 = str(ctx.author.id)
      id2 = str(member.id)
      read = fc.economyInfo()
      if amount>read[id1]['money']:
        await ctx.reply("nob you don't have enough floofbred >:(")
      else:
        read[id1]['money']-=amount
        read[id2]['money']+=amount
        fc.writeEconomy(read)
        embed = nextcord.Embed(title=f"Successfully gave `{member.name}` `{fc.nF(amount)}` <:floofbred:928880102014590996>", color=ctx.author.color)
        await ctx.reply(embed=embed)


  @commands.command(aliases=["peta"])
  @commands.cooldown(1, 11, commands.BucketType.user)
  async def hunt(self, ctx):
    read = fc.economyInfo()
    n = random.randint(1,100)
    if n<36:
      embed = nextcord.Embed(title="You got a pretty Smol Beetle!", color=ctx.author.color)
      read[str(ctx.author.id)]["items"].append("tbug")
      fc.writeEconomy(read)
      await ctx.send(embed=embed)
    elif n<56:
      embed = nextcord.Embed(title="You got a Chonky Beetle!", color=ctx.author.color)
      read[str(ctx.author.id)]["items"].append("lbug")
      fc.writeEconomy(read)
      await ctx.send(embed=embed)
    elif n<61:
      embed = nextcord.Embed(title="You got Bear Hide!", color=ctx.author.color)
      read[str(ctx.author.id)]["items"].append("bhide")
      fc.writeEconomy(read)
      await ctx.send(embed=embed)
    elif n<76:
      embed = nextcord.Embed(title="You got Deer Venison!", color=ctx.author.color)
      read[str(ctx.author.id)]["items"].append("dvenison")
      fc.writeEconomy(read)
      await ctx.send(embed=embed)
    elif n<91:
      embed = nextcord.Embed(title="You got a Rabbit Foot!", color=ctx.author.color)
      read[str(ctx.author.id)]["items"].append("rfoot")
      fc.writeEconomy(read)
      await ctx.send(embed=embed)
    elif n<100:
      embed = nextcord.Embed(title="You got a Anaconda!", color=ctx.author.color)
      read[str(ctx.author.id)]["items"].append("conda")
      fc.writeEconomy(read)
      await ctx.send(embed=embed)
    else:
      n2 = random.randint(1,100)
      if n2<11:
        embed = nextcord.Embed(title="You got a Unicorn Horn!", color=ctx.author.color)
        read[str(ctx.author.id)]["items"].append("uhorn")
        fc.writeEconomy(read)
        await ctx.send(embed=embed)
      elif n2<21:
        embed = nextcord.Embed(title="You got a Dragon Scale!", color=ctx.author.color)
        read[str(ctx.author.id)]["items"].append("dscale")
        fc.writeEconomy(read)
        await ctx.send(embed=embed)
      elif n2<24:
        embed = nextcord.Embed(title="You got... A DOGE, HOLY FLIP O.O", color=ctx.author.color)
        read[str(ctx.author.id)]["items"].append("doge")
        fc.writeEconomy(read)
        await ctx.send(embed=embed)
      else:
        embed = nextcord.Embed(title="You got some Stingray Poison!", color=ctx.author.color)
        read[str(ctx.author.id)]["items"].append("spoison")
        fc.writeEconomy(read)
        await ctx.send(embed=embed)
  
  @commands.command(aliases=["inv", "storage"])
  @commands.cooldown(1, 7, commands.BucketType.user)
  async def inventory(self, ctx, member:nextcord.Member=None):
    if member is None:
      member = ctx.author
    fc.memberReg(member)
    read1 = fc.economyInfo()
    read2 = fc.itemInfo()

    if read1[str(member.id)]["items"] == []:
      await ctx.reply("nob you have no items :laughing:")
    else:
      embed = nextcord.Embed(title=f"{member.name}'s Inventory", color=ctx.author.color)
      for i in read2:
        if i["short"] in read1[str(member.id)]["items"]:
          amount = read1[str(member.id)]["items"].count(i["short"])
          embed.add_field(name=f"{i['dname']} ({amount}x) {i['emoji']}", value=f"_(Short: {i['short']})_\n{i['desc']}", inline=True)
      await ctx.reply(embed=embed)


  @commands.command(aliases=["sale"])
  @commands.cooldown(1, 8, commands.BucketType.user)
  async def sell(self, ctx, item:str, num:int=1):
    read1 = fc.economyInfo()
    read2 = fc.itemInfo()
    item_exist = False
    for e in read2:
      if e["short"].lower() == item.lower() or e["name"].lower() == item.lower():
        item_exist = True
        if e["sellable"] is True:
          amount = read1[str(ctx.author.id)]["items"].count(e["short"])
          if num>amount:
            embed = nextcord.Embed(title="<a:cross:925969103087341578> You don't have enough!", color=ctx.author.color)
            await ctx.reply(embed=embed)
          else:
            gain = e["sell_cost"] * num
            read1[str(ctx.author.id)]["money"]+=gain
            while read1[str(ctx.author.id)]["items"].count(e['short'])>0:
              read1[str(ctx.author.id)]["items"].remove(e['short'])
            fc.writeEconomy(read1)
            embed = nextcord.Embed(title=f"<a:tick:925969125367480340> Successfully sold `{fc.nF(num)} {e['dname']}`, your current balance is `{fc.nF(read1[str(ctx.author.id)]['money'])}` <:floofbred:928880102014590996>", color=ctx.author.color)
            await ctx.reply(embed=embed)
        else:
          embed = nextcord.Embed(title="<a:cross:925969103087341578> You can't sell that item!", color=ctx.author.color)
          await ctx.reply(embed=embed)
    
    if not item_exist:
      embed = nextcord.Embed(title="<a:cross:925969103087341578> That item does not exist!", color=ctx.author.color)
      await ctx.reply(embed=embed)



  @commands.command(aliases=['item', 'iteminfo'])
  @commands.cooldown(1, 5, commands.BucketType.user)
  async def shop(self, ctx, *arg):
    read = fc.itemInfo()
    item = ''
    item_exist = False
    if arg != ():
      for i in arg:
        item = item + i + ' '
      item = item[0:len(item)-1]
      for e in read:
        l = [e["short"].lower(), e["name"].lower(), e["dname"].lower()]
        if item.lower() in l:
          item_exist = True
          embed = nextcord.Embed(title=f"{e['dname']} {e['emoji']}", description=f"_(Short:{e['short']})_\n{e['desc']}", color=ctx.author.color)
          if not e['sellable']:
            embed.add_field(name="_Cannot be sold_", value='\u200b', inline=False)
          else:
            embed.add_field(name="Can be sold for", value=f"`{fc.nF(e['sell_cost'])}` <:floofbred:928880102014590996>")
          if e['buy_cost'] == None:
            embed.add_field(name="_Cannot be bought_", value='\u200b', inline=False)
          else:
            embed.add_field(name="Can be bought for", value=f"`{fc.nF(e['buy_cost'])}` <:floofbred:928880102014590996>")
          await ctx.reply(embed=embed)
      
      if not item_exist:
        embed = nextcord.Embed(title="<a:cross:925969103087341578> That item does not exist", color=ctx.author.color)
        await ctx.reply(embed=embed)

    else:
      await ctx.reply("nob there's no actual shop yet")



  @commands.command(aliases=['job'])
  #@commands.cooldown(1, 3, commands.BucketType.user)
  async def work(self, ctx):
    read1 = fc.economyInfo()
    read2 = fc.jobInfo()
    id = str(ctx.author.id)
    if read1[id]["job"] is None:
      await ctx.reply("Nob you don't have a job <:lel:926461435444338758>")
    else:
      for e in read2:
        job = e["name"]
        pay = e["pay"]
        if e["name"] == job:
          pay = e["pay"]
          def check(m):
              return m.content and m.channel == ctx.channel and m.author == ctx.author
          if job == "builder":
            a = random.randint(1,3)
            if a == 1:
              l = ["bricks", "buildings", "cement", 'tools']
              random.shuffle(l)
              message = await ctx.send(f"Remember this in this order:\n`{l[0]}`\n`{l[1]}`\n`{l[2]}`\n`{l[3]}`")
              await asyncio.sleep(5)
              await message.edit(content="Type the words")
              try:
                msg = await self.bot.wait_for('message', check=check, timeout=8)
                cont = msg.content.lower().replace(" ","").split("\n")
                
                if l == cont:
                  read1[id]["money"] += pay
                  fc.writeEconomy(read1)
                  embed = nextcord.Embed(title=f"Poggers! You earned {pay} <:floofbred:928880102014590996>\nYour current balance is {fc.nF(read1[id]['money'])} <:floofbred:928880102014590996>", color=ctx.author.color)
                  await msg.reply(embed=embed)
                else:
                  embed = nextcord.Embed(title=f"Grrrr, you didn't do your work properly :rage:\nYou got 0 <:floofbred:928880102014590996>", color=ctx.author.color)
                  await msg.reply(embed=embed)


              except asyncio.TimeoutError:
                embed = nextcord.Embed(title=f"You took too much time to work :rage:\nYou got 0 <:floofbred:928880102014590996>", color=ctx.author.color)
                await ctx.reply(embed=embed)

            elif a == 2:
              pass
            elif a == 3:
              pass


def setup(bot):
  bot.add_cog(Economy(bot))