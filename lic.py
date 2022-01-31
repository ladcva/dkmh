"""
 This is the default license template.
 
 File: lic.py
 Author: mac
 Copyright (c) 2022 mac
 
 To edit this license information: Press Ctrl+Shift+P and press 'Create new License Template...'.
"""

import re
from termcolor import colored

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

pattern = "[a-zA-Z0-9]+@[a-zA-Z]+\.(com|edu|net)"
user_input = 'ladcva@yahoo.com'

if re.search(pattern, user_input):
    print(f'{bcolors.OKGREEN}{user_input}{bcolors.ENDC} is a valid email !!')
else:
    print('Not valid !')

import sys
from termcolor import colored, cprint

text = colored('Hello, World!', 'red', attrs=['reverse', 'blink'])
print(text)
cprint('Hello, World!', 'green', 'on_red')

print_red_on_cyan = lambda x: cprint(x, 'red', 'on_cyan')
print_red_on_cyan('Hello, World!')
print_red_on_cyan('Hello, Universe!')

for i in range(10):
    cprint(i, 'magenta', end=' ')

cprint("Attention!", 'red', attrs=['bold'], file=sys.stderr)