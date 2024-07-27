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
    else:
        raise ValueError(f"{res_code} isn't handled.")
    
def simple_response(res_code):
    return (response_status_line(res_code)+2*new_line).encode()

def full_response(response_body, content_type="text/plain", res_code=200):
    c_type = content_type_fmt.format(content_type)
    c_len = content_length_fmt.format(len(response_body))
    response_header = new_line.join([c_type, c_len])+new_line
    return new_line.join([response_status_line(res_code), response_header, response_body]).encode()

def return_file_content(filename):
    parser = argparse.ArgumentParser("parser")
    parser.add_argument("--directory", type=str)
    args = parser.parse_args()
    dir = args.directory
    filepath = f"/{dir}/{filename}"

    if not os.path.isfile(filepath):
        return simple_response(404)
    
    with open(filepath, "r") as f:
        data = f.read()
        return full_response(data, content_type="application/octet-stream")

def parse_request(conn):
    # parse request data
    request_data = conn.recv(1024).decode('utf-8')
    
    # parse request_line
    request_line = request_data.split(new_line)[0]
    # parse request url
    request_url = request_line.split(" ")[1]
    request_type = request_url.split("/")[1]


    if not request_url.startswith("/") :
        response = simple_response(404)
    elif request_type == '':
        response = simple_response(200)
    elif request_type == "echo":
        message_str = request_url.split("/")[-1]
        response = full_response(message_str)
    elif request_type == "user-agent":
        request_header_agent = request_data.split(new_line)[2].split(": ")[1]
        response = full_response(request_header_agent)
    elif request_type == "files":
        filename = request_url.split("/")[-1]
        response = return_file_content(filename)
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