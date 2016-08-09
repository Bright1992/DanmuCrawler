# -*- coding: utf8 -*-

from util.util import *
from util.message import *
from util.default_callback import *

#config{
#     'rid':
#     'dir':
#     'verbose':
# }


class danmu_crawler:
    def __init__(self,config=None):
        if config is None:
            print("config must not be None!",file=sys.stderr)
        directory=config['dir']
        rid=self.rid=config['rid']
        self.config=config
        ts=time.strftime('%m-%d-%H-%M-%S',time.localtime(time.time()))
        
        # print(os.listdir())
        self.file_dict={'chatmsg':create_record(directory+'\\chatmsg_%s_%s.txt'%(rid,ts))}
        self.type_dict={'chatmsg':create_callback('chatmsg',self.file_dict['chatmsg'])}
        self.summery={'chatmsg':(0,0,'barrage')}

        # print(os.listdir())
        self.file_dict['dgb']=create_record('dgb_%s_%s.txt'%(rid,ts))   #No 'directory' ahead, because in case of relative path, create_record will recursively mkdir(directory)
        self.type_dict['dgb']=create_callback('dgb',self.file_dict['dgb'])
        self.summery['dgb']=(0,0,'gift')

        self.conn=socket.socket()
        self.lock=threading.Lock()

    def clear_default_callback(self):
        self.type_dict={}

    def set_callback(self,msgtype,func):
        self.type_dict[msgtype]=func

    def connect(self,terminate,max_count=20):
        print("Connecting...")
        self.conn.connect((host,port))
        print("Connected to %s:%d"%(host,port))
        content=RequestMessage('loginreq',rid=self.rid)
        message=content.get_raw()
        self.conn.settimeout(20)
        try:
            self.conn.sendall(message)
            print("Login request has been sent")
            rec=self.conn.recv(4096)
            # rm=ResponseMessage(rec)
            # kvpl=rm.get_kvpairs()
            content=RequestMessage('joingroup',rid=self.rid)
            message=content.get_raw()
            self.conn.sendall(message)
            print("Join group Request has been sent")
            rec=self.conn.recv(4096)
            # rm=ResponseMessage(rec)
            # kvp2=rm.get_kvpairs()
        except socket.timeout:
            print("Request timeout",file=sys.stderr)
            return -1
        self.conn.settimeout(5)
        keepalive_thread=threading.Thread(target=keepalive_func,args={self},daemon=True)
        keepalive_thread.start()
        count=0
        while not terminate[0]:
            if count>max_count:
                print('Server not answering, quit.')
                #Terminate keepalive thread
                return -1
            self.lock.acquire()
            try:
                rec=self.conn.recv(4096)
            except socket.timeout:
                count+=1
                continue
            finally:
                self.lock.release()
            count=0
            try:
                rm=ResponseMessage(rec)
                msgs=rm.get_kvpairs()
            except Exception as e:
                print("Exception Happened:%s"%str(e))
                continue
            for msg in msgs:
                try:
                    if msg['type'] in self.type_dict:
                        ret=self.type_dict[msg['type']](msg,self.config)
                        if not self.config['verbose']:
                            self.summery[msg['type']]=ret
                            sys.stdout.write('\rCollected ')
                            c=0
                            # print(len(self.summery))
                            for s in self.summery:
                                sys.stdout.write('(%d/%d) %s'%(self.summery[s][0],self.summery[s][1],self.summery[s][2]))
                                if c<len(self.summery)-1:
                                    sys.stdout.write(', ')
                                c+=1
                            sys.stdout.write(' in room:%s'%self.rid)
                except Exception as e:
                    print("Something wrong happened:%s"%str(e))
        for f in self.file_dict:
            self.file_dict[f].close()

    def keepalive(self):
        content=RequestMessage('keepalive')
        message=content.get_raw()
        self.lock.acquire()
        try:
            self.conn.sendall(message)
        finally:
            self.lock.release()

