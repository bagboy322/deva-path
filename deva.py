import discord
import asyncio

client = discord.Client()

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

@client.event
async def on_message(message):
    # we do not want the bot to reply to itself
    if message.author == client.user:
        return
    if message.content.startswith('!help'):
        msg = 'Type !rollDeva or !rollDevaG'.format(message)
        await client. send_message(message.channel, msg)
    if message.content.startswith('!rollDevaG'):
         await client.wait_until_ready()
         i = 1
         while i < 6:
             msg = '$mg'.format(message)
             await client.send_message(message.channel, msg)
             i += 1
             await asyncio.sleep(3)
    elif message.content.startswith('!rollDeva'):
         await client.wait_until_ready()
         i = 1
         while i < 9:
            msg = '$m'.format(message)
            await client.send_message(message.channel, msg)
            i +=1
            await asyncio.sleep(3)

    if message.content.startswith('!THEBEAST'):
        msg = '$im Kagami Uchiha'.format(message)
        await client.send_message(message.channel, msg)



client.run('ozzytoth322@gmail.com', 'toth6614')
