# Copyright (c) Intamixx

"""
Shoutcast client to update TuneIn station playing now information using broadcaster api. Run with:

python shoutcast.py <shoutcast server ip> <port>
"""

# Import required libraries, raise an exception if not installed
try:
        import socket
        import sys
        import os
        import pycurl
        import cStringIO
        import getopt
except ImportError as e:
        print "\n%s is installed. Please install it before running this script." % (e)
        exit (1)

# TuneIn credentials
partnerId = "xxxxxxx"
partnerKey = "xxxxxxxxx"
id = "xxxxxx"

from twisted.internet import protocol, reactor
from twisted.protocols.shoutcast import ShoutcastClient

def check_server(host, port):
        # Create a TCP socket
                s = socket.socket()
                print "Attempting to connect to %s on port %s" % (host, port)
                try:
                        s.connect((host, port))
                        print "Connected to %s on port %s" % (host, port)
                        return True
                except socket.error, e:
                        print "Connection to %s on port %s failed: %s" % (host, port, e)
                        os._exit(1)
                        return False

class Intamixx(ShoutcastClient):
    def gotMetaData(self, data):
        print data[0]
        streamtitle = data[0]
        song = streamtitle [1]
        #print song
        try:
                (artist, title) = song.split(' - ')
        except Exception as e:
                #errno, errstr = error
                print 'An error occurred from song split - Filling in with alternative info ...', e
                artist = song
                title = "Intamixx Live"
        print "Artist is", artist
        print "Title is", title

        fartist = artist.replace(' ', '+')
        ftitle = title.replace(' ', '+')

        url =  "http://air.radiotime.com/Playing.ashx?partnerId={}&partnerKey={}&id={}&artist={}&title={}".format(partnerId, partnerKey, id, fartist, ftitle)

        buf = cStringIO.StringIO()
 
        c = pycurl.Curl()
        c.setopt(c.URL, url)
        c.setopt(c.WRITEFUNCTION, buf.write)
        try:
                c.perform()
        except pycurl.error, error:
                errno, errstr = error
                print 'An error occurred: ', errstr
 
        print buf.getvalue()
        print('Status: %d' % c.getinfo(c.RESPONSE_CODE))
        print('Status: %f' % c.getinfo(c.TOTAL_TIME))
        buf.close()

        os._exit(0)

    def gotMP3Data(self, data):
        pass

def main(argv):
        host = ''
        port = ''
        try:
           opts, args = getopt.getopt(argv,"hs:p:",["server=","port="])
        except getopt.GetoptError:
         print '{} -s <hostname> -p <port>'.format(os.path.basename(__file__))
         sys.exit(2)
        for opt, arg in opts:
         if opt == '-h':
            print '{} -s <hostname> -p <port>'.format(os.path.basename(__file__))
            sys.exit()
         elif opt in ("-s", "--server"):
            host = arg
         elif opt in ("-p", "--port"):
            port = arg
        if not port or not host:
           print '{} -s <hostname> -p <port>'.format(os.path.basename(__file__))
           sys.exit(1)
        else:
           port = int(port)
           check = check_server(host, port)
           protocol.ClientCreator(reactor, Intamixx).connectTCP(host, port)
           reactor.run()
           os._exit(0)

if __name__ == "__main__":
        main(sys.argv[1:])
