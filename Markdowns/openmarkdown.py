__author__ = 'DanielAjisafe'

import os
import sys

challenges = '/Users/danielajisafe/Energy-Project/Markdowns/challenges.md' if sys.platform == 'darwin' else \
    r'C:\Users\ajide\Energy-Project\Markdowns\challenges.md'
bugs = '/Users/danielajisafe/Energy-Project/Markdowns/bugs.md' if sys.platform == 'darwin' else r'C:\Users\ajide\Energy-Project\Markdowns\bugs.md'


def open_bugs(where):
    bug = open(bugs)
    if where is 1:
        for num, line in enumerate(bug, 1):
            if '## Bugs to fix' in line:
                lineNumber = num + 1
    elif where is 2:
        for num, line in enumerate(bug, 1):
            if '## Things to do' in line:
                lineNumber = num + 1
    elif where is 3:
        for num, line in enumerate(bug, 1):
            if '## Tasks completed' in line:
                lineNumber = num + 1
    elif where is 4:
        for num, line in enumerate(bug, 1):
            if '### Bugs Fixed' in line:
                lineNumber = num + 1
    os.system(f'code -g {bugs}:{lineNumber}')


print('1. Bugs to Fix  \n2. Things to do \n3. Tasks Completed \n4. Bugs Completed')
i = int(input(''))
while i not in (1, 2, 3, 4):
    print('1. Bugs to Fix  \n2. Things to do \n3. Tasks Completed \n4. Bugs Completed')
    i = int(input(''))

open_bugs(i)
