import time
import logging
import functools

from ..game import GameBoard
from eventlet.semaphore import Semaphore

logger = logging.getLogger(__name__)

class User(object):
    def __init__(self, sid, name=None, game=None, board=None):
        self.sid = sid
        self.name = name or ('User_%s' % sid[:12])
        self.game = None
        self.board = GameBoard()
        self.board_lock = Semaphore(1)
        self.op_map = {
            'BOOM': self.board.down,
            'MOVE_LEFT': functools.partial(self.board.move, -1),
            'MOVE_RIGHT': functools.partial(self.board.move, 1),
            'ROTATE_RIGHT': functools.partial(self.board.rotate, 'right'),
            'ROTATE_LEFT': functools.partial(self.board.rotate, 'left')
        }

    def send(self, op):
        act = self.op_map.get(op, None)
        if not act:
            return

        with self.board_lock:
            act()
            self.report_state()

    def report_state(self):
        self.game.sio.emit('board state', data=str(self.board), room=self.sid, namespace='/game')

    def __repr__(self):
        return 'User(sid=%r, game=%r, name=%r, board=%r)' % (
            self.sid, self.game, self.name, self.board
        )
