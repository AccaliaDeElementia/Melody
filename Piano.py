#!/usr/bin/env python
import socket


class Piano(object):
    GOOD = 'GOOD'
    NEUTRAL = 'NEUTRAL'
    BAD = 'BAD'
    OVERPLAYED = 'OVERPLAYED'

    def __init__(self, host='localhost', port=4445, 
                 user='admin', password='admin'):
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        
    def __command(self, command):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((self.host, self.port))
        try:
            s.setblocking(False)
            with s.makefile(mode='rw', buffering=1) as piano:
                resp = []
                piano.write('AS USER %s "%s"\n' %(self.user, self.password))
                piano.write('%s\n' % command)
                piano.write('quit')
                data = piano.readline().strip()
                while data:
                    resp.append(data)
                    data = piano.readline().strip()
        finally:
            s.close()
        return resp

    def __getstatus(self, response, status):
        items = response[::-1]
        for item in items:
            if item.startswith(status):
                parts = item.split(':', 1)
                if len(parts) == 1:
                    return True
                else:
                    return parts[1].strip()
        return None
    
    def __getstatuslist(self, response, status):
        items = []
        for item in response:
            if item.startswith(status):
                parts = item.split(':', 1)
                if len(parts) > 1:
                    items.append(parts[1].strip())
        return items

    def __getsongs(self, response):
        items = []
        data = None
        for item in response:
            print (item)
            parts = item.split(':', 1)
            if parts[0].startswith('203') or parts[0].startswith('204'): # Start of record
                if data: 
                    items.append(data)
                data = {}
            elif data != None:
                if parts[0].startswith('111'): # Artist Id
                    data['ArtistId'] = parts[1].strip()
                elif parts[0].startswith('112'): # Album Name
                    data['Album'] = parts[1].strip()
                elif parts[0].startswith('113'): # Artist
                    data['Artist'] = parts[1].strip()
                elif parts[0].startswith('114'): # Title
                    data['Title'] = parts[1].strip()
                elif parts[0].startswith('115'): # Station
                    data['Station'] = parts[1].strip()
                elif parts[0].startswith('116'): # Rating
                    data['Rating'] = parts[1].strip()
                elif parts[0].startswith('117'): # See Also
                    data['SeeAlso'] = parts[1].strip()
                elif parts[0].startswith('118'): # Cover Art
                    data['CoverArt'] = parts[1].strip()
                elif parts[0].startswith('120'): # Station Rating
                    data['StationRating'] = parts[1].strip()
        return items

    def stations (self):
        items = self.__command('STATIONS LIST')
        return self.__getstatuslist(items, '115')

    def select(self, station=None):
        if not station:
            items = self.__command('SELECT MIX')
        else:
            items = self.__command('SELECT STATION "%s"' % station)
        station = self.__getstatus(items, '109')
        if station:
            if station.startswith('station'):
                station = station[8:]
            elif station.startswith('mix'):
                station = station[4:]
        return station
    
    def play (self):
        response = self.__command('PLAY')
        return self.__getstatus(response, '200 Success')

    def stop (self, now=False):
        if now:
            response = self.__command('STOP')
        else:
            response = self.__command('STOP')
        return self.__getstatus(response, '200 Success')

    def pause (self):
        response = self.__command('PAUSE')
        return self.__getstatus(response, '200 Success')

    def playpause (self):
        response = self.__command('PLAYPAUSE')
        return self.__getstatus(response, '200 Success')

    def status (self):
        response = self.__command('STATUS')
        songs = self.__getsongs(response)
        return songs[0] if songs else None

    def history (self):
        response = self.__command('HISTORY')
        return self.__getsongs(response)

    def queue (self):
        response = self.__command('QUEUE')
        return self.__getsongs(response)

    def skip (self):
        response = self.__command('SKIP')
        return self.__getstatus(response, '200 Success')

    def rate (self, rating=NEUTRAL):
        return self.__getstatus(self.__command('RATE %s' % rating), '200 Success')

if __name__ =='__main__':
    p = Piano()
    r = p.queue()
    print('%r' % r)
 
