import argparse
import zmq
from uuid import uuid4


def barista():
    " Espresso CLI."

    parser = argparse.ArgumentParser(description="Brew some coffee")

    # Seed for the system.
    parser.add_argument(
        '--seed', dest='seed', help='Seed peer to connect.', default='127.0.0.1:8888')

    # List the peers connected.
    parser.add_argument('--list-peers', dest='list_peers', help='List the peers in the system.', action='store_true', default=False)

    # Parse arguments
    args = parser.parse_args()

    if args.list_peers:

        # Random id.
        id = str(uuid4())

        # We need to connect to some peer and ask this.
        context = zmq.Context()

        # Connecting to peer.
        socket = context.socket(zmq.PUB)
        socket.connect('tcp://' + args.seed)

        # Send request.
        socket.send_json({'espresso': {'command': 'list-peers', 'sender': id}})

