#!/usr/bin/env python3
import socket, sys
from multiprocessing import Process

HOST = ''
PORT = 8001
BUFFER_SIZE = 1024

def main():
    #create socket, bind and set to listening mode
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as proxy_start:
        #allow reuse address
        proxy_start.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        proxy_start.bind((HOST, PORT))
        proxy_start.listen(2)
        
        while True:
            #accept connections and start a Process daemon for handling multiple connections
            conn, addr = proxy_start.accept()
            p = Process(target=handle_echo, args=(addr, conn))
            p.daemon = True
            print("Starting process ", p)
            p.start()
            p.join()
            print("Finished process")

#echo connections back to client
def handle_echo(addr, conn):
    host = 'www.google.com'
    port = 80

    print("Connected by", addr)

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as proxy_end:
        print("Connecting to host {host}")
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

if __name__ == "__main__":
    main()
