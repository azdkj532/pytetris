import time
import logging
from ..game import GameBoard

logger = logging.getLogger(__name__)

class User(object):
    def __init__(self, sid, name=None, game=None, board=None):
        self.sid = sid
        self.name = name or ('User_%s' % sid[:12])
        self.game = None
        self.board = GameBoard()

    def __repr__(self):
        return 'User(sid=%r, game=%r, name=%r, board=%r)' % (
            self.sid, self.game, self.name, self.board
        )
