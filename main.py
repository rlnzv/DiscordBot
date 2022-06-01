import discord
import datetime as date
import yaml

def getFtTime():
    return date.datetime.now().strftime('%Y/%m/%d %H:%M:%S')

def formatTime(sec):
    return fillZero(sec//3600) + ':' + fillZero(sec%3600//60) + ':' + fillZero(sec%60)

def fillZero(num):
    return '0' + str(num) if num < 10 else str(num)

def writeLog(log):
    with open('log.txt', 'a') as f:
        f.write(log + '\n')
    # console
    print(log)

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
        if id in users_working:
            msg = await message.channel.send(message.author.mention + ' \n既に出勤処理をしています。')
            await msg.delete(delay=10) # 10秒後に削除
            await message.delete() # 元のメッセージを削除
            return
        users_working[id] = date.datetime.now()
        users_rest[id] = date.datetime.now()
        await message.channel.send(message.author.mention + ' \n出勤: ' + getFtTime())
        writeLog('ID: ' + str(id) + ' | 出勤: ' + getFtTime())

    elif message.content.startswith('!end'):
        if id in users_working:
            calc = date.datetime.now() - users_working[id]
            calc = calc.seconds
            users_working.pop(id)
            await message.channel.send(message.author.mention + ' \n退勤: ' + getFtTime() + ' \n出勤時間: ' + formatTime(calc))
            writeLog('ID: ' + str(id) + ' | 退勤: ' + getFtTime() + ' | 出勤時間: ' + formatTime(calc))
        else:
            msg = await message.channel.send(message.author.mention + ' \n出勤処理をしていません。')
            await msg.delete(delay=10) # 10秒後に削除
            await message.delete() # 元のメッセージを削除
            return
    
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
