"""Default settings and paths"""

import os

project_name = 'pyorient'
HOME = os.environ['HOME']

# Base folder
PROJECT_DIR = os.path.join(HOME, ".{}".format(project_name))
os.makedirs(PROJECT_DIR, exist_ok=True)

# Config
CFG_PATH = os.path.join(PROJECT_DIR, 'tests.cfg')
if not os.path.exists(CFG_PATH):  # Make config file if it doesn't exist
    with open(CFG_PATH, 'w'):
        pass
