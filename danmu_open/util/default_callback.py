from util.dependency import *

def create_callback(msgtype,file):
    uset=set()
    count=0
    def onChatmsg(msg,config=None):
        nonlocal uset
        nonlocal file
        nonlocal count
        count+=1
        ts=time.localtime(time.time())
        ts=time.strftime('%H:%M:%S',ts)
        line="%s\t(lv%02d)\t%s\t%s"%(ts,int(msg['level']),msg['nn'],msg['txt'])     #Why some char cannot be decoded?
        if not msg['nn'] in uset:
            uset.add(msg['nn'])
        line+="\t(%d/%d)"%(len(uset),count)
        if config['verbose']:
            print(line)
        else:
            return(len(uset),count,'barrages')
            # sys.stdout.write("\rCollected %d/%d barrages in Room:%s"%(len(uset),count,config['rid']))
        file.write(line+'\n')
        file.flush()
    def onReward(msg,config=None):
        pass
    def onGift(msg,config=None):
        # print("gift!!!!!!!!!!!!!!!!!!")
        nonlocal uset
        nonlocal file
        nonlocal count
        count+=1
        ts=time.localtime(time.time())
        ts=time.strftime('%H:%M:%S',ts)
        try:
            gcnt='1' if (not 'gfcnt' in msg or msg['gfcnt']=='') else msg['gfcnt']
            line="%s\t(lv%02d)\t%s\t%s\t%s\t\t\t%s"%(ts,int(msg['level']),msg['nn'],msg['gfid'],gcnt,msg['dw'])     #Why some char cannot be decoded?
            if not msg['nn'] in uset:
                uset.add(msg['nn'])
            line+="\t(%d/%d)"%(len(uset),count)
            if config['verbose']:
                print(line)
            else:
                return (len(uset),count,'gifts')
                # sys.stdout.write("\rCollected %d/%d gifts in Room:%s"%(len(uset),count,config['rid']))
        except:
            count-=1
        file.write(line+'\n')
        file.flush()

    def onUenter(msg,config=None):
        pass
    def onBcBuy(msg,config=None):
        pass
    if msgtype=='chatmsg':
        return onChatmsg
    elif msgtype=='onlinereward':
        return onReward
    elif msgtype=='dgb':
        return onGift
    elif msgtype=='uenter':
        return onUenter
    elif msgtype=='bc_buy_deserve':
        return onBcBuy