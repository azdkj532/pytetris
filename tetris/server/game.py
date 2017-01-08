import os
import logging

logger = logging.getLogger(__name__)

class Game(object):
    def __init__(self, sio, players=None, room_id=None):
        # dict({user_id: User})
        self.sio = sio
        self.players = players or {}
        self.room_id = room_id or os.urandom(16).hex()

    def broadcast(self, message):
        logger.info('[+] Broadcast message: %r' % message)
        self.sio.send(message, room=self.room_id, namespace='/game')

    def remove_user(self, sid):
        user = self.players.get(sid, None)
        if not user:
            return

        del self.players[sid]
        self.broadcast('User "%s" leaved' % user.name)

    def add_user(self, user):
        if user.game:
            return
        user.game = self
        self.players[user.sid] = user
        self.broadcast('User "%s" entered' % user.name)

    def __repr__(self):
        return 'Game(sio=%r, players=%r, room_id=%r)' % (
            self.sio, self.players, self.room_id
        )
