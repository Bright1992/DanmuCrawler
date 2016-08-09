#!/usr/bin/python3

import sys
import re

sys.path.append('./danmu_open')
from danmu_open.danmu_open import *

def new_crawler(terminate,config):
    p=danmu_crawler(config=config)
    p.connect(terminate)

# import util.getch

terminate=[False]
import tkinter

class outlet(tkinter.Frame):
    def __init__(self,master=None):
        super().__init__(master)
        self.pack()
        self.create_widgets()
        self.master=master
    def create_widgets(self):
        self.btn=tkinter.Button(self,text="QUIT",fg='red',command=self.quit_func)
        self.btn.pack()
    def quit_func(self):
        global terminate
        terminate[0]=True
        self.master.destroy()    


def test():
    help="""format:
    danmu_crawler <rid> [-v] [-d <default directory>]"""
    crawl_threads={}
    global ternimate
    # terminate=[False]
    argc=len(sys.argv)
    if argc==1:
        print(help)
        sys.exit()
    verbose=True if '-v' in sys.argv else False
    if argc==0 or ('-d' in sys.argv and argc==sys.argv.index('-d')+1):
        print(help)
        sys.exit()
    directory='./danmu_crawler' if not '-d' in sys.argv else sys.argv[sys.argv.index('-d')+1]
    rid=sys.argv[1]
    if not re.search(r"\D",rid) is None:
        print(help)
        sys.exit()
    config={
    'dir':directory,
    'verbose':verbose,
    'rid':rid
    }
    crawl_threads[rid]=threading.Thread(target=new_crawler,args=[terminate,config])
    crawl_threads[rid].start()
    # for ct in crawl_threads:
    #     crawl_threads[ct].join()


    root = tkinter.Tk()
    tk=outlet(root)
    tk.mainloop()
    print("end")

    
if __name__=='__main__':
    test()
