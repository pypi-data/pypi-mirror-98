import socket
import inspect
import time


BLOCK_SIZE = 4
DEBUG = False


class Connection:

    def __init__(self, addr, timeout=20, block_size=BLOCK_SIZE, str_mode=True, msg=None, conn=None):
        """
        Connection object to handle both sides of a socket communication
        To initiate a 2-way socket communication (i.e. act as a client) use this class to send a message to an address
        e.g.
        my_conn = Connection(address)
        my_conn.send("initial message in communications")
        reply = my_conn.recv()

        See also Server object. The server object returns a Connection instance once a connection is initiated by a
        client. Thereafter both sides of the communications are using the Connection object to alternatively send and
        recieve messages.

        Note: The Server and the Connection objects must have same setting for 'str_mode' you can't mix and match.

        :param addr:        address to connect to. A tuple with ipv4 address and port number, like ("127.0.0.1, 12345)
        :param timeout:     optional. default is 20 seconds. specify integer seconds.
        :param block_size:  optional. default is 1024 bytes. specify integer value, usually 2**n.
        :param str_mode:    optional. default is True. set to False if you want to send binary data instead of strings.
        :param msg:         optional. default is None. If supplied then .send() is called to send the message
        :param conn:        optional. default is None. Ready made connection to adopt. Dragons be here.
        """

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
            self.sock.settimeout(self.timeout)
            self.sock.setblocking(False)

        if msg:
            self.send(msg)

    def __del__(self):
        self.close()

    def close(self):
        """
        Closes the connection
        """
        self.sock.close()

    def send(self, msg):
        """
        send data over the connection

        :param msg: the data to send. Type should be either 'str' or 'bytes' consistent with 'str_mode' setting.
        """

        printif('{}. Client sending: "{}"'.format(_lnum(), msg))
        if self.str_mode:
            self.sock.sendall(msg.encode('utf-8'))
        else:
            self.sock.sendall(msg)

    def send_and_recv(self, msg):
        """
        Send a message and wait for a reply and return the reply. If a timeout occurs an empty reply is returned.

        :param msg:  the data to send. Type should be either 'str' or 'bytes' consistent with 'str_mode' setting.
        :return:     the reply. Type will be either 'str' or 'bytes' consistent with 'str_mode' setting.
        """
        self.send(msg)
        return self.recv()

    def recv(self):
        """
        receive data if available. If a timeout occurs an empty reply is returned

        :return:     the reply. Type will be either 'str' or 'bytes' consistent with 'str_mode' setting.
        """
        return _recv(self.sock, timeout=self.timeout, str_mode=self.str_mode, block_size=self.block_size)


class Server:

    def __init__(self, addr, timeout=20, block_size=BLOCK_SIZE, str_mode=True):
        """
        Server class to handle passive waiting for connections.

        To passively wait for clients to initiate a 2-way socket communication (i.e. act as a server) use this class to
        regularly check for new connections. When a new connection is made a Connection object is returned so that
        thereafter 2-way communications on the TCP/IP socket are handles by the Connection objects at both ends.
        e.g.
        my_serv = Server(address)
        while True:
            msg, conn, addr = my_serv.get_next()
            conn.send("my reply to msg")

        See also Connection class.

        Note: The Server and the Connection objects must have same setting for 'str_mode' you can't mix and match.

        :param addr:        address to listen to. A tuple with ipv4 address and port number, like ("127.0.0.1, 12345)
        :param timeout:     optional. default is 20 seconds. specify integer seconds.
        :param block_size:  optional. default is 1024 bytes. specify integer value, usually 2**n.
        :param str_mode:    optional. default is True. set to False if you want to send binary data instead of strings.
        """

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
        """
        Method to check for incoming connections from clients. Essential passive Server functionality. Returns the
        message recieved, a Connection object and the address of the client.

        :param echo_back:          optional. default=False. Set to True to immediately echo message back to the client
        :param close_immediately:  optional. default=False. Set to True if your application is 1-way communications
        :return: msg, conn, addr   return type is a list. First list element is the message sent by the client, second
                                   list element is a Connection object for continued 2-way communications with the
                                   client, third list element is the address of the client.
        """
        t0 = time.time()
        try:
            self.server.listen()
            conn, addr = self.server.accept()
            conn.setblocking(False)
            data = _recv(conn, self.str_mode, block_size=self.block_size, timeout=self.timeout)
            # Wrap the conn object return ed by accept() in our client object so user code can use send() recv()
            # functions without worrying about blocking/timeouts/block_size etc...
            conn = Connection(addr=addr, conn=conn,
                              str_mode=self.str_mode, block_size=self.block_size, timeout=self.timeout)
        except socket.timeout as st:
            if self.str_mode:
                data = ""
            else:
                data = b''
            conn = None
            addr = None

        if echo_back and conn is not None:
            conn.send(data)
        if close_immediately and conn is not None:
            conn.close()
            conn = None

        return data, conn, addr


def _recv(sock, str_mode, block_size=BLOCK_SIZE, timeout=20):
    """
    Internal utility code for socket_for_humans module. You don't normally need to use this.
    Instead see Connection.recv() and Server.get_next()

    :param sock:        The socket to use
    :param str_mode:    True = output data is 'str' type. False = output data is 'bytes' type
    :param block_size:  optional. size of data blocks to read from buffer
    :param timeout:     optional. timeout in seconds
    :return:            data received from buffer. Type will be consistent with 'str_mode' setting.
    """
    t0 = time.time()
    if str_mode:
        data = ""
    else:
        data = b''
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
    """Returns the current line number in our program. used for debugging"""
    return str(inspect.currentframe().f_back.f_lineno)


def printif(s, **kwargs):
    """
    Conditional print function for simple debugging verbosity control
    :param s:
    :param kwargs:
    """
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
