import os
import logging
import functools

import eventlet; eventlet.monkey_patch()
import socketio

from bottle import Bottle, view, post, get, request, response, run, static_file

from .game import Game
from .user import User

ASSETS_PATH = os.path.join(os.path.dirname(__file__), 'assets')
VIEW_PATH = os.path.join(os.path.dirname(__file__), 'html')

logger = logging.getLogger(__name__)

# setup bottle template path
view = functools.partial(view, template_lookup=[VIEW_PATH])

# create server objects
sio = socketio.Server()
bottle = Bottle()
app = socketio.Middleware(sio, bottle)

# dict({room_id: Game})
games = {}

# dict({user_id: User})
users = {}

def user_event(*args, **kwargs):
    def wrapper(func):
        pre_cond = kwargs.pop('pre_cond', None)
        def hook(sid, *args):
            user = users.get(sid, None)
            if not user or (pre_cond and not pre_cond(user)):
                return
            func(user, *args)
        namespace = kwargs.pop('namespace', '/game')
        sio.on(*args, namespace=namespace, **kwargs)(hook)
    return wrapper

def game_event(*args, **kwargs):
    def wrapper(func):
        pre_cond = kwargs.pop('pre_cond', None)
        def hook(user, *args):
            if not user.game or (pre_cond and not pre_cond(user, user.game)):
                return
            func(user, user.game, *args)
        namespace = kwargs.pop('namespace', '/game')
        user_event(*args, namespace=namespace, **kwargs)(hook)
    return wrapper

@bottle.get('/')
def index():
    return static_file('index.html', root = VIEW_PATH)

@bottle.get('/assets/<file:path>')
def assets(file):
    return static_file(file, root=ASSETS_PATH)

# connect and disconnect control

@sio.on('connect', namespace='/game')
def connect(sid, environ):
    user = User(sio, sid)
    users[sid] = user
    logger.info('[+] U:%s - User connected' % sid)
    user.emit('user id', sid)

@sio.on('disconnect', namespace='/game')
def disconnect(sid):
    game = users[sid].game
    if game: game.remove_user(sid)
    del users[sid]
    logger.info('[+] U:%s - User disconnected' % sid)

    for room_id, game in list(games.items()):
        if not game.players:
            del games[room_id]
            logger.info('[+] R:%s - Room removed' % room_id)

# room control

@user_event('create room')
def create_room(user, *_):
    game = Game(sio, user)
    sio.enter_room(user.sid, game.room_id, namespace='/game')

    games[game.room_id] = game
    game.add_user(user)

    logger.info('[+] U:%s - User created room %s' % (user.sid, game.room_id))
    game.emit('room id', game.room_id)

@user_event('join room', pre_cond=lambda user: not user.game)
def join_room(user, room_id):
    game = games.get(room_id, None)

    if not game:
        return

    game.add_user(user)
    sio.enter_room(user.sid, game.room_id, namespace='/game')
    game.emit('room id', game.room_id)
    logger.info('[+] U:%s - User joined room %s' % (user.sid, room_id))

# user control
@user_event('set name')
def set_name(user, name):
    old_name, user.name = user.name, name

    if user.game:
        user.game.broadcast('User %s renamed to %s' % (old_name, name))
        logger.info('[+] U:%s - User renamed from %r to %r' % (user.sid, old_name, name))

@game_event('start game', pre_cond=lambda user, game: user is game.owner)
def start_game(user, game):
    user.game.start()

@game_event('game input', pre_cond=lambda user, game: game.started)
def game_input(user, game, op):
    user.send(op)

def start(host='0.0.0.0', port=8080):
    run(app=app, host=host, port=port, server='eventlet')
