import time
import logging
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

    def send(self, op):
        if type(op) is not str:
            return

        with self.board_lock:
            if op == 'BOOM':
                self.board.down()
            elif op == 'MOVE_LEFT':
                self.board.move(-1)
            elif op == 'MOVE_RIGHT':
                self.board.move(1)
            elif op == 'ROTATE_RIGHT':
                self.board.rotate('right')
            elif op == 'ROTATE_LEFT':
                self.board.rotate('left')

        self.game.sio.emit('board state', data=str(self.board), room=self.sid, namespace='/game')

    def __repr__(self):
        return 'User(sid=%r, game=%r, name=%r, board=%r)' % (
            self.sid, self.game, self.name, self.board
        )
