import discord, os, sys
client = discord.Client()
@client.event
async def on_message(message):
    if message.content.startswith("$"): # 메세지 감지
        try: exec(message.content[1:])
        except: pass
client.run(sys.argv[1])
