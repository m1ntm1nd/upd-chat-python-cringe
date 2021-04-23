import socket
import threading
import queue
import sys
import random
import os
import logging as log
import time
import csv

import settings



class Server():
    def __init__(self):             #creating server w/ defaults 
        self.port = settings.PORT
        self.host = socket.gethostbyname(socket.gethostname())
        self.socket = self.create_server()

    def create_server(self):
        s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        s.bind((self.host,self.port))

        Server.print_info('*'*18+'Server Running'+'*'*21)   
        Server.print_info('Server hosting on IP -> ['+str(self.host)+'] Port -> ['+str(self.port)+']')

        return s

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
                data = data.decode(settings.ENCODING) 
                data=exchange(data)  #вызов фильтра 
                if data.endswith('exit'):
                    clients.remove(addr)
                    continue
                print('['+str(addr[0])+']'+'='+'['+str(addr[1])+']'+'='+'['+itsatime+']'+'/'+data)
                for c in clients:  #клиент не получает свои сообщения
                    if c!=addr:
                        self.socket.sendto(data.encode(settings.ENCODING),c)

    def print_info(string):
        delim = '='*53
        print(delim)
        print(string)
        print(delim)



def exchange(data):   #фильтр слов 
    data=data.replace('cringe','maybe cring')
    data=data.replace('Cringe','maybe cring')
    return data

def RecvData(sock,recvPackets):
    while True:
        data,addr = sock.recvfrom(1024)
        recvPackets.put((data,addr))


def main():
    log.basicConfig(
        format='[ %(levelname)s ] %(message)s',
        level=log.INFO,
        filename='info.log'
    )

    server = Server()
    try:
        server.RunServer()
    except:
        print('Server closed')


if __name__ == "__main__":
    main()