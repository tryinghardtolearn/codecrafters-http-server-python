import socket


def main():
    # You can use print statements as follows for debugging, they'll be visible when running tests.
    print("Logs from your program will appear here!")
    
    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)
    conn, addr  = server_socket.accept() # wait for client
    print(f"Connection from address: {addr} has been established.")
    response = b"HTTP/1.1 200 OK\r\n\r\n"

    request_data = conn.recv(1024).decode('utf-8')
    request_line = request_data.split("\r\n")[0]
    if request_line.split(" ")[1] != '/':
        response = b"HTTP/1.1 404 Not Found\r\n\r\n"

    conn.sendall(response)
    conn.close()



if __name__ == "__main__":
    main()