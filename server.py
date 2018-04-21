import sys
import socket
from time import sleep

host, port = sys.argv[1], int(sys.argv[2])

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((host, port))
s.listen(1)
while True:
    print('\nListening for a client at',host , port)
    conn, addr = s.accept()
    print('\nConnected by', addr)
    try:
        print('\nReading file...\n')
        with open('data/testing.csv') as f:
            f.readline()
            for line in f:
                out = line.encode('utf-8')
                print('Sending line',line.strip())
                conn.send(out)
                sleep(2)
            print('End Of Stream.')
    except socket.error:
        print ('Error Occured.\n\nClient disconnected.\n')
conn.close()
