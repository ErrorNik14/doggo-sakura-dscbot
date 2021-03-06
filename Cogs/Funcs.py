import json
import nextcord

def economyInfo():
  f = open("Databases/economy.json", 'r')
  read = json.load(f)
  f.close()
  return read

def writeEconomy(cont):
  f = open("Databases/economy.json", 'w')
  json.dump(cont, f)
  f.close()

def itemInfo():
  f = open("Databases/iteminfo.json", 'r')
  read = json.load(f)
  f.close()
  return read

def jobInfo():
  f = open("Databases/worklist.json", 'r')
  read = json.load(f)
  f.close()
  return read

def serverInfo():
  f = open("Databases/server_info.json", 'r')
  read = json.load(f)
  f.close()
  return read

def writeServerInfo(cont):
  f = open("Databases/server_info.json", 'w')
  json.dump(cont, f)
  f.close()

def memberReg(member):
  read = economyInfo()
  if str(member.id) not in read:
    read[str(member.id)] = {"username": str(member), "money": 0, "items": [], "job": None}
    writeEconomy(read)

def serverReg(guild):
  read = serverInfo()
  if str(guild.id) not in read:
    read[str(guild.id)] = {"sug_count": 0, "triggers": {}, "blacklisted_words": [], "sug_channel": None}
    writeServerInfo(read)

def nF(num):
  return "{:,}".format(num)