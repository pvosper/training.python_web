import socket
import sys


def server(log_buffer=sys.stderr):
    address = ('127.0.0.1', 10000)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    print("making a server on {0}:{1}".format(*address), file=log_buffer)
    sock.bind(address)
    sock.listen(1)

    try:
        while True:
            print('waiting for a connection', file=log_buffer)
            conn, addr = sock.accept()  # blocking
            try:
                print('connection - {0}:{1}'.format(*addr), file=log_buffer)
                request = ""
                while True:
                    data = conn.recv(1024)
                    request += data.decode('utf8')
                    if len(data) < 1024:
                        break
                print('sending response', file=log_buffer)
                response = response_ok()
                conn.sendall(response)
            finally:
                conn.close()

    except KeyboardInterrupt:
        sock.close()
        return


def response_ok():
    """this function returns the simple http response"""

    resp = []
    resp.append(b"HTTP/1.1 200 OK")
    resp.append(b"Content-Type: text/plain")
    resp.append(b"")
    resp.append(b"this is a pretty minimal response")

    return b"\r\n".join(resp)


def parse_request(request):
    first_line = request.split("\r\n")[0]
    method, uri, protocol = first_line.split()
    if method != "GET":
        raise NotImplementedError("We only accept GET")
    print('request is okay', file=sys.stderr)


def response_method_not_allowed():
    """returns a 405 Method Not Allowed response"""
    resp = []
    resp.append(b"HTTP/1.1 405 Method Not Allowed")
    resp.append(b"")
    return b"\r\n".join(resp)


if __name__ == '__main__':
    server()
    sys.exit(0)
