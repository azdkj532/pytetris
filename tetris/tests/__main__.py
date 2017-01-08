import logging
import os
import sys

logging.basicConfig(level=None)

# setup path for tetris package
sys.path = [os.path.join(os.path.dirname(__file__), 'mocks')] + sys.path + [os.path.join(os.path.dirname(__file__), '../..')]

import unittest

# import tests
from test_blocks import *
from test_game_board import *

if __name__ == '__main__':
    unittest.main()
