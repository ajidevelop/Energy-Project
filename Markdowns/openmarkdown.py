__author__ = 'DanielAjisafe'

import os
import sys

challenges = '/Users/danielajisafe/Energy-Project/Markdowns/challenges.md' if sys.platform == 'darwin' else \
    r'C:\Users\ajide\Energy-Project\Markdowns\challenges.md'
bugs = '/Users/danielajisafe/Energy-Project/Markdowns/bugs.md' if sys.platform == 'darwin' else r'C:\Users\ajide\Energy-Project\Markdowns\bugs.md'


def open_bugs(where, bn=None):
    bug = open(bugs)
    if bn is not None:
        for num, line in enumerate(bug, 1):
            if f'- #{bn}' in line:
                lineNumber = num
    else:
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


def open_challenges():
    challenge = open(challenges)
    line_number = 1
    for num, line in enumerate(challenge, 1):
        if line_number > num:
            break
        else:
            line_number += 1
    os.system(f'code -g {challenges}:{line_number}')


def open_file_1():
    try:
        print('1. Bugs and Todo List \n2. Challenges')
        try:
            i = int(input(''))
        except ValueError:
            open_file_1()
        if i in (1, 2):
            open_file_2(i)
        else:
            open_file_1()
    except UnboundLocalError:
        pass


def open_file_2(i):
    if int(i) == 1:
        print('1. Bugs to Fix  \n2. Things to do \n3. Tasks Completed \n4. Bugs Completed')
        try:
            d = int(input(''))
        except ValueError:
            open_file_2(i)
        if d is 4:
            var = False
            while var is False:
                try:
                    ln = int(input('Bug Number: '))
                    var = True
                except TypeError:
                    pass
            open_bugs(d, ln)
        if d in (1, 2, 3, 4):
            open_bugs(d)
        else:
            open_file_2(i)
    else:
        open_challenges()


open_file_1()
