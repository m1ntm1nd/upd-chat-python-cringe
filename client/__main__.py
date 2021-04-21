import socket
import threading
import queue
import sys
import random
import os
import time


from settings import ENCODING,BUFFERSIZE
# from actions import Slash as sl


# logger=logging.getLogger('main')

# formatter = logging.Formatter(
#     '%(asctime)s - %(levelname)s - %()s'
# )

# handler=logging.FileHandler('info.log',encoding=ENCODING)
# handler.setFormatter(formatter) 
# handler.setLevel(logging.DEBUG)

# logger.setLevel(logging.DEBUG)
# logger.addHandler(handler)


try:
    def ReceiveData(sock,recvPackets):
        while True:
            try:
                #
                data,addr = sock.recvfrom(BufferSize)
                data=data.decode(encoding)
                itsatime = time.strftime("%Y-%m-%d-%H.%M.%S", time.localtime())
                print('['+str(addr[0])+']'+'='+'['+str(addr[1])+']'+'='+'['+itsatime+']'+'/'+data)
            except:
                pass

    def connect(serverIP,port):
        print('Now server IP = ',serverIP)
        print('Your port = ',port)
        serverIP=input('Enter new serverIP: ')
        port=int(input('Enter new port: '))
        RunClient(serverIP,port)

    def rename(name):
        name=input("Enter new name: ")
        return name            

    def RunClient(serverIP,port):
        BufferSize=BUFFERSIZE
        encoding=ENCODING
        host = socket.gethostbyname(socket.gethostname())
        # if not port:
        #     port = random.randint(6000,10000)
        # logger.info('Client IP->'+str(host)+' Port->'+str(port))
        print(('Client IP -> '+str(host)+' Port -> '+str(port)))
        server = (str(serverIP),8000)
        s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        s.bind((host,port))
        s.setblocking(0)

        join=False

        name = input('Please write your name here: ')
        if name == '':
            name = 'Guest'+str(random.randint(1000,9999))
            #logger.info('Your name is:'+name) 
            print('Your name is:'+name)
        s.sendto(name.encode(encoding),server)

        recvPackets = queue.Queue()
        threading.Thread(target=ReceiveData,args=(s,recvPackets)).start()

        while True:
            if join == False:
                data='['+ name + '] -> join chat'
                s.sendto(data.encode(encoding),server)
                join=True
            data = input()
            if data == 'exit':
                break
            elif data=='':
                continue
            elif data[0]=='/':
                if data=='/rename':
                    old_name=name
                    name=rename(name)
                    data= '['+old_name+']' + ' -> ' + 'change name'+' on ' + '['+name+']'
                    s.sendto(data.encode(encoding),server)
                elif data=='/connect':
                    data='['+name+']' + ' <- ' + 'left the chat' 
                    s.sendto(data.encode(encoding),server)
                    connect(serverIP,port)
            data = '['+name+']' + ' -> '+ data
            s.sendto(data.encode(encoding),server)
        data='['+name+']' + ' <- ' + 'left the chat' 
        s.sendto(data.encode(encoding),server)
        s.close()
        os._exit(1)
except:
    # logger.info('Client closed')
    print('Client closed')
    
# if len(sys.argv)==2:
RunClient(sys.argv[1],int(sys.argv[2]))
# else:
#   RunClient(sys.argv[1])