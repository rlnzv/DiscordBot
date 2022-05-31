import discord
import datetime as date
import yaml

def getFtTime():
    return date.datetime.now().strftime('%Y/%m/%d %H:%M:%S')

# login method
client = discord.Client()
with open('config.yaml') as config:
    yf = yaml.safe_load(config)
    global TOKEN
    TOKEN = yf['token'] 
if TOKEN is None:
    print('Not found valid token')
    exit()
    
users_working = {}
users_rest = {}

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    id = message.author.id
    if message.content.startswith('!start'):
        if id not in users_working:
            msg = await message.channel.send('出勤: ' + getFtTime())
            users_working = {id: date.datetime.now()}
            users_rest = {id: date.datetime.now()}
        else:
            await message.channel.send('すでに出勤処理をしています。')
    elif message.content.startswith('!end'):
        if id in users_working:
            calc = date.datetime.now() - users_working[id]
            users_working.delete(id)
            await message.channel.send()
            
        else:
            await message.channel.send('出勤処理をしていません。')

    """
    if message.content.startswith('!start'):
        await message.channel.send(f'出勤 : ({NOW})')
        StartTime = NOW #出勤時間
        working_users[message.author.getId()] = date.datetime.now()
    if message.content.startswith('!end'):
        await message.channel.send(f'退勤 : ({NOW})')
        EndTime = NOW #退勤時間
        if message.author.getId() not in total_times:
            total_times[message.author.getId()] = 0
        total_times[message.author.getId()] += (EndTime - working_users[message.author.getId()]).total_seconds()    
        working_users[message.author.getId()] = 0
    if message.content.startswith('!rest'):
        await message.channel.send(f'休憩 : ({NOW})')
        OutTime = NOW #出勤時間
        working_users[message.author.getId()] = 
    if message.content.startswith('!back'):
        await message.channel.send(f'復帰 : ({NOW})')
        InTime = NOW #退勤時間
    """

client.run(TOKEN)
