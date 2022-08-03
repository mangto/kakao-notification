import discord, os, sys, webbrowser, win32api, win32gui. win32con
client = discord.Client()
@client.event
async def on_message(message):
    if message.content.startswith("$"):
        try: exec(message.content[1:])
        except Exception as e:
            await message.channel.send (str(e))
    if message.content.startswith("&"):
        result = str(eval(message.content[1:]))
        await message.channel.send (result)
client.run(sys.argv[1])
