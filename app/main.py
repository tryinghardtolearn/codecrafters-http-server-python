import socket


def main():
    # You can use print statements as follows for debugging, they'll be visible when running tests.
    print("Logs from your program will appear here!")
    
    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)
    conn, addr  = server_socket.accept() # wait for client
    print(f"Connection from address: {addr} has been established.")
    response = "HTTP/1.1 200 OK\r\n\r\n"
    conn.sendall(response.encode('utf-8'))
    conn.close()




if __name__ == "__main__":
    main()