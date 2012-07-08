#!/usr/bin/env python

# (c) 2012 - Accalia de Elementia

import sys
from os import environ
from json import loads, dumps
from urllib.request import Request, urlopen
from xmlrpc.client import ServerProxy
from argparse import ArgumentParser


isatty = sys.stdout.isatty()

ENVIRON = [
    { 
        'name': 'server', 'environ': 'OCTAVIA_REMOTE_SERVER',
        'default': 'localhost', 'type': str,
    },
    { 
        'name': 'port', 'environ': 'OCTAVIA_REMOTE_PORT',
        'default': 8080, 'type': int,
    },
    {
        'name': 'type', 'environ': 'OCTAVIA_TRANSFER_TYPE',
        'default': 'JSON', 'values': ['JSON', 'XML'],
    }
]
METHODS = [
    {
        'name': 'playlist', 'method': 'queueList',
        'help': 'Prints entire playlist', 'formatter': 'list_songs'
    },
    {
        'name': 'add', 'method': 'queueAdd', 'params': ['path'],
        'multiple': ['path'], 'formatter': 'list_songs',
        'help': 'Add songs from the music database to the playlist.',
    },
    {
        'name': 'ls', 'method': 'libraryList', 'params': ['path'],
        'defaults': ['path'], 'formatter': 'list_library',
        'help': 'List all songs/directories in <path>.',
    },
    {
        'name': 'clear', 'method': 'queueClear',
        'help': 'Empties playlist.', 'formatter': 'list_songs'
    },
    {
        'name': 'current', 'method': 'queueCurrent',
        'help': 'Show the currently playing song.', 'formatter': 'song'
    },
    {
        'name': 'next', 'method': 'queueNext', 'formatter': 'song',
        'help': 'Starts playing next song on playlist.'
    },
    {
        'name': 'prev', 'method': 'queuePrev', 'formatter': 'song',
        'help': 'Starts playing previous song.'
    },
    {
        'name': 'stop', 'method': 'queueStop', 'formatter': 'song',
        'help': 'Stops playing'
    },
    {
        'name': 'play', 'method': 'queuePlay', 'params': ['position'],
        'defaults': ['position'], 'formatter': 'song',
        'help': 'Starts playing the song-number specified. if none is specified, plays number 1.'
    },
    {
        'name': 'pause', 'method': 'queuePause', 'formatter': 'song',
        'help': 'Pauses playing'
    },
    {
        'name': 'toggle', 'method': 'queueToggle', 'formatter': 'song',
        'help': 'Toggles between play and pause. If stopped starts playing. Does not support start playing at song number (use play).'
    }
]
METHODS.sort(key=lambda x: x['name'])

def get_argument_parser():
    getlist = lambda x, y: x.get(y, [])
    parser = ArgumentParser()
    for env in ENVIRON:
        _default = (environ[env['environ']] if env['environ'] in environ 
                    else env['default'])
        args = ['--'+env['name'], '-'+env['name'][1]]
        kwargs = {'default': _default}
        if 'values' in env: kwargs['choices'] = env['values']
        if 'type' in env: kwargs['type'] = env['type']
        parser.add_argument(*args, **kwargs)
    subparsers = parser.add_subparsers(title='Commands')
    for method in METHODS:
        mparser = subparsers.add_parser(method['name'], help=method['help'])
        mparser.set_defaults(params=[], definition=method)
        for param in getlist(method, 'params'):
            args = [param]
            kwargs={}
            if param in getlist(method, 'defaults'): kwargs['nargs']='?'
            if param in getlist(method, 'multiple'): kwargs['nargs']='*'
            mparser.add_argument(*args, **kwargs)
    return parser

class Response (object):
    def __init__(self, response, formatter):
        self.raw = response
        self.formatter = formatter

    def __str__(self):
        return self.formatter(self.raw)

    def __repr__(self):
        return dumps(self.raw, indent=4)

class Executor (object):
    class ExecutorException(Exception): pass

    def __init__(self, server, port, type_):
        self.server = server
        self.port = port
        self.id = 0
        self.type = type_

    def execute(self, command, params):
        return {
            'JSON': self.execute_json,
            'XML': self.execute_xml
        }.get(self.type, self.execute_json)(command, params)

    def execute_json(self, command, params):
        if not params: params = []
        self.id += 1
        method = {
            'jsonrpc': '2.0', 
            'method': command,
            'params': params,
            'id': self.id
        }
        headers = {
            'Content-Type': 'application/json'
        }
        url = 'http://%s:%s/json' %(self.server, self.port)
        request = Request(url, dumps(method).encode('utf8'), headers)
        res = urlopen(request).read()
        response = loads(res.decode('utf8'))
        if response.get('error', None):
            raise Executor.ExecutorException('%s - %s' % (response['error']['message'], response['error']['data']))
        return response['result']

    def execute_xml(self, command, params):
        if not params: params = []
        proxy = ServerProxy('http://%s:%s/xml'%(self.server,self.port))
        return getattr(proxy, command)(*params)

def get_formatter(name):
    def as_song(obj):
        if not isatty or (not obj['artist'] and not obj['title']):
            return obj['file']
        return '%s - %s'%(obj['artist'], obj['title'])
    def as_songs(objs):
        return '\n'.join([as_song(obj) for obj in objs])
    def as_library(objs):
        def name (obj):
            names = ['file', 'directory']
            for name in names:
                if name in obj:
                    return obj[name]
            return None
        return '\n'.join(filter(lambda x: x is not None, 
                            [name(x) for x in objs]))
    return {
        'song': as_song,
        'list_songs': as_songs,
        'list_library': as_library,
    }.get(name, lambda x: dumps(x))

if __name__ == '__main__':
    import sys, codecs
    # Force UTF8 encoding
    sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())
    sys.stdin = codecs.getwriter("utf-8")(sys.stdin.detach())

    parser = get_argument_parser()
    args = parser.parse_args()

    method = args.definition
    params = []
    for parm in method.get('params', []):
        arg = getattr(args, parm, None)
        if getattr(args, parm, False):
            params.append(getattr(args, parm))
        elif parm in method.get('multiple',[]):
            y = sys.stdin.readlines()
            params.append([ x.decode('utf8').rstrip('\n') for x in y])
            
    executor = Executor(args.server, args.port, args.type)
    value = executor.execute(method['method'], params)

    formatter = get_formatter(method['formatter'])
    print (formatter(value))

