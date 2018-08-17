__author__ = 'DanielAjisafe'

import os
import sys
import subprocess

challenges = '/Users/danielajisafe/Energy-Project/Markdowns/challenges.md' if sys.platform == 'darwin' else \
    r'C:\Users\ajide\Energy-Project\Markdowns\challenges.md'
bugs = '/Users/danielajisafe/Energy-Project/Markdowns/bugs.md' if sys.platform == 'darwin' else r'C:\Users\ajide\Energy-Project\Markdowns\bugs.md'


def open_bugs():
    bug = open(bugs)
    for num, line in enumerate(bug, 1):
        if '### Bugs to fix' in line:
            lineNumber = num + 1
    os.system(f'code -g {bugs}:{lineNumber}')


open_bugs()
