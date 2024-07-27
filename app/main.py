import socket


def main():
    # You can use print statements as follows for debugging, they'll be visible when running tests.
    print("Logs from your program will appear here!")
    
    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)
    conn, addr  = server_socket.accept() # wait for client
    print(f"Connection from address: {addr} has been established.")
    response_status_line = "HTTP/1.1 200 OK"
    content_type = "Content-Type: text/plain"
    new_line = "\r\n"

    # parse request data
    request_data = conn.recv(1024).decode('utf-8')
    
    # parse request_line
    request_line = request_data.split(new_line)[0]
    # parse request url
    request_url = request_line.split(" ")[1]
    request_type = request_url.split("/")[1]


    if not request_url.startswith("/") :
        response = ("HTTP/1.1 404 Not Found" + 2*new_line).encode()
    elif request_type == '':
        response = (response_status_line + 2*new_line).encode()
    elif request_type == "echo":
        message_str = request_url.split("/")[-1]
        content_length = f"Content-Length: {len(message_str)}"
        response_body = new_line.join([content_type, content_length])+new_line
        response = new_line.join([response_status_line, response_body, message_str]).encode()
    elif request_type == "user-agent":
        request_header_agent = request_data.split(new_line)[2].split(": ")[1]
        content_length = f"Content-Length: {len(request_header_agent)}"
        response_body = new_line.join([content_type, content_length])+new_line
        response = new_line.join([response_status_line, response_body, request_header_agent]).encode()
    else:
        response = ("HTTP/1.1 404 Not Found" + 2*new_line).encode()
        


    conn.sendall(response)
    conn.close()



if __name__ == "__main__":
    main()