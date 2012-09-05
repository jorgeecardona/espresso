import argparse
from uuid import uuid4
import zmq.green as zmq

from gevent import Greenlet
from gevent.queue import Queue


class Consumer(Greenlet):
    """
    Consumer
    ========

    This class will be connected to all the neighbors and will consume
    any message sent from them.

    """

    def __init__(self, address):
        super(Consumer, self).__init__()

        # Create context, socket and connect to address.
        context = zmq.Context()
        self.socket = context.socket(zmq.SUB)
        self.address = address

        # We need someone to process messages.
        self.processor = MessageProcessor()
        self.processor.start()

    def bind(self):
        " Bind socket to address. "

        print "Start listing in address %s ..." % (self.address, )
        self.socket.bind(self.address)

    def subscribe(self, topic):
        " Subscribe to some topic."

        print "Subscribe to topic %s" % (topic, )
        self.socket.setsockopt(zmq.SUBSCRIBE, topic)

    def _run(self):

        # Bind zmq socket.
        self.bind()
        self.subscribe('')

        for i in xrange(10):

            # Put the messages in the inbox.
            self.processor.put(self.socket.recv_json())

        # Stop processor.
        self.processor.running = False
        self.processor.join()


class MessageProcessor(Greenlet):
    """
    Message processor
    =================

    This class will process the messsage and react.

    """

    def __init__(self):
        Greenlet.__init__(self)

        self.running = True

        # Inbox queue.
        self.inbox = Queue()

    def _run(self):

        while self.running:

            # Receive message.
            self.process(self.inbox.get())

    def put(self, message):
        self.inbox.put(message)

    def process(self, message):
        " Process a single message."

        print message


class Daemon(object):

    def __init__(self):

        # We choose a random id.
        self.id = str(uuid4())




class RouteManager(object):
    """
    Route Manager
    =============

    Found a route to a particular peer using tags.

    """

    routes = {}




class PeerManager(object):
    """
    Peer Manager
    ============

    This class is intended to Keep track of peers.

    First we are going to keep a simple list of all the server seen and we
    going to replicate this info using some gossip protocol.

    http://graphics.stanford.edu/courses/cs428-03-spring/Papers/readings/Networking/Hass_gossip_routing_infocom02.pdf


    Roadmap
    -------

    It seems that the first step is to use flooding, then some gossip.

    There are some nice papers about routing in DHT, maybe some ideas can be used
    in here:

    1. SecureRoutingDHT: A Protocol for Reliable Routing in P2P DHT-based Systems:
    http://www.thinkmind.org/download.php?articleid=iciw_2012_9_10_20227

    """

    peers = {}

    @classmethod
    def __init__(cls, seed={}):
        cls.peers.update(seed)

    @classmethod
    def add(cls, peer):
        cls.peers.update(peer)

    @classmethod
    def flood(cls, messenger):
        " Send the local set of peers to the rest."

        for peer in cls.peers:

            # Send a messages to.
            messenger.send({'peers': {}}, to=peer.address)


class QueueManager(object):
    " Manager of the queues of the system. "



class MessageManager(object):
    " Manager for all the incoming messages. "

    def __init__(self, address='tcp://localhost:4128'):

        # We choose a random id.
        self.id = str(uuid4())

        # Create the peers manager.
        self.peers = PeerManager({self.id: address})

        # Store address.
        self.address = address

        # Get zmq context.
        self.context = zmq.Context()

        # Create socket.
        self.socket = self.context.socket(zmq.REP)
        self.socket.bind(self.address)

        print "Start listening in " + self.address

        # Start polling on this.
        self.poll = zmq.Poller()
        self.poll.register(self.socket, zmq.POLLIN)

    def send(self, to, data):
        " Send a message to other."

        socket = self.context.socket(zmq.REQ)

    def loop(self):

        while True:

            sockets = dict(self.poll.poll(1000))

            if self.socket in sockets:

                if sockets[self.socket] == zmq.POLLIN:

                    try:
                        self.process_message(self.socket.recv_json())
                    finally:
                        self.socket.send_json({'result': 'ok'})

    def process_message(self, message):
        " Process any arriving message."

        # We need at least two items:
        if not isinstance(message, dict):
            return

        if 'espresso' not in message:
            return

        if 'command' in message['espresso']:

            if message['espresso']['command'] == 'list-peers':

                print "List peers" + str(self.peers.peers)

            if message['espresso']['command'] == 'join':
                # Join to system.
                pass

# Peers in the system.
peers = {}

def espresso():

    parser = argparse.ArgumentParser(description="Espresso daemon.")

    # Set the address to start listening for messages.
    parser.add_argument(
        '--address', dest='address', default='127.0.0.1:8888',
        help='Address to listen, default: 127.0.0.1:8888')

    # Plugins to load.
    parser.add_argument('--plugins', dest='plugins', help='Plugins to load.')

    # Parse arguments
    args = parser.parse_args()

    # Consumer.
    consumer = Consumer(address='tcp://%s' % (args.address, ))
    consumer.start()
    consumer.join()



    # Create message manager.
    #manager = MessageManager(
    #    address='tcp://%s' % (args.address, ))

    # Start the loop.
    #manager.loop()
