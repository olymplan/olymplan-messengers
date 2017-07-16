#! /usr/bin/env python
import os
import sys

print('Installing python messenger')

os.chdir('yowsup')

with open('yowsup/env/env.py', 'r') as fenv:
    data = fenv.read()
    data.replace('DEFAULT = "s40"', 'DEFAULT = "android"')
with open('yowsup/env/env.py', 'w') as fenv:
    fenv.write(data)

with open('yowsup/env/env_android.py', 'r') as fenv_android:
    data = fenv_android.readlines()
with open('yowsup/env/env_android.py', 'w') as fenv_android:
    for line in data:
        if '    _MD5_CLASSES' in line:
            fenv_android.write('    _MD5_CLASSES = "1naz8gL5pIYWbtaOZ3207g=="\n')
        elif '    _VERSION' in line:
            fenv_android.write('    _VERSION = "2.17.16"\n')
        else:
            fenv_android.write(line)

if os.system(sys.executable + ' ./setup.py install') != 0:
    exit('Error while installing yowsup')

print('Successfully installed python messenger')
