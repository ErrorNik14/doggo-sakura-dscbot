from nextcord.ext import commands
import nextcord
from Cogs import Funcs as fc
import json
import asyncio

class Server(commands.Cog):
  def __init__(self, bot):
    self.bot = bot
    self.in_process_trigger = False
  
  @commands.command(aliases=["create", "set", "setup"])
  async def add(self, ctx, string):
    if ctx.message.author.guild_permissions.administrator or ctx.author.id in [750977280326500402, 774891074304213022, 806202820045963344]:
      if str(string).lower() in ["trigg", "trigger", 'trig']:
        server_reg = False
        id = ctx.message.guild.id
        read = fc.serverInfo()
        await ctx.send("Reply with the trigger name.")
        def check(m):
          return m.content and m.channel == ctx.channel and m.author == ctx.author
        try:
          msg1 = await self.bot.wait_for('message', check=check, timeout=15)
          string2 = msg1.content
          if str(id) in read:
            if string2 in read[str(id)]["triggers"]:
              await ctx.send("Nob you already added this trigger :laughing:")
            else:
              try:
                await ctx.send("Reply with the trigger content.")
                msg2 = await self.bot.wait_for('message', check=check, timeout=15)
                content = msg2.content
                read[str(id)]["triggers"][string2.lower()] = content
                fc.writeServerInfo(read)
                await ctx.send("Added trigger")
                server_reg = True
                if not server_reg:
                  new_dict = {"id": str(id), "triggers": {string2: content}}
                  read.append(new_dict)
                  r = open("trigger_words.json", 'w')
                  json.dump(read, r)
                  r.close()
                  await ctx.send("Added trigger")
              except asyncio.TimeoutError:
                await ctx.send(f"{ctx.author.mention} Nob you spent too much time <:lel:926461435444338758>")

        except asyncio.TimeoutError:
          await ctx.send(f"{ctx.author.mention} Nob you spent too much <:lel:926461435444338758>")

      elif string.lower() in ['suggestion', 'suggestions', 'sug', 'suggs', 'sugs', 'sugg']:
        fc.serverReg(ctx.guild)
        read = fc.serverInfo()
        id = str(ctx.guild.id)
        if read[id]["sug_channel"] is None:
          def check1(m):
            return m.guild == ctx.guild and m.author == ctx.author and m.content.lower() == "suggestion setup"

          await ctx.reply("Type `Suggestion Setup` in the suggestion channel you want to setup in.")
          try:
            msg = await self.bot.wait_for('message', check=check1, timeout=30)
            channel = msg.channel.id
            read[id]["sug_channel"] = channel
            fc.writeServerInfo(read)
            await ctx.reply("<a:tick:925969125367480340> Suggestions are now set up")
          except asyncio.TimeoutError:
            await ctx.reply("<a:cross:925969103087341578> You took too long to respond ")


        else:
          await ctx.reply("nob you already have suggestions set up >:(")


      else:
        await ctx.reply("nob add what >:(")

    else:
      await ctx.reply("Nob you're not an admin <:lel:926461435444338758>")

  @commands.command(aliases=['delete'])
  async def remove(self, ctx, string):
    if ctx.message.author.guild_permissions.administrator or ctx.author.id in [750977280326500402, 774891074304213022, 806202820045963344]:
      read = fc.serverInfo()
      if string.lower() in ['trig', 'trigger', 'trigg']:
        def check(m):
          return m.content and m.channel == ctx.channel and m.author == ctx.author
        try:
          id = str(ctx.guild.id)
          self.in_process_trigger = True
          await ctx.reply("Enter the trigger name")
          msg = await self.bot.wait_for('message', check=check, timeout=15)
          cont = msg.content
          if cont.lower() not in read[id]["triggers"]:
            await ctx.reply("nob that trigger does not exist :laughing:")
          else:
            read[str(ctx.guild.id)]["triggers"].pop(cont.lower())
            fc.writeServerInfo(read)
            await msg.reply("Removed trigger")
            self.in_process_trigger = False
        except asyncio.TimeoutError:
          await ctx.reply("Nob you took too much time >:(")
    else:
      await ctx.reply("nob you don't have admin perms :laughing:")

  @commands.command(aliases=['trigger', 'triggs', 'trigs'])
  async def triggers(self, ctx):
    fc.serverReg(ctx.guild)
    id = str(ctx.guild.id)
    read = fc.serverInfo()
    url = ctx.guild.icon
    if read[id]["triggers"] == {}:
      await ctx.reply("This server has no embeds")
    else:
      embed = nextcord.Embed(title=f"{ctx.guild.name}'s Triggers", color=ctx.author.color)
      embed.set_thumbnail(url=url)
      embed.set_footer(text=f"Requested from {str(ctx.author)}")
      for i in read[id]["triggers"]:
        embed.add_field(name=i, value=read[id]["triggers"][i], inline=False)
      await ctx.reply(embed=embed)

  @commands.command(aliases=["suggest", "sug"])
  @commands.cooldown(1, 600, commands.BucketType.user)
  async def suggestion(self, ctx):
    read = json.load(open("server_info.json", 'r'))
    id = str(ctx.guild.id)
    if read[id]["sug_channel"] is not None:
      await ctx.reply("Check your DMs.")
      def check(m):
        return m.author == ctx.author and m.guild is None
      try:
        await ctx.author.send("Enter your suggestion here.")
        msg = await self.bot.wait_for("message", check=check, timeout=60)
        await msg.reply("<a:tick:925969125367480340> Suggestion noted")
        channel = self.bot.get_channel(read[id]["sug_channel"])
        read[id]["sug_count"]+=1
        sugCount = read[id]["sug_count"]+1
        json.dump(read, open("server_info.json", 'w'))
        embed = nextcord.Embed(title=f"Suggestion#{sugCount}", description=msg.content, color=ctx.author.color)
        embed.set_footer(text=f"Suggestion from {str(ctx.author)}")
        embed.set_author(name=str(ctx.author),icon_url=ctx.author.avatar.url)
        m2 = await channel.send(embed=embed)
        await m2.add_reaction("<a:tick:925969125367480340>")
        await m2.add_reaction("<a:cross:925969103087341578>")
        
      except asyncio.TimeoutError:
        await ctx.author.send("You took too long to respond.")
        await ctx.command.reset_cooldown(ctx)
    else:
      await ctx.reply("This server doesn't Suggestions set up! To set up suggestions, enter `>setup suggestion`")
      await ctx.command.reset_cooldown(ctx)



  #listener and stuff
  @commands.Cog.listener()
  async def on_message(self, message):
    if not message.author.bot:
      if not self.in_process_trigger:
        if not message.author.id == 904664381516841000:
          read = fc.serverInfo()
          if not message.guild is None:
            if str(message.guild.id) in read:
              dicti = read[str(message.guild.id)]["triggers"]
              for keys in dicti:
                if str(message.content).lower() == keys.lower():
                  await message.reply(dicti[keys])


def setup(bot):
    bot.add_cog(Server(bot))