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


try:

    # def change_port(port):
    #     print('Now u have ',port,' port')
    #     port=int(input('Enter new port: '))
    #     RunServer(port)

    def exchange(data):   #фильтр слов 
        data=data.replace('cringe','maybe cring')
        data=data.replace('Cringe','maybe cring')
        return data

    def RecvData(sock,recvPackets):
        while True:
            data,addr = sock.recvfrom(1024)
            recvPackets.put((data,addr))

    def RunServer(port):
        logger=logging.getLogger('main')   #логирование
        formatter = logging.Formatter(
            '%(asctime)s - %(levelname)s - %(message)s'
        )

        handler=logging.FileHandler('info.log',encoding=ENCODING)
        handler.setLevel(logging.DEBUG)
        handler.setFormatter(formatter)
        
        logger.setLevel(logging.DEBUG)
        logger.addHandler(handler)

        host = socket.gethostbyname(socket.gethostname())

        print('='*53)
        print('*'*18+'Server Running'+'*'*21)
        print('='*53)
        logger.info(f'Server hosting on IP -> '+str(host)+' Port -> '+str(port))
        print('Server hosting on IP -> ['+str(host)+'] Port -> ['+str(port)+']')
        print('='*53)
        s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        s.bind((host,port))
        clients = set()
        recvPackets = queue.Queue()

        threading.Thread(target=RecvData,args=(s,recvPackets)).start()

        # join_name,addr=s.recvfrom(1024)
        # recvPackets.put((join_name,addr))
        # join_name,addr = recvPackets.get()
        # join_name=join_name.decode(encoding)
        # print(join_name)
        # join_name,addr = recvPackets.get()
        # join_name=join_name.decode(encoding)
        # print(join_name)

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
                        s.sendto(data.encode(encoding),c)

                #Попытка организовать ввод команд для сервера
                # command=input()
                # if not command:
                #     continue
                # elif command=='/change port':
                #     data='Server change port = ',port
                #     client=(str(addr[0]),addr[1])
                #     s.sendto(data.ecnode(encoding),client)
                #     change_port(port)
                # elif command=='/remove client':
                #     with open('list.csv', 'w', newline='') as file:
                #         file.open()
                # elif command=='/stop':
                #     break
                # if command=='/change port':
                #     change_port(port)
                # elif command=='/remove client':
                #     with open('list.csv', 'w', newline='') as file:
                #         file.open()
                # elif command=='/stop':
                #     break
        print('Server closed')
        s.close()
        os._exit(1)
except:
    # logger.info('Server closed')
    print('Server closed')

RunServer(port)