import re
import json
import time
import requests
import os

with open('epic.log', 'r') as log:
    log = log.readlines()
# print(log)
hook_content = []
emoji = {'WARN': ':warning: ', 'INFO': ':information_source: ',
         'EMAIL': ':e_mail: ', 'SUCCESS': ':ballot_box_with_check: ',
         'ALREADY': ':interrobang: ', 'LEAVE': ':leaves: ', 'USER': ':video_game: '}
index = []
webhook_url = os.getenv('Discord_Webhook')
for i in log[3:]:
    ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
    result = ansi_escape.sub('', i).strip().split('|')
    result = [i.strip() for i in result]
    try:
        email = re.search(r'[A-Za-z0-9.+_-]+@[A-Za-z0-9._-]+', result[3])
        user = re.search(r'(?<=Logged in as ).+?(?= )', result[3])
        email = email.group(0) if email else None
        user = user.group(0) if user else None
        if email:
            result = {'name': emoji['EMAIL'] + 'EMAIL', 'value': email, 'inline': True}
        elif user:
            result = {'name': emoji['USER'] + 'USER', 'value': user, 'inline': True}
        elif 'was already claimed for this account' in result[3]:
            result = {'name': emoji['ALREADY'] + 'ALREADY', 'value': result[3]}
        elif 'Successfully claimed' in result[3]:
            result = {'name': emoji['SUCCESS'] + 'SUCCESS', 'value': result[3]}
        elif re.search('Logged .+? out of Epic Games', result[3]):
            result = {'name': emoji['LEAVE'] + 'LEAVE', 'value': result[3]}
        else:
            result = {'name': emoji[result[2]] + result[2], 'value': result[3]}
    except IndexError:
        continue
    # print(result)
    hook_content.append(result)
# print(hook_content)
for a in hook_content:
    if 'out of Epic Games' in a['value']:
        index.append(hook_content.index(a))
discord_hook = {
    "username": "Epic Log",
    "avatar_url": "https://i.imgur.com/4M34hi2.png",
    "content": "",
    "embeds": [
        {
            "author": {
                "name": "Log Bot",
                "url": "https://github.com/scatking/epicgames-freebies-claimer",
                "icon_url": "https://i.imgur.com/R66g1Pe.jpg"
            },
            "title": "Claim Log",
            "url": "https://github.com/scatking/epicgames-freebies-claimer",
            "description": "Here is your free game log at " + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
            "color": 15258703
        },
    ]
}
for b in index:
    num = index.index(b)
    prev = 0 if num == 0 else index[num - 1]
    discord_hook['embeds'][0]['fields'] = hook_content[prev + 1:b + 1]
    # print(discord_hook['embeds'][0]['fields'])
    with open('webhook.json', 'w') as webhook:
        json.dump(discord_hook, webhook)
    if webhook_url:
        requests.post(webhook_url, json=discord_hook)
