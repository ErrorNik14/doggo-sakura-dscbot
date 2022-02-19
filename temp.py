import json

read = json.load(open("trigger_words.json", 'r'))
read2 = json.load(open("server_info.json", 'r'))

for i in read:
  read2[i] = {"sug_count": 0, "triggers": read[i], 'blacklisted_words': []}

json.dump(read2, open("server_info.json", 'w'))