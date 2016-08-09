from util.dependency import *

class RequestMessage:
    def __init__(self,type,**kw):
        self.string=''
        self.message=b''
        if type=='loginreq':
            if not 'rid' in kw:
                raise IllegalFomat
                #return -1
            self.rid=kw['rid']
            self.string="type@=%s/roomid@=%s/"%(type,self.rid)
            self.message=self.to_raw(self.string)

        elif type=='keepalive':
            ts=int(time.time())
            self.string="type@=%s/tick@=%d/"%(type,ts)
            self.message=self.to_raw(self.string)
        elif type=='joingroup':
            if not 'rid' in kw:
                raise IllegalFomat
                #return -1
            self.gid=-9999 if not 'gid' in kw else kw['gid'] 
            self.string="type@=%s/rid@=%s/gid@=%s"%(type,kw['rid'],self.gid)
            self.message=self.to_raw(self.string)
        elif type=='logout':
            self.string="type@=logout/"
            self.message=self.to_raw(self.string)
        else:
            raise IllegalFomat
            #return -1

    def to_raw(self,string):
        length=len(string)+1+8
        message=struct.pack("<LLHH%dsB"%len(string),length,length,MAGICNUM_TO_SERVER,0,string.encode(),0)
        return message

    def get_raw(self):
        return self.message

    def get_text(self):
        return self.string




class ResponseMessage:
    def __init__(self,raw_byte):
        length=-4
        self.kv_pair_set=list()
        while length+4<len(raw_byte):
            try:
                raw_byte=raw_byte[length+4:]
                length=raw_byte[0:4]
                length=(length[0])|(length[1]<<8)|(length[2]<<16)|(length[3]<<24)
                mgkn=raw_byte[8]+(raw_byte[9]<<8)
                if mgkn==MAGICNUM_FROM_SERVER:
                    try:
                        self.raw_string=raw_byte[12:4+length].decode()
                    except Exception as e:
                        print(e)
                        print(raw_byte)
                    kv_pairs={}
                    kvs=self.raw_string.split('/')
                    for kv in kvs:
                        if kv.find('@=')!=-1:
                            #print(kv)
                            kvp=kv.split('@=')
                            kv_pairs[kvp[0]]=kvp[1]
                    self.kv_pair_set.append(kv_pairs)
            except Exception as e:
                print('Exception Happened:%s'%str(e))
                continue
            else:
                #raise IllegalFomat(raw_byte[12:12+length])
                pass

    def get_kvpairs(self):
        return self.kv_pair_set