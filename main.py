import discord
import datetime as date
import yaml

client = discord.Client()
with open('config.yaml') as config:
    oj = yaml.safe_load(config)
    global TOKEN
    TOKEN = oj['token'] 
if TOKEN is None:
    print('Not found valid token')
    exit()
NOW = date.datetime.now()
StartTime = .1
EndTime = .1
@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('!start'):
        await message.channel.send(f'出勤 : ({NOW})')
        StartTime = NOW #出勤時間
    if message.content.startswith('!end'):
        await message.channel.send(f'退勤 : ({NOW})')
        EndTime = NOW #退勤時間
    if message.content.startswith('!rest'):
        await message.channel.send(f'休憩 : ({NOW})')
        OutTime = NOW #出勤時間
    if message.content.startswith('!back'):
        await message.channel.send(f'復帰 : ({NOW})')
        InTime = NOW #退勤時間

client.run(TOKEN)