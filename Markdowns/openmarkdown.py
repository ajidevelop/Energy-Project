__author__ = 'DanielAjisafe'

import os, sys, subprocess

def open_file(filename):
    if sys.platform == 'win32':
        os.startfile(filename)
    opener = 'open' if sys.platform == 'darwin' else 'xdg-open'
    subprocess.call([opener, filename])


challenges = '/Users/danielajisafe/Energy-Project/Markdowns/challenges.md' if sys.platform == 'darwin' else ''
bugs = '/Users/danielajisafe/Energy-Project/Markdowns/bugs.md' if sys.platform == 'darwin' else ''

open_file(challenges)
