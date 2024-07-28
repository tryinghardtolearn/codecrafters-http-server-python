import socket
import threading
import argparse
import os

content_type_fmt = "Content-Type: {}"
content_length_fmt = "Content-Length: {}"
content_encoding_fmt = "Content-Encoding: {}"
new_line = "\r\n"
accepted_compression = ['gzip']

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

def compress(body, encoding=None):
    if not encoding:
        return body
    else:
        return body

def full_response(response_body:str, content_type:str="text/plain", res_code: int=200, compression_encoding:str|None=None):
    c_type = content_type_fmt.format(content_type)
    c_len = content_length_fmt.format(len(response_body))
    response_header = new_line.join([c_type, c_len])+new_line

    if compression_encoding and compression_encoding in accepted_compression:
        c_encode = content_encoding_fmt.format(compression_encoding)
        compressed_body = compress(response_body, compression_encoding)
        c_len = content_length_fmt.format(len(compressed_body))
        response_header = new_line.join([c_type, c_encode, c_len])+new_line

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
    request_line = request_data.split(new_line)[0]
    # request_host = request_data.split(new_line)[1]

    # Parse headers
    headers = {}
    for header in request_data.split(new_line)[2:-1]:
        print("Parsing header: ", header)
        if not header:
            continue
        header_key, header_value = header.split(": ") 
        headers[header_key] = header_value
        

    request_body = request_data.split(new_line)[-1]

    
    # parse request_line
    request_type = request_line.split(" ")[0]
    request_url = request_line.split(" ")[1]

    # parse request url
    request_action = request_url.split("/")[1]

    # parse request_body


    print(f"request_type is {request_type}, request_action is {request_action}, request_url is {request_url}")
    if not request_url.startswith("/") :
        response = simple_response(404)
    elif request_action == '':
        response = simple_response(200)
    elif request_action == "echo":
        message_str = request_url.split("/")[-1]
        encoding = headers.setdefault('Accept-Encoding', None)
        response = full_response(message_str,compression_encoding=encoding)
    elif request_action == "user-agent":
        user_agent=headers.setdefault('User-Agent', '')
        response = full_response(user_agent)
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