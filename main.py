import socket
import _thread


def main():
    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)
    while True:
        client_socket, client_address = server_socket.accept()
        _thread.start_new_thread(respond,(client_socket,))
    server_socket.close()

def respond(client_socket): 
    request = client_socket.recv(1024)
    path = request.split()[1]
    if path == b"/":
        response = b"HTTP/1.1 200 OK\r\n\r\n"
    elif path.startswith(b"/echo"):
        echo_str = path.split(b"/echo/")[1]
        response = b"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length:%d\r\n\r\n%s" % (len(echo_str), echo_str)
    elif path == b"/user-agent":
        user_agent = request.split(b"User-Agent: ")[1].split(b"\r\n")[0]
        response = b"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length:%d\r\n\r\n%s" % (len(user_agent), user_agent)
    else:
        response= b"HTTP/1.1 404 Not Found\r\n\r\n"
    client_socket.send(response)
    client_socket.close()

if __name__ == "__main__":
    main()
