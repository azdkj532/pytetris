import logging
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

logging.basicConfig(level=logging.INFO)
logging.getLogger('engineio').setLevel(logging.WARN)
logging.getLogger('socketio').setLevel(logging.WARN)

import tetris

if 'serve' in sys.argv:
    tetris.server.start()
