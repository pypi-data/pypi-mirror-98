import zmq
import msgpack
import time

__all__ = ['SourceSubscriber', 'SourcePublisher', 'ServiceConsumer']

class Socket:
    def __init__(self, type_, *, endpoint=None):
        if type_ not in [zmq.SUB, zmq.PUB, zmq.PUSH, zmq.PULL, zmq.REQ, zmq.REP]:
            raise ValueError('Unknown ZeroMQ socket type. Example: `zmq.SUB`')
        self.context = zmq.Context.instance()
        self.socket = self.context.socket(type_)
        if type_ in [zmq.PUB, zmq.PULL, zmq.REP]:
            if endpoint is None:
                self.socket.bind_to_random_port('tcp://127.0.0.1')
            else:
                self.socket.bind(endpoint)
        else:
            if endpoint == None:
                raise ValueError('An endpoint needs to be specified for this socket type.')
            self.socket.connect(endpoint)
        if type_ == zmq.SUB:
            # By default, we subscribe to all topics
            self.socket.setsockopt(zmq.SUBSCRIBE, b'')
    def get_last_endpoint(self):
        return self.socket.get_string(zmq.LAST_ENDPOINT)
    def send(self, data):
        data_msg = msgpack.packb(data)
        self.socket.send(data_msg)
    def receive(self, *, noblock=False):
        flags = zmq.NOBLOCK if noblock else zmq.NULL
        data_msg = self.socket.recv(flags=flags)
        return msgpack.unpackb(data_msg, raw=False)
    def request(self, request):
        self.send(request)
        return self.receive()

def connection(network_string):
    socket = Socket(zmq.SUB, endpoint=network_string)
    return socket.receive()

def request_endpoint(name, req, try_endpoint):
    conn = connection(try_endpoint)
    socket = Socket(zmq.REQ, endpoint=conn['replyEndpoint'])
    return socket.request(req)

def get_endpoint(name, try_endpoint):
    req = {
        'tag': 'get',
        'name': name,
        'endpoint': ''
        }
    return request_endpoint(name, req, try_endpoint)

def get_endpoint_retry(name, try_endpoint):
    while True:
        endpoint = get_endpoint(name, try_endpoint)
        if (not endpoint == ''):
            break
        print(f'Endpoint `{name}` is not available on the network yet. Retrying in 500ms...')
        time.sleep(0.5)
    return endpoint

def add_endpoint(name, endpoint, server_endpoint):
    req = {
        'tag': 'add',
        'name': name,
        'endpoint': endpoint
        }
    return request_endpoint(name, req, server_endpoint)

class SourceSubscriber:
    def __init__(self, name, *, server_address="tcp://127.0.0.1:49152"):
        endpoint = get_endpoint_retry(name, server_address)
        self.socket = Socket(zmq.SUB, endpoint=endpoint)

    def receive(self, *, noblock=False):
        return self.socket.receive(noblock=noblock)

class SourcePublisher:
    def __init__(self, name, *, endpoint=None,
        server_address="tcp://127.0.0.1:49152"):
        self.socket = Socket(zmq.PUB, endpoint=endpoint)
        add_endpoint(name, self.socket.get_last_endpoint(), server_address)

    def publish(self, data):
        self.socket.send(data)

class ServiceConsumer:
    def __init__(self, name, *,
        server_address="tcp://127.0.0.1:49152"):
        endpoint = get_endpoint_retry(name, server_address)
        self.socket = Socket(zmq.REQ, endpoint=endpoint)

    def request(self, request):
        return self.socket.request(request)


