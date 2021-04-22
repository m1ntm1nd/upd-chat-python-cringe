import socket
import threading
import queue
import sys
import random
import os
import logging
import time
import csv


from settings import PORT,BUFFERSIZE,ENCODING


BufferSize=BUFFERSIZE
encoding=ENCODING
port=PORT

class Server():
    def __init__(self, logger, host, socket):
        self.port = port
        self.log = logger
        self.host = host
        self.socket = socket

    def RunServer(self):         
        clients = set()
        recvPackets = queue.Queue()

        threading.Thread(target=RecvData,args=(self.socket,recvPackets)).start()

        while True:
            while not recvPackets.empty():
                data,addr = recvPackets.get()
                if addr not in clients:
                    clients.add(addr)
                    with open('list.csv', 'w', newline='') as file: #список клиентов
                        csv.writer(file).writerow(clients)
                    continue
                clients.add(addr)
                itsatime = time.strftime("%Y-%m-%d-%H.%M.%S", time.localtime())
                data = data.decode(encoding) 
                data=exchange(data)  #вызов фильтра 
                if data.endswith('exit'):
                    clients.remove(addr)
                    continue
                print('['+str(addr[0])+']'+'='+'['+str(addr[1])+']'+'='+'['+itsatime+']'+'/'+data)
                for c in clients:  #клиент не получает свои сообщения
                    if c!=addr:
                        self.socket.sendto(data.encode(encoding),c)


def create_logger():
    logger=logging.getLogger('main')   #логирование
    formatter = logging.Formatter(
        '%(asctime)s - %(levelname)s - %(message)s'
    )
    handler=logging.FileHandler('info.log',encoding=ENCODING)
    handler.setLevel(logging.DEBUG)
    handler.setFormatter(formatter)    
    logger.setLevel(logging.DEBUG)
    logger.addHandler(handler)

    return logger

def create_server(logger):
    host = socket.gethostbyname(socket.gethostname())

    print('='*53)
    print('*'*18+'Server Running'+'*'*21)
    print('='*53)

    print('Server hosting on IP -> ['+str(host)+'] Port -> ['+str(port)+']')    
    print('='*53)
    s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    s.bind((host,port))
    return (host, s)

def exchange(data):   #фильтр слов 
    data=data.replace('cringe','maybe cring')
    data=data.replace('Cringe','maybe cring')
    return data

def RecvData(sock,recvPackets):
    while True:
        data,addr = sock.recvfrom(1024)
        recvPackets.put((data,addr))


def main():
    logger = create_logger()
    srv = create_server(logger)
    server = Server(logger, srv[0], srv[1])
    try:
        server.RunServer()
    except:
    # logger.info('Server closed')
        print('Server closed')

if __name__ == "__main__":
    main()