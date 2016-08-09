from util.dependency import *

def escape(self,string):
    string.replace('@','@A')
    string.replace('/','@S')
    return string

def rev_escape(self,string):
    string.replace('@S','/')
    string.replace('@A','@')
    return string

def create_record(fname,delimiter='\\'):
    dirs=fname.split(delimiter)
    if dirs[0][-1]==':':
        os.chdir(dirs[0]+'\\')
        dirs.pop(0)
    for d in dirs[:-1]:
        try:
            os.chdir(d)
        except FileNotFoundError:
            os.mkdir(d)
            os.chdir(d)
    return open(dirs[-1],'w+')

def keepalive_func(danmu_crawler):
    while 1:
        danmu_crawler.keepalive()
        time.sleep(KEEPALIVE_INTERVAL)

class NameException(Exception):
    def __init__(self):
        self.value='Need either rid or anc_name'
    def __str__(self):
        return self.value

class IllegalFomat(Exception):
    def __init__(self,value=None):
        self.value='IllegalFomat:' if type(value)!=str and type(value)!=bytes else 'IllegalFomat:\n%s'%value
    def __str__(self):
        return self.value