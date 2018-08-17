__author__ = 'DanielAjisafe'

import os
import sys
import subprocess

challenges = '/Users/danielajisafe/Energy-Project/Markdowns/challenges.md' if sys.platform == 'darwin' else ''
bugs = '/Users/danielajisafe/Energy-Project/Markdowns/bugs.md' if sys.platform == 'darwin' else ''


def open_file(filename):
    if sys.platform == 'win32':
        os.startfile(filename)

    opener = 'open' if sys.platform == 'darwin' else 'xdg-open'
    subprocess.call([opener, filename])


def open_bugs(filename=''):
    bug = open(bugs)
    for num, line in enumerate(bug, 1):
        if '### Bugs to fix' in line:
            lineNumber = num + 1
    if sys.platform == 'win32':
        os.startfile(filename)
    elif sys.platform == 'darwin':
        os.system(f'code -g {bugs}:{lineNumber}')


open_bugs()
