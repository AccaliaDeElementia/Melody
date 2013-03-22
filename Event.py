#!/usr/bin/env python

from warnings import warn

class _EventDispatcher (object):
    def __init__(self):
        self.events = set()
        self.__listeners = {}

    def register(self,  event):
        if event in self.events:
            warn('Event "%s" is already subscribed.' % event)
            return
        if event in self.__listeners.keys():
            warn(('Handlers are already listening for unregistered ' +
                  'event "%s"') % event)
        self.events.add(event)

    def unregister(self, event):
        if event not in self.events:
            return
        try:
            self.events.remove(event)
        except:
            pass

    def subscribe(self, event, handler):
        if event not in self.events:
            warn(('Event "%s" is not registered. handler might ' +
                  'never execute.') % event)
        if event not in self.__listeners.keys():
            self.__listeners[event] = set()
        self.__listeners[event].add(handler)
        
    def unsubscribe(self, event, handler):
        if event in self.__listeners.keys():
            try:
                self.__listeners[event].remove(handler)
            except:
                pass

    def publish(self, event, *args, **kwargs):
        if event not in self.__listeners.keys():
            return
        for handler in self.__listeners[event]:
            handler(*args, **kwargs)
EventDispatcher = _EventDispatcher()

if __name__ == '__main__':
    def h (x):
        print('Handled: %s' % x)
    EventDispatcher.register('foo')
    EventDispatcher.publish('foo', 'Event1')
    EventDispatcher.subscribe('foo', h)
    EventDispatcher.publish('foo', 'Event2')
    EventDispatcher.unsubscribe('foo', h)
    EventDispatcher.publish('foo', 'Event3')
    EventDispatcher.unsubscribe('foo', h)

