#! /usr/bin/env python
from subprocess import Popen, PIPE
import string
import random
import hashlib
import json
import os
import sys

print('Configuring whatsapp messenger')

os.chdir('yowsup')
with open('yowsup/env/env.py', 'r') as fenv:
    data = fenv.read()
    data = data.replace('DEFAULT = "s40"', 'DEFAULT = "android"')
with open('yowsup/env/env.py', 'w') as fenv:
    fenv.write(data)

cc = input('Input country code [7]: ').strip() or '7'
mcc = input('Input mobile country code [205]: ').strip() or '205'
phone = ''
while phone == '':
    phone = input('Input phone number: ').strip()
mnc = input('Input operator code (01 - MTS, 02 - Megaphone, 20 - Tele2, 99 - Biline) [01]: ').strip() or '01'

with Popen([sys.executable, './yowsup-cli', 'registration', '--requestcode', 'sms', '--phone', phone, '--cc', cc, '--mcc', mcc, '--mnc', mnc], stderr=PIPE, stdout=PIPE) as proc:
    if proc.wait(60) != 0:
        exit('Error while registering using yowsup-cli')
    data = proc.stderr.read()
    print(proc.stderr.read())
    print(proc.stdout.read())

parsed = json.loads(data.decode('utf-8')[data.find(b'{'):data.find(b'}') + 1]);

if parsed['status'] == 'fail':
    exit('Failed. Reason: {}'.format(parsed['reason']))
if 'pw' not in parsed:
    code = ''
    while (code == ''):
        code = input('Input confirmation code (XXX-XXX): ').strip()

    with Popen([sys.executable, './yowsup-cli', 'registration', '--register', code, '--phone', phone, '--cc', cc], stderr=PIPE, stdout=PIPE) as proc:
        if proc.wait(60) != 0:
            exit('Error while confirming phone number using yowsup-cli')
        data = proc.stderr.read()
        print(proc.stderr.read())
        print(proc.stdout.read())
    parsed = json.loads(data.decode('utf-8')[data.find(b'{'):data.find(b'}') + 1]);

password = parsed['pw']

os.chdir('..')

token = ''.join([random.choice(string.ascii_letters + string.digits) for n in range(64)])
confdict = {'phone': phone, 'password': password, 'token': token}
with open('config.json', 'w') as config:
    config.write(json.dumps(confdict, indent=4))

print('Your secret token: '+token)
print('Successfully configured whatsapp messenger')
