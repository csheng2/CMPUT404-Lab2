#!/usr/bin/env python3
import socket, sys

#define address & buffer size
HOST = ''
PORT = 8001
BUFFER_SIZE = 1024

#get host information
def get_remote_ip(host):
    print(f'Getting IP for {host}')
    try:
        remote_ip = socket.gethostbyname(host)
    except socket.gaierror:
        print ('Hostname could not be resolved. Exiting')
        sys.exit()

    print (f'Ip address of {host} is {remote_ip}')
    return remote_ip

def main():
    # Question 6, connect to google
    host = 'www.google.com'
    port = 80

    # server part
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as proxy_start:
        #allow reuse address, bind, and set to listening mode
        proxy_start.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        proxy_start.bind((HOST, PORT))
        proxy_start.listen(1)
        
        while True:
            #connect proxy_start
            conn, addr = proxy_start.accept()
            print("Connected by", addr)

            # act as client
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as proxy_end:
                print("Connecting to Google")
                remote_ip = get_remote_ip(host)

                # create proxy_end connection
                proxy_end.connect((remote_ip , port))

                # send data
                send_full_data = conn.recv(BUFFER_SIZE)
                print(f"Sending received data {send_full_data} to google")
                proxy_end.sendall(send_full_data)

                proxy_end.shutdown(socket.SHUT_WR)

                data = proxy_end.recv(BUFFER_SIZE)
                print(f"Sending received data {data} to client")

                conn.send(data)
            
            conn.close()

if __name__ == "__main__":
    main()
