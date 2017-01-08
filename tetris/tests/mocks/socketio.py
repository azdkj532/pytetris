import os
from collections import deque

MOCK = True

class NameSpace(object):
    def __init__(self, name):
        self.name = name
        self.handler = {}
        self.emit_queue = deque()
        self.rooms = {}

    def __repr__(self):
        return 'NameSpace(name=%r, handler=%r, emit_queue=%r, rooms=%r)' % (
            self.name, self.handler, self.emit_queue, self.rooms
        )

class Message(object):
    def __init__(self, event, data, room, skip_sid):
        self.event = event
        self.data = data
        self.room = room
        self.skip_sid = skip_sid

    def __repr__(self):
        return 'Message(event=%r, data=%r, room=%r, skip_sid=%r)' % (
            self.event, self.data, self.room, self.skip_sid
        )

class Client(object):
    def __init__(self, server, namespace, sid=None):
        self.sid = sid or os.urandom(12).hex()
        self.server = server
        self.namespace = namespace
        self.emit('connect', {}, namespace)

    def emit(self, event, data, namespace='DUMMY_NAME_SPACE'):
        if namespace == 'DUMMY_NAME_SPACE':
            namespace = self.namespace
        self.server.mock_send_event(self, event, data, namespace)

class Server(object):
    def __init__(self):
        self.namespaces = {}

    def get_namespace(self, name):
        if name in self.namespaces:
            return self.namespaces[name]
        else:
            return self.namespaces.setdefault(name, NameSpace(name))

    def mock_send_event(self, client, event, data, namespace=None):
        """
        enumerate client send event
        """
        NS = self.get_namespace(namespace)
        for handler in NS.handler.get(event, []):
            handler(client.sid, data)

    def on(self, event, handler=None, namespace=None):
        if handler:
            self.get_namespace(namespace).handler.setdefault(event, []).append(handler)
        else:
            return lambda handler: self.on(event, handler, namespace)

    def send(self, data, room=None, skip_sid=None, namespace=None, callback=None, **kwargs):
        self.emit('message', data, room, skip_sid, namespace, callback, **kwargs)

    def emit(self, event, data=None, room=None, skip_sid=None, namespace=None, callback=None, **kwargs):
        NS = self.get_namespace(namespace)
        data = data or kwargs
        NS.emit_queue.append(Message(event, data, room, skip_sid))

    def enter_room(self, sid, room, namespace=None):
        self.get_namespace(namespace).rooms.setdefault(room, set()).add(sid)

    def leave_room(self, sid, room, namespace=None):
        try:
            rooms = self.get_namespace(namespace).rooms
            rooms.setdefault(room, set()).remove(sid)
        except KeyError:
            pass

    def close_room(self, room, namespace=None):
        rooms = self.get_namespace(namespace).rooms
        rooms.pop(room, None)

def Middleware(a, b):
    return a
