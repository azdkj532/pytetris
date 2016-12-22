import sys, os
# setup path for tetris package
sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))

import unittest

# import tests
from blocks import *

if __name__ == '__main__':
    unittest.main()
