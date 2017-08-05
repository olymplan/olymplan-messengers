import sys
import json
from stack import BotStack
from yowsup.env import YowsupEnv
from sys import argv

if len(argv) == 2:
    port = int(argv[1])
else:
    port = 80

YowsupEnv.setEnv('s40')

with open('config.json', 'r') as config:
    data = json.loads(config.read())

credentials = (data['phone'], data['password'])
token = data['token']

try:
    stack = BotStack(credentials, True, token=token, port=3000)
    print('Starting.')
    stack.start()
except KeyboardInterrupt:
    print("\nInterrupted.")
    sys.exit(0)