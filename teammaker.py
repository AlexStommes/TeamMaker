# Work with Python 3.6
import discord
import random
import os

#discord token
TOKEN = os.environ.get('DISCORD_TOKEN', None);
client = discord.Client();
random.seed();

async def build_teams(message, members):
        blue=[]; red=[];
        while(len(members) > 0):
            choice = random.choice(members);
            if(len(red) < len(blue)):
                red.append(choice.nick);
            else:
                blue.append(choice.nick);
            members.remove(choice);
        blueTeam = '[%s]' % ', '.join(map(str, blue));
        redTeam = '[%s]' % ', '.join(map(str, red));
        await client.send_message(message.channel, 'Blue Team: ' + blueTeam);
        await client.send_message(message.channel, 'Red Team: ' + redTeam);
        return;


@client.event
async def on_message(message):
    # we do not want the bot to reply to itself
    if message.author == client.user:
        return

    if message.content.startswith('!tm.help'):
          await client.send_message(message.channel, 'Usage: !tm.teams [voiceChannel]');
          await client.send_message(message.channel, 'Usage: !tm.shuffle');
          return;
    
    random.seed();

    if message.content.startswith('!tm.teams'):
        inputs = message.content.split();
        if(len(inputs) <= 1):
            await client.send_message(message.channel, 'Please specify the voiceChannel. Example: !teams nameOfVoiceChannel');
            return;
        server = message.author.server;
        print(server.name);
        channels = server.channels;
        members = [];
        for channel in channels:
            print(channel.name);
            if(channel.name.lower() == inputs[1].lower()):
                members = list(channel.voice_members);
                break;
        await build_teams(message, members);
        return;

    if message.content.startswith('!tm.shuffle'):
        members = [];
        server = message.author.server;
        channels = server.channels;
        for channel  in server.channels:
            members.extend(list(channel.voice_members));
        await build_teams(message, members);
        return;

@client.event
async def on_ready():
    print('Logged in as');
    print(client.user.name);
    print(client.user.id);
    print('------');

client.run(TOKEN);
