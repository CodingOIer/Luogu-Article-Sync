import os
import sys
import json
import argparse
import requests

uid = '0'
client = '0'
path = ''


def getArgv():
    parser = argparse.ArgumentParser(description="处理命令行参数的示例")
    parser.add_argument('-path', type=str, default='.', help='目标文件夹地址')
    parser.add_argument('-init', action='store_true', help='初始化博客文件')
    parser.add_argument('-add', type=str, help='追踪文件')
    parser.add_argument('-remove', type=str, help='取消追踪文件')
    parser.add_argument('-sync', type=str, help='推送更新')

    return parser.parse_args()


def readList():
    list = json.loads(open(f'{path}/.blog/links.json', 'r').read())


def main():
    global uid, client
    with open('./.config', 'r') as f:
        l = f.readlines()
        uid = l[0]
        while uid[-1] in ['\r', '\n', '/', '\\']:
            uid = uid[:-1]
        client = [1]
        while client[-1] in ['\r', '\n', '/', '\\']:
            client = client[:-1]
    argv = getArgv()
    path = argv.path
    while path[-1] in ['\r', '\n', '/', '\\']:
        path = path[:-1]
    if argv.init:
        os.mkdir(f'{path}/.blog')
        with open(f'{path}/.blog/links.json') as f:
            f.write('{[]}')


if __name__ == '__main__':
    main()
