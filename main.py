import discord
from datetime import datetime, timedelta, timezone
import yaml

JST = timezone(timedelta(hours=+9), 'JST')

def getFtTime():
    return datetime.now(JST).strftime('%Y/%m/%d %H:%M:%S')

def fillZeroTime(d):
    if len(d.split(':')[0]) == 1:
        d = '0' + d
    d = d.split('.')[0]
    return d

def writeLog(log):
    with open('log.txt', 'a') as f:
        f.write(log + '\n')
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
        users_working[id] = datetime.now(JST)
        # users_rest[id] = date.datetime.now()
        await message.channel.send(message.author.mention + ' \n出勤: ' + getFtTime())
        writeLog('ID: ' + str(id) + ' | 出勤: ' + getFtTime())

    elif message.content.startswith('!end'):
        if id in users_working:
            calc = datetime.now(JST) - users_working[id]
            users_working.pop(id)
            if id in users_rest:
                users_rest.pop(id)
            await message.channel.send(message.author.mention + ' \n退勤: ' + getFtTime() + ' \n出勤時間: ' + fillZeroTime(str(calc)))
            writeLog('ID: ' + str(id) + ' | 退勤: ' + getFtTime() + ' | 出勤時間: ' + fillZeroTime(str(calc)))
        else:
            msg = await message.channel.send(message.author.mention + ' \n出勤処理をしていません。')
            await msg.delete(delay=10) # 10秒後に削除
            await message.delete() # 元のメッセージを削除
            return
        
    elif message.content.startswith('!rest'):
        if id in users_rest:
            msg = await message.channel.send(message.author.mention + ' \n既に休憩処理をしています。')
            await msg.delete(delay=10)
            await message.delete()
            return
        elif id not in users_working:
            msg = await message.channel.send(message.author.mention + ' \n出勤処理をしていません。')
            await msg.delete(delay=10)
            await message.delete()
            return
        users_rest[id] = datetime.now(JST)
        await message.channel.send(message.author.mention + ' \n休憩: ' + getFtTime())
        writeLog('ID: ' + str(id) + ' | 休憩: ' + getFtTime())
    
    elif message.content.startswith('!back'):
        if id in users_rest:
            calc = datetime.now(JST) - users_rest[id]
            users_rest.pop(id)
            # reduce rest time from working time
            users_working[id] = users_working[id] - calc
            await message.channel.send(message.author.mention + ' \n復帰: ' + getFtTime() + ' \n休憩時間: ' + fillZeroTime(str(calc)))
            writeLog('ID: ' + str(id) + ' | 復帰: ' + getFtTime() + ' | 休憩時間: ' + fillZeroTime(str(calc)))
        else:
            msg = await message.channel.send(message.author.mention + ' \n休憩処理をしていません。')
            await msg.delete(delay=10)
            await message.delete()
            return

client.run(TOKEN)
