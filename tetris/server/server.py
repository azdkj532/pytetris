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

@bottle.get('/')
def index():
    return static_file('index.html', root = VIEW_PATH)

@bottle.get('/assets/<file:path>')
def assets(file):
    return static_file(file, root=ASSETS_PATH)

# connect and disconnect control

@sio.on('connect', namespace='/game')
def connect(sid, environ):
    users[sid] = User(sid)
    print('[+] User connected, sid = %s' % sid)

@sio.on('disconnect', namespace='/game')
def disconnect(sid):
    game = users[sid].game
    if game: game.remove_user(sid)
    del users[sid]
    print('[+] User disconnected, sid = %s' % sid)

# room control

@sio.on('create room', namespace='/game')
def create_room(sid, *_):
    user = users.get(sid, None)
    if not user:
        return

    game = Game(sio, user)
    sio.enter_room(sid, game.room_id, namespace='/game')

    games[game.room_id] = game
    game.add_user(user)

    print('[+] User %s created room %s' % (sid, game.room_id))
    sio.emit('room id', data=game.room_id, room=game.room_id, namespace='/game')

@sio.on('join room', namespace='/game')
def join_room(sid, room_id):
    game = games.get(room_id, None)
    user = users.get(sid, None)

    if not game or not user or user.game:
        return

    game.add_user(user)
    sio.enter_room(user.sid, game.room_id, namespace='/game')
    sio.emit('room id', data=game.room_id, room=game.room_id, namespace='/game')

# user control
@sio.on('set name', namespace='/game')
def set_name(sid, name):
    user = users.get(sid, None)
    if not user:
        return
    old_name = user.name
    user.name = name

    if user.game:
        user.game.broadcast('User %s renamed to %s' % (old_name, name))

def start(host='0.0.0.0', port=8080):
    run(app=app, host=host, port=port, server='eventlet')
