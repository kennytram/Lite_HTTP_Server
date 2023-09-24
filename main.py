import socket
import _thread
import sys
from pathlib import Path


def main():
    server_socket = socket.create_server(("localhost", 8080), reuse_port=True)
    
    while True:
        client_socket, client_address = server_socket.accept()
        _thread.start_new_thread(respond,(client_socket,))
    server_socket.close()

def respond(client_socket): 
    request = client_socket.recv(1024)
    http_method = request.split()[0]
    path = request.split()[1]
    command_line_args = sys.argv
    match http_method: 
        case b"GET":
            if path == b"/":
                response = b"HTTP/1.1 200 OK\r\n\r\n"
            elif path.startswith(b"/echo"):
                echo_bytes = path.split(b"/echo/")[1]
                response = b"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length:%d\r\n\r\n%s" % (len(echo_bytes), echo_bytes)
            elif path.startswith(b"/files"):
                directory = command_line_args[-1]
                path_str = path.split(b"/files/")[1].decode("utf-8")
                file_path = directory + path_str
                if Path(file_path).exists():
                    with open(file_path, "rb") as f:
                        file_content = f.read()
                    response = b"HTTP/1.1 200 OK\r\nContent-Type: application/octet-stream\r\nContent-Length:%d\r\n\r\n%s" % (len(file_content), file_content)
                else:
                    response = b"HTTP/1.1 404 Not Found\r\n\r\n"

            elif path == b"/user-agent":
                user_agent = request.split(b"User-Agent: ")[1].split(b"\r\n")[0]
                response = b"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length:%d\r\n\r\n%s" % (len(user_agent), user_agent)
            else:
                response= b"HTTP/1.1 404 Not Found\r\n\r\n"
        case b"POST":
            if path.startswith(b"/files"):
                directory = command_line_args[-1]
                path_str = path.split(b"/files/")[1].decode("utf-8")
                file_path = directory + path_str
                file_content = request.split(b"\r\n\r\n")[1]
                with open(file_path, "wb") as f:
                    f.write(file_content)
                response = b"HTTP/1.1 201 OK\r\n\r\n"
            else:
                response = b"HTTP/1.1 404 Not Found\r\n\r\n"
    client_socket.send(response)
    client_socket.close()

if __name__ == "__main__":
    main()
