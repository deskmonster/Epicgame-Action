import re
import json
import time

with open('epic.log', 'r') as log:
    log = log.readlines()
# print(log)
hook_content = []
emoji = {'WARN': ':warning: ', 'INFO': ':information_source: '}
for i in log[3:]:
    ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
    result = ansi_escape.sub('', i).strip().split('|')
    result = [i.strip() for i in result]
    try:
        result = {'name': emoji[result[2]] + result[2], 'value': result[3]}
    except IndexError:
        continue
    # print(result)
    hook_content.append(result)
# print(hook_content)
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
discord_hook['embeds'][0]['fields'] = hook_content
# print(discord_hook)
with open('webhook.json','w') as webhook:
    json.dump(discord_hook,webhook)