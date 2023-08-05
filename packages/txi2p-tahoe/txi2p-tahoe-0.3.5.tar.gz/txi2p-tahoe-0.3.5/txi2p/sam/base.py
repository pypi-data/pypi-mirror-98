# Copyright (c) str4d <str4d@mail.i2p>
# See COPYING for details.

from builtins import str
from builtins import object
import functools
from ometa.grammar import OMeta
from ometa.protocol import ParserProtocol
import re
import time
from twisted.internet import reactor
from twisted.internet.interfaces import IProtocolFactory
from twisted.internet.protocol import ClientFactory
from twisted.python.failure import Failure
from zope.interface import implementer

from txi2p import grammar
from txi2p.address import (
    I2PAddress,
    I2PServerTunnelProtocol,
    I2PTunnelTransport,
)
from txi2p.sam import constants as c

KEEPALIVE_TIMEOUT = 2 * 60


def cmpSAM(a, b):
    def normalize(v):
        return [int(x) for x in re.sub(r'(\.0+)*$','', v).split(".")]
    a_n = normalize(a)
    b_n = normalize(b)
    return (a_n > b_n) - (a_n < b_n)

def peerSAM(data):
    peerInfo = data.decode('utf-8').split('\n')[0].split(' ')
    peerOptions = {x: y for x, y in [x.split('=', 1) for x in peerInfo[1:] if x]}
    fromPort = peerOptions['FROM_PORT'] if 'FROM_PORT' in peerOptions else None
    return I2PAddress(peerInfo[0], port=fromPort)


class SAMParserProtocol(ParserProtocol):
    def __init__(self, *args):
        ParserProtocol.__init__(self, *args)

    def dataReceived(self, data):
        """
        Receive and parse some data.

        :param data: A ``bytes`` from Twisted.
        """

        if self._disconnecting:
            return

        if self.receiver.currentRule == 'State_readData':
            # Shortcut for efficiency
            self.receiver.dataReceived(data)
        else:
            # Duplicated from Parsley because it expects a str but Twisted
            # provides a bytes.
            try:
                self._parser.receive(data.decode('utf-8'))
            except Exception:
                self.connectionLost(Failure())
                self.transport.abortConnection()
                return


def makeSAMProtocol(senderFactory, receiverFactory):
    g = OMeta(grammar.samGrammarSource).parseGrammar('Grammar')
    return functools.partial(
        SAMParserProtocol, g, senderFactory, receiverFactory, {})


class SAMSender(object):
    def __init__(self, transport):
        self.transport = transport

    def sendHello(self):
        self.transport.write(b'HELLO VERSION MIN=3.0 MAX=3.2\n')

    def sendNamingLookup(self, name):
        msg = 'NAMING LOOKUP NAME=%s\n' % name
        self.transport.write(msg.encode('utf-8'))

    def sendPing(self, data):
        if data:
            self.transport.write(('PING %s\n' % data).encode('utf-8'))
        else:
            self.transport.write(b'PING\n')

    def sendPong(self, data):
        if data:
            self.transport.write(('PONG %s\n' % data).encode('utf-8'))
        else:
            self.transport.write(b'PONG\n')


class SAMReceiver(object):
    wrappedProto = None
    currentRule = 'State_hello'
    pinger = None
    lastPing = ''
    pingTimeout = None

    def __init__(self, sender):
        self.sender = sender

    def prepareParsing(self, parser):
        # Store the factory for later use
        self.factory = parser.factory
        self.sender.sendHello()

    def wrapProto(self, proto, peerAddress, invertTLS=False):
        self.wrappedProto = proto
        if hasattr(self.factory, 'localPort'):
            localAddress = I2PAddress(self.factory.session.address,
                                      port=self.factory.localPort)
        else:
            localAddress = self.factory.session.address
        self.transportWrapper = I2PTunnelTransport(
            self.sender.transport,
            localAddress, peerAddress,
            invertTLS)
        proto.makeConnection(self.transportWrapper)

    def dataReceived(self, data):
        self.wrappedProto.dataReceived(data)

    def finishParsing(self, reason):
        if self.wrappedProto:
            self.wrappedProto.connectionLost(reason)
        else:
            self.factory.connectionFailed(reason)
        if hasattr(self.factory, 'session'):
            self.factory.session.removeStream(self)

    def hello(self, result, version=None, message=None):
        if result != c.RESULT_OK:
            self.factory.resultNotOK(result, message)
            return
        self.factory.samVersion = version
        self.command()

    def lookupReply(self, result, name, value=None, message=None):
        if result != c.RESULT_OK:
            self.factory.resultNotOK(result, message)
            return
        self.postLookup(value)

    def _sendPing(self):
        self.lastPing = str(time.time())
        self.sender.sendPing(self.lastPing)
        self.pingTimeout = reactor.callLater(KEEPALIVE_TIMEOUT, self.sender.transport.loseConnection)

    def _resetPingTimeout(self):
        if self.pingTimeout:
            self.pingTimeout.cancel()
        self.pinger = reactor.callLater(KEEPALIVE_TIMEOUT, self._sendPing)

    def ping(self, data):
        self.sender.sendPong(data)
        self._resetPingTimeout()

    def pong(self, data):
        if (data == str(self.lastPing)):
            self._resetPingTimeout()

    def startPinging(self):
        self.pinger = reactor.callLater(KEEPALIVE_TIMEOUT, self._sendPing)
        self.currentRule = 'State_keepalive'

    def stopPinging(self):
        if self.pinger and self.pinger.active():
            self.pinger.cancel()
        if self.pingTimeout and self.pingTimeout.active():
            self.pingTimeout.cancel()

class SAMFactory(ClientFactory):
    currentCandidate = None
    canceled = False

    def _cancel(self, d):
        self.currentCandidate.sender.transport.abortConnection()
        self.canceled = True

    def buildProtocol(self, addr):
        proto = self.protocol()
        proto.factory = self
        self.currentCandidate = proto
        return proto

    def connectionFailed(self, reason):
        if not self.canceled and not self.deferred.called:
            self.deferred.errback(reason)

    # This method is not called if an endpoint deferred errbacks
    def clientConnectionFailed(self, connector, reason):
        self.connectionFailed(reason)

    def resultNotOK(self, result, message):
        raise c.samErrorMap.get(result)(string=(message if message else result))


class SAMI2PServerTunnelProtocol(I2PServerTunnelProtocol):
    def setPeer(self, data):
        self.peer = peerSAM(data)
        self.transport.peerAddr = self.peer


@implementer(IProtocolFactory)
class I2PFactoryWrapper(object):
    protocol = SAMI2PServerTunnelProtocol

    def __init__(self, wrappedFactory, serverAddr):
        self.w = wrappedFactory
        self.serverAddr = serverAddr

    def buildProtocol(self, addr):
        wrappedProto = self.w.buildProtocol(addr)
        proto = self.protocol(wrappedProto, self.serverAddr)
        proto.factory = self
        return proto

    def __getattr__(self, attr):
        return getattr(self.w, attr)
