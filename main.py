import os
import re
import sys
import json
import argparse
import requests

uid = '0'
client = '0'
path = ''


def getGetHeaders():
    return {
        'user-agent': 'CodingOIer\'s Article Sync Helper',
        'referer': 'https://www.luogu.com.cn/',
        'cookie': f'_uid={uid}; __client_id={client};',
        'x-luogu-type': 'content-only',
    }


def getCsrfToken():
    return (
        requests.get(url=f'https://www.luogu.com.cn/', headers=getGetHeaders())
        .text.split("<meta name=\"csrf-token\" content=\"")[-1]
        .split("\">")[0]
    )


def getPostHeaders():
    return {
        'user-agent': 'CodingOIer\'s Article Sync Helper',
        'referer': 'https://www.luogu.com.cn/',
        'cookie': f'_uid={uid}; __client_id={client};',
        'x-csrf-token': getCsrfToken(),
    }


def getArgv():
    parser = argparse.ArgumentParser(description="处理命令行参数的示例")
    parser.add_argument('-path', type=str, default='.', help='目标文件夹地址')
    parser.add_argument('-init', action='store_true', help='初始化博客文件')
    parser.add_argument('-add', type=str, default='NONE', help='追踪文件')
    parser.add_argument('-remote', type=str, default='NONE', help='指定远程文章 id')
    parser.add_argument('-remove', type=str, default='NONE', help='取消追踪文件')
    parser.add_argument('-sync', action='store_true', help='推送更新')

    return parser.parse_args()


def getTitle(content):
    expr = [
        r'^# (.+)',
        r'^## (.+)',
        r'^### (.+)',
    ]
    lines = content.splitlines()
    for x in expr:
        for line in lines:
            match = re.match(x, line)
            if match:
                return match.group(1)
    return None


def readList():
    list = json.loads(open(f'{path}/.blog/links.json', 'r').read())


def init():
    if os.path.dirname(f'{path}/.blog') and not os.path.exists(f'{path}/.blog'):
        os.makedirs(f'{path}/.blog')
    with open(f'{path}/.blog/links.json', 'w') as f:
        f.write('{}')
    print(f'已初始化路径 {path}/，配置文件位于 {path}/.blog/links.json。')


def add(local, remote):
    data = json.loads(open(f'{path}/.blog/links.json', 'r').read())
    data[local] = remote
    with open(f'{path}/.blog/links.json', 'w') as f:
        f.write(json.dumps(data))
    print(f'已增加本地文件文件 {local} 到文章 {remote} 的链接。')


def remove(local):
    data = json.loads(open(f'{path}/.blog/links.json', 'r').read())
    data[local] = 'NONE'
    with open(f'{path}/.blog/links.json', 'w') as f:
        f.write(json.dumps(data))
    print(f'已删除本地文件文件 {local} 到文章的链接。')


def getJson(response):
    try:
        return json.loads(
            response.text.split(
                '<script id="lentille-context" type="application/json">'
            )[1].split('</script>')[0]
        )
    except:
        return {}


def sync():
    data = json.loads(open(f'{path}/.blog/links.json', 'r').read())
    keys = data.keys()
    for x in keys:
        if data[x] == 'NONE':
            continue
        content = open(f'{path}/{x}', 'r', encoding='utf-8').read()
        title = getTitle(content)
        print(f'开始同步本地文件 {x}，目标文章 {data[x]}，标题为 「{title}」')
        response = requests.get(
            url=f'https://www.luogu.com.cn/article/{data[x]}/edit',
            headers=getGetHeaders(),
        )
        if response.status_code == 404:
            print(f'未找到远程文章 {data[x]}。')
        elif response.status_code == 403:
            print(f'没有权限操作远程文章 {data[x]}。')
        elif response.status_code == 200:
            js = getJson(response)
            category = js['data']['article']['category']
            solutionFor = js['data']['article']['solutionFor']
            status = js['data']['article']['status']
            response = requests.post(
                url=f'https://www.luogu.com.cn/api/article/edit/{data[x]}',
                headers=getPostHeaders(),
                json={
                    'title': title,
                    'content': content,
                    'category': category,
                    'solutionFor': solutionFor,
                    'status': status,
                },
            )
            if response.status_code == 200:
                print(f'成功同步本地文件 {x} 到 {data[x]}。')
            else:
                print(f'未知错误，状态码：{response.status_code}。')
        else:
            print(f'未知错误，状态码：{response.status_code}。')


def main():
    global path, uid, client
    with open('./.config', 'r') as f:
        l = f.readlines()
        uid = l[0]
        while uid[-1] in ['\r', '\n', '/', '\\']:
            uid = uid[:-1]
        client = l[1]
        while client[-1] in ['\r', '\n', '/', '\\']:
            client = client[:-1]
    argv = getArgv()
    path = argv.path
    while path[-1] in ['\r', '\n', '/', '\\']:
        path = path[:-1]
    if argv.init:
        init()
    if argv.add != 'NONE':
        add(argv.add, argv.remote)
    if argv.remove != 'NONE':
        remove(argv.remove)
    if argv.sync:
        sync()


if __name__ == '__main__':
    main()
