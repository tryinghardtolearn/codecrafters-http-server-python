import socket
import threading
import argparse
import os

content_type_fmt = "Content-Type: {}"
content_length_fmt = "Content-Length: {}"
new_line = "\r\n"

def response_status_line(res_code=200):
    if res_code == 200:
        return "HTTP/1.1 200 OK"
    elif res_code == 404:
        return "HTTP/1.1 404 Not Found"
    elif res_code == 201:
        return "HTTP/1.1 201 Created"
    else:
        raise ValueError(f"{res_code} isn't handled.")
    
def simple_response(res_code):
    return (response_status_line(res_code)+2*new_line).encode()

def full_response(response_body, content_type="text/plain", res_code=200):
    c_type = content_type_fmt.format(content_type)
    c_len = content_length_fmt.format(len(response_body))
    response_header = new_line.join([c_type, c_len])+new_line
    return new_line.join([response_status_line(res_code), response_header, response_body]).encode()

def return_file_content(filepath):
    if not os.path.isfile(filepath):
        return simple_response(404)
    
    with open(filepath, "r") as f:
        data = f.read()
        return full_response(data, content_type="application/octet-stream")

def modify_file_content(filepath, data):
    with open(filepath, "x") as f:
        f.write(data)
        return simple_response(201)


def parse_request(conn):
    # parse arguments
    parser   = argparse.ArgumentParser("parser")
    parser.add_argument("--directory", type=str)
    args = parser.parse_args()
    dir = args.directory

    # parse request data
    request_data = conn.recv(1024).decode('utf-8')
    
    # parse request_line
    request_line = request_data.split(new_line)[0]
    request_type = request_line.split(" ")[0]
    # parse request url
    request_url = request_line.split(" ")[1]
    request_action = request_url.split("/")[1]

    # parse request_body
    request_body = request_data.split(new_line)[-1]


    print(f"request_type is {request_type}, request_action is {request_action}, request_url is {request_url}")
    if not request_url.startswith("/") :
        response = simple_response(404)
    elif request_action == '':
        response = simple_response(200)
    elif request_action == "echo":
        message_str = request_url.split("/")[-1]
        response = full_response(message_str)
    elif request_action == "user-agent":
        request_header_agent = request_data.split(new_line)[2].split(": ")[1]
        response = full_response(request_header_agent)
    elif request_action == "files":
        filename = request_url.split("/")[-1]
        filepath = f"/{dir}/{filename}"
        if request_type == "GET":
            response = return_file_content(filepath)
        elif request_type == "POST":
            data = request_body
            response = modify_file_content(filepath, data)
    else:
        response = simple_response(404)
    
    print("response is ", response)
    conn.sendall(response)
    conn.close()

def main():
    # You can use print statements as follows for debugging, they'll be visible when running tests.
    print("Logs from your program will appear here!")

    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)
    while True:
        conn, addr  = server_socket.accept() # wait for client
        print(f"Connection from address: {addr} has been established.")
 
        threading.Thread(target=parse_request, args=(conn,)).start()


if __name__ == "__main__":
    main()