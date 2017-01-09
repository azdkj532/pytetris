import os
import logging
from greenlet import GreenletExit
from eventlet import greenthread

logger = logging.getLogger(__name__)

class Game(object):
    def __init__(self, sio, owner, speed=0.75, players={}, room_id=None):
        self.sio = sio
        self.owner = owner
        self.players = players or {} # dict({user_id: User})
        self.room_id = room_id or os.urandom(16).hex()
        self.worker = None # GreenThread
        self.speed = speed # second(s)

    def work(self): # background worker
        self.broadcast('Hello players, this is message from worker!!!')

    def worker_loop(self):
        try:
            while True:
                self.work()
                greenthread.sleep(self.speed)
        except GreenletExit:
            logger.debug('[*] R:%s - Worker exited' % self.room_id)

    def start(self): # start game
        self.worker = greenthread.spawn(self.worker_loop)

    def broadcast(self, message):
        logger.debug('[+] R:%s - Broadcast message: %r' % (self.room_id, message))
        self.sio.send(message, room=self.room_id, namespace='/game')

    def shutdown(self):
        self.broadcast('Goodbye')
        logger.info('[*] R:%s - Room shutting down' % self.room_id)
        for sid in list(self.players):
            self.sio.disconnect(sid, namespace='/game')
            try:
                del self.players[sid]
                logger.warn('[-] R:%s - KeyError (%r) while remove user from room' % (self.room_id, sid))
            except KeyError:
                pass

    def remove_user(self, sid):
        user = self.players.get(sid, None)
        if not user:
            return

        del self.players[sid]
        self.broadcast('User "%s" leaved' % user.name)

        if user is self.owner:
            self.broadcast('Game owner leaved, this game is shutting down.')
            self.shutdown()
            if self.worker:
                self.worker.kill()
                self.worker = None

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
