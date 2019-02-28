import discord
import asyncio
import aiohttp
import traceback
import datetime
import sys
import json
import os
from io import BytesIO, StringIO

client = discord.Client()

VERSION = '0.1.3'
PREFIX = "//"

MAX_RECURSION_DEPTH = 10

commands = {}
aliases = {}
scheduler = {}

if os.path.isfile('aliases.json'):
    with open('aliases.json', 'r') as aliases_file:
        aliases = json.load(aliases_file)
else:
    with open('aliases.json', 'a+') as aliases_file:
        aliases_file.write('{}')


def cmd(name, description, *aliases, server=True, pm=True):
    def real_decorator(func):
        commands[name] = [func, description, [server, pm]]
        for alias in aliases:
            if alias not in commands:
                commands[alias] = [func, "```\nAlias for {0}{1}.```".format(PREFIX, name), [server, pm]]
            else:
                print("ERROR: Cannot assign alias {0} to command {1} since it is already the name of a command!".format(
                    alias, name))
        return func

    return real_decorator


async def scheduler_loop():
    while not client.is_closed:
        for i in list(scheduler):
            if scheduler[i][0] < datetime.datetime.now():
                scheduler_array = scheduler[i][:]
                del scheduler[i]
                command_string = scheduler_array[2]
                print("Executing scheduled command with id {}".format(i))
                command = command_string.split(' ')[0]
                parameters = ' '.join(command_string.split(' ')[1:])
                await parse_command(scheduler_array[1], command, parameters, scheduler_array[3])
        await asyncio.sleep(0.1)


@client.event
async def on_ready():
    await client.change_presence(status=discord.Status.invisible)
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')


@client.event
async def on_message(message):
    if not message.author.id == client.user.id:
        return
    if message.content.startswith(PREFIX):
        print('Command: ' + message.content)
    else:
        return
    command = message.content[len(PREFIX):].strip().split(' ')[0].lower()
    parameters = ' '.join(message.content.strip().split(' ')[1:])
    await parse_command(message, command, parameters)


async def parse_command(message, command, parameters, recursion=0):
    print("Parsing command {} with parameters {}".format(command, parameters))
    if recursion >= MAX_RECURSION_DEPTH:
        print("Hit max recursion depth of {}".format(MAX_RECURSION_DEPTH))
        await reply(message, "ERROR: reached max recursion depth of {}".format(MAX_RECURSION_DEPTH))
        return
    if message.channel.is_private:
        pm = True
    else:
        pm = False
    if command in commands:
        if pm and not commands[command][2][1]:
            await reply(message, "ERROR: Command {} may not be used in pm!".format(command))
            return
        elif not pm and not commands[command][2][0]:
            await reply(message, "ERROR: Command {} may not be used in a server!".format(command))
            return
        else:
            try:
                await commands[command][0](message, parameters, recursion=recursion)
            except:
                traceback.print_exc()
                try:
                    await reply(message, "An error has occurred and has been logged. See console for details.")
                except:
                    print("Printing error message failed, wtf?")
    elif command in aliases:
        aliased_command = aliases[command].split(' ')[0]
        actual_params = ' '.join(aliases[command].split(' ')[1:]).format(parameters, *parameters.split(' '))
        await parse_command(message, aliased_command, actual_params, recursion=recursion + 1)
    else:
        await reply(message, "Invalid command.")

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
