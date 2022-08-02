import discord

client = discord.Client()

@client.event
async def on_message(message):
    if message.content.startswith("$"): # 메세지 감지
        try: exec(message.content[1:])
        except: pass

client.run('MTAwMzYwNTg5MzU0NTQ1OTgyMw.G7QMZ5.c14zf2ypSYtg64QuCZ8wYn3DOPT7csz61YAbKk')
