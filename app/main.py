import socket


def main():
    # You can use print statements as follows for debugging, they'll be visible when running tests.
    print("Logs from your program will appear here!")
    
    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)
    conn, addr  = server_socket.accept() # wait for client
    print(f"Connection from address: {addr} has been established.")
    response_status_line = "HTTP/1.1 200 OK"

    request_data = conn.recv(1024).decode('utf-8')
    request_line = request_data.split("\r\n")[0]
    request_url = request_line.split(" ")[1]
    request_type = request_url.split("/")[1]
    message_str = request_url.split("/")[-1]
    print("message_str",message_str)

    content_type = "Content-Type: text/plain"
    content_length = f"Content-Length: {len(message_str)}"
    new_line = "\r\n"

    if not request_url.startswith("/") :
        response = ("HTTP/1.1 404 Not Found" + 2*new_line).encode()
    elif request_type == '':
        response = (response_status_line + 2*new_line).encode()
    elif request_type == "echo":
        response_body = new_line.join([content_type, content_length])+new_line
        response = new_line.join([response_status_line, response_body, message_str]).encode()
    else:
        response = ("HTTP/1.1 404 Not Found" + 2*new_line).encode()
        


    conn.sendall(response)
    conn.close()



if __name__ == "__main__":
    main()