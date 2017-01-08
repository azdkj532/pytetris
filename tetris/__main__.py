import logging
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

logging.basicConfig(level=logging.INFO)

import tetris

if 'serve' in sys.argv:
    tetris.server.start()
