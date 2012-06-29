#!/usr/bin/python

from argparse import ArgumentParser
from os import environ

from RemoteMethods import Methods

ENVIRON_SERVER = 'OCTAVIA_REMOTE_SERVER'
ENVIRON_PORT = 'OCTAVIA_REMOTE_PORT'
parser = ArgumentParser()

server_default = (environ[ENVIRON_SERVER] if ENVIRON_SERVER in environ 
                    else 'localhost')
parser.add_argument('--server', '-s', default=server_default)
port_default = (int(environ[ENVIRON_PORT]) if ENVIRON_PORT in environ
                    else 8080)
parser.add_argument('--port', '-p', default=port_default, type=int)

parser.add_argument('--type', '-t', default='JSON', choices=['JSON', 'XML'])

subparsers = parser.add_subparsers(title='Commands', help="Available Commands")
for method in Methods:
    mparse = subparsers.add_parser(method['method'], help=method['help'])
    mparse.set_defaults(_method=method['method'])
    for param in method['params']:
        required = param not in method['defaults']
        if required:
            mparse.add_argument(param)
        else:
            mparse.add_argument(param, nargs='?')
