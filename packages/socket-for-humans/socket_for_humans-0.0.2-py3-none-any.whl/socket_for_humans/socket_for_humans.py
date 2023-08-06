import socket
import inspect
import time


BLOCK_SIZE = 4
DEBUG = False


class Connection:

    def __init__(self, addr, timeout=20, block_size=BLOCK_SIZE, str_mode=True, msg=None, conn=None):
        self.addr = addr
        self.timeout = timeout
        self.block_size = block_size
        self.str_mode = str_mode

        if conn is None:
            printif('{}. Client connecting to: "{}"'.format(_lnum(), self.addr))
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.connect(self.addr)
            self.sock.settimeout(self.timeout)
            self.sock.setblocking(False)

            printif('{}. Client connected to: "{}". timeout = {}s. block_size = {}b'.format(
                _lnum(), self.addr, self.timeout, self.block_size))
        else:
            self.sock = conn

        if msg:
            self.send(msg)

    def __del__(self):
        self.sock.close()

    def close(self):
        self.sock.close()

    def send(self, msg):
        """
        fcn to handle client requests.
        used when query makes request to node and also when node makes request to another node
        """

        printif('{}. Client sending: "{}"'.format(_lnum(), msg))
        if self.str_mode:
            self.sock.sendall(msg.encode('utf-8'))
        else:
            self.sock.sendall(msg)

    def send_and_recv(self, msg):

        self.send(msg)
        return self.recv()

    def recv(self):
        return _recv(self.sock, timeout=self.timeout, str_mode=self.str_mode, block_size=self.block_size)


class Server:

    def __init__(self, addr, timeout=20, block_size=BLOCK_SIZE, str_mode=True):
        self.addr = addr
        self.timeout = timeout
        self.block_size = block_size
        self.str_mode = str_mode

        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.settimeout(self.timeout)
        self.server.bind(self.addr)
        self.server.listen()
        printif('{}. Server started, listening on {}'.format(_lnum(), self.addr))

    def __del__(self):
        self.server.close()

    def get_next(self, echo_back=False, close_immediately=False):
        t0 = time.time()
        try:
            self.server.listen()
            conn, addr = self.server.accept()
            conn.setblocking(False)
            data = _recv(conn)
            # Wrap the conn object return ed by accept() in our client object so user code can use send() recv()
            # functions without worrying about blocking/timeouts/block_size etc...
            conn = Connection(addr=addr, conn=conn)
        except socket.timeout as st:
            data = None
            conn = None
            addr = None

        if echo_back and conn is not None:
            conn.send(data)
        if close_immediately and conn is not None:
            conn.close()
            conn = None

        return data, conn, addr


def _recv(sock, block_size=BLOCK_SIZE, str_mode=True, timeout=20):
    t0 = time.time()
    data = ""
    data_started = False
    data_finished = False
    while not data_finished:
        try:
            d = sock.recv(block_size)
            if d:
                data_started = True
                if str_mode:
                    data += d.decode('UTF-8')
                else:
                    data += d
                t0 = time.time()
                # print("{}. Received: {}. data = '{}'".format(lnum(), d, data), flush=True)
            elif data_started:
                data_finished = True
                printif('{}. Received: "{}"'.format(_lnum(), data), flush=True)
            if time.time() - t0 > timeout:
                data_finished = True
                printif(_lnum() + '. Timeout.')
        except BlockingIOError as err:
            printif('BlockingIOError')
            if data_started:
                data_finished = True
    printif('{}. Received: "{}"'.format(_lnum(), data))
    return data


def _lnum():
    """Returns the current line number in our program."""
    return str(inspect.currentframe().f_back.f_lineno)


def printif(s, **kwargs):
    if DEBUG:
        print(s, kwargs)


if __name__ == "__main__":

    import random

    print("test 1")
    test_addr = ('127.0.0.1', 12345)
    test_server = Server(addr=test_addr)
    test_client = Connection(addr=test_addr)
    test_msg = "the quick brown fox jumps over the lazy dog"
    test_client.send(test_msg)
    recv_msg, server_conn, _ = test_server.get_next(echo_back=True)
    reply = test_client.recv()
    assert test_msg == recv_msg, "recv_msg not same as test_msg"
    assert test_msg == reply, "reply not same as test_msg"

    print("test 2")
    # continue to use conn for multiple messages...
    test_msg2 = "life ain't always empty"
    test_client.send(test_msg2)
    recv_msg2 = server_conn.recv()
    server_conn.send(recv_msg2)
    reply2 = test_client.recv()
    assert test_msg2 == recv_msg2, "recv_msg2 not same as test_msg2"
    assert test_msg2 == reply2, "reply2 not same as test_msg2"

    print("test 3")
    test_addr = ('127.0.0.1', 12346)  # different port
    test_server = Server(addr=test_addr)
    test_client = Connection(addr=test_addr)
    test_msg = "how many roads must a man walk down"
    test_client.send(test_msg)
    time.sleep(max(0.5, random.gauss(1.0, 1.0)))
    recv_msg, server_conn, _ = test_server.get_next(echo_back=True)
    time.sleep(max(0.5, random.gauss(1.0, 1.0)))
    reply = test_client.recv()
    assert test_msg == recv_msg, "recv_msg not same as test_msg"
    assert test_msg == reply, "reply not same as test_msg"

    print("test 4")
    # continue to use server_conn for multiple messages...
    test_msg2 = "If you want an other kind of lover, I'll wear a mask for you"
    time.sleep(max(0.5, random.gauss(1.0, 1.0)))
    test_client.send(test_msg2)
    time.sleep(max(0.5, random.gauss(1.0, 1.0)))
    recv_msg2 = server_conn.recv()
    time.sleep(max(0.5, random.gauss(1.0, 1.0)))
    server_conn.send(recv_msg2)
    time.sleep(max(0.5, random.gauss(1.0, 1.0)))
    reply2 = test_client.recv()
    time.sleep(max(0.5, random.gauss(1.0, 1.0)))
    assert test_msg2 == recv_msg2, "recv_msg2 not same as test_msg2"
    assert test_msg2 == reply2, "reply2 not same as test_msg2"
