# Copyright 2012 Niko Usai <usai.niko@gmail.com>, http://mogui.it
#
#   this file is part of pyorient
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.

import configparser

from pyorient.defaults import CFG_PATH, TESTING
from pyorient.utils import create_test_section


def get_test_config() -> dict:
    """Returns testing configuration parameters as a dictionary"""
    config = configparser.RawConfigParser()
    config.read(CFG_PATH)

    if not config.has_section('TEST'):
        create_test_section()

    else:
        conf = {
            'server': config.get(TESTING, 'server'),
            'port': config.get(TESTING, 'port'),
            'rootu': config.get(TESTING, 'user'),
            'rootp': config.get(TESTING, 'password'),
            # 'useru': config.get('user', 'user'),
            # 'userp': config.get('user', 'pwd'),
            'database': config.get(TESTING, 'database'),
        }

    return conf
