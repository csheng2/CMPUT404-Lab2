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
            p.start()
            print("Starting process ", p)

            handle_echo(addr, conn)

            print("Finished process ", p)

#echo connections back to client
def handle_echo(addr, conn):
    print("Connected by", addr)

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as proxy_end:
        # send data
        send_full_data = conn.recv(BUFFER_SIZE)
        print(f"Sending received data {send_full_data} to google")
        proxy_end.sendall(send_full_data)

        proxy_end.shutdown(socket.SHUT_RDWR)

        data = proxy_end.recv(BUFFER_SIZE)
        print(f"Sending received data {data} to client")

        conn.send(data)
    conn.close()

if __name__ == "__main__":
    main()
