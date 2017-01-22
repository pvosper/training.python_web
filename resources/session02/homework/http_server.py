#!/usr/bin/env python3

"""
Homework
    Take the following steps one at a time. Run the tests in
    assignments/session02/homework between to ensure that you are getting it
    right.

    1) Complete the stub resolve_uri function so that it handles looking up
    resources on disk using the URI returned by parse_request.

    2) Make sure that if the URI does not map to a file that exists, it raises
    an appropriate error for our server to handle.

    3) Complete the response_not_found function stub so that it returns a 404
    response.

    4) Update response_ok so that it uses the values returned by resolve_uri by
    the URI. (these have already been added to the function signature)
    You'll plug those values into the response you generate in the way
    required by the protocol

    @maria:

    When starting the homework, start by first getting just this test to pass:
    ```python tests.py ResolveURITestCase.test_directory_resource```

    You might find the test to look confusing at first. It is testing the
    function resolve_uri (the function above this test assigns
    call_function_under_test to this function).

    It is expecting that this function is going to return two objects,

    Look at the test to figure out what these objects should be.
"""

import socket
import sys
import os


def response_ok(body=b"this is a pretty minimal response", mimetype=b"text/plain"):
    """returns a basic HTTP response"""
    resp = []
    resp.append(b"HTTP/1.1 200 OK")
    resp.append(b"Content-Type: text/plain")
    resp.append(b"")
    resp.append(b"this is a pretty minimal response")
    return b"\r\n".join(resp)


def response_method_not_allowed():
    """returns a 405 Method Not Allowed response"""
    resp = []
    resp.append("HTTP/1.1 405 Method Not Allowed")
    resp.append("")
    return "\r\n".join(resp).encode('utf8')


def response_not_found():
    """returns a 404 Not Found response"""
    return b""


def parse_request(request):
    first_line = request.split("\r\n", 1)[0]
    method, uri, protocol = first_line.split()
    if method != "GET":
        raise NotImplementedError("We only accept GET")
    return uri

# It is expecting that this function is going to return two objects,
# Look at the test to figure out what these objects should be.
# 1) Complete the stub resolve_uri function so that it handles looking up
#   resources on disk using the URI returned by parse_request.
# actual_body, actual_mimetype
def resolve_uri(uri):
    """This method should return appropriate content and a mime type"""
    """Your resolve_uri function will need to accomplish the following tasks:

    It should take a URI as the sole argument
    It should map the pathname represented by the URI to a filesystem location.
    It should have a 'home directory', and look only in that location.
    If the URI is a directory, it should return a plain-text listing of the
        directory contents and the mimetype text/plain.
    If the URI is a file, it should return the contents of that file and its
        correct mimetype.
    If the URI does not map to a real location, it should raise an exception
        that the server can catch to return a 404 response.
    """
    content = b""
    if uri[-1] == "/":
        path  = os.getcwd() + '//webroot' + uri
        content = os.listdir(path)
        content = ';'.join(content)
            # .encode('utf-8')
    # with open(filepath) as f:
    #     content = f.readlines()
    # return b"still broken", b"text/plain"
    return content.encode('utf-8'), b"text/plain"


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
                request = ''
                while True:
                    data = conn.recv(1024)
                    request += data.decode('utf8')
                    if len(data) < 1024:
                        break

                try:
                    uri = parse_request(request)
                except NotImplementedError:
                    response = response_method_not_allowed()
                else:
                    try:
                        content, mime_type = resolve_uri(uri)
                    except NameError:
                        response = response_not_found()
                    else:
                        response = response_ok(content, mime_type)

                print('sending response', file=log_buffer)
                conn.sendall(response)
            finally:
                conn.close()

    except KeyboardInterrupt:
        sock.close()
        return


if __name__ == '__main__':
    server()
    sys.exit(0)
