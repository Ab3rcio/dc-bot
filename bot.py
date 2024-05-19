#!/usr/bin/env python3

import requests, random, sys, yaml, time

print("Youtube Channerl : TRENDING BOS \nsubscribe - like - comment - share \n Happy for Use :\n\n") 
	
class Discord:
	
    def __init__(self, t):
        self.base = "https://discord.com/api/v9"
        self.auth = { 'authorization': t }
        
    def getMe(self):
        u = requests.get(self.base + "/users/@me", headers=self.auth).json()
        return u
        
    def getMessage(self, cid, l):
        u = requests.get(self.base + "/channels/" + str(cid) + "/messages?limit=" + str(l), headers=self.auth).json()
        return u
        
    def sendMessage(self, cid, txt):    
        u = requests.post(self.base + "/channels/" + str(cid) + "/messages", headers=self.auth, json={ 'content': txt }).json()
        return u

    def replyMessage(self, cid, mid, txt):    
        u = requests.post(self.base + "/channels/" + str(cid) + "/messages", headers=self.auth, json={ 'content': txt, 'message_reference': { 'message_id': str(mid) } }).json()
        return u

    def deleteMessage(self, cid, mid):
        u = requests.delete(self.base + "/channels/" + str(cid) + "/messages/" + str(mid), headers=self.auth)
        return u

def quote():
    u = requests.get("https://gist.githubusercontent.com/camperbot/5a022b72e96c4c9585c32bf6a75f62d9/raw/e3c6895ce42069f0ee7e991229064f167fe8ccdc/quotes.json").json()
    return random.choice(list(u))['quote']

def simsimi(lc, txt):
    u = requests.post("https://api.simsimi.info/v1/simtalk", data={ 'lc': lc, 'text': txt}).json()
    return u['message']

def main():
    with open('config.yaml') as cfg:
        conf = yaml.load(cfg, Loader=yaml.FullLoader)

    if not conf['BOT_TOKEN']:
        print("Edit Dulu token akun dc di config.yaml!")
        sys.exit()

    if not conf['CHANNEL_ID']:
        print("Edit dulu channel id di diconfig.yaml!")
        sys.exit()

    mode = conf['MODE']
    simi_lc = conf['SIMSIMI_LANG']
    delay = conf['DELAY']
    del_after = conf['DEL_AFTER']
    repost_last = conf['REPOST_LAST_CHAT']
                
    if not mode: 
        mode = "quote"
        
    if not simi_lc:
        simi_lc = "id"
        
    if not repost_last: 
        repost_last = "100"
    
    while True:
        for token in conf['BOT_TOKEN']:
            try:

                for chan in conf['CHANNEL_ID']:

                    Bot = Discord(token)
                    me = Bot.getMe()['username'] + "#" + Bot.getMe()['discriminator']
                    
                    if mode == "quote":
                        q = quote()
                        send = Bot.sendMessage(chan, q)
                        print("[{}][{}][QUOTE] {}".format(me, chan, q))                
                        if del_after:
                            Bot.deleteMessage(chan, send['id'])
                            print("[{}][DELETE] {}".format(me, send['id']))

                    elif mode == "repost":
                        res = Bot.getMessage(chan, repost_last)
                        getlast = list(reversed(res))[0]                    
                        send = Bot.sendMessage(chan, getlast['content'])
                        print("[{}][{}][REPOST] {}".format(me, chan, getlast['content']))
                        if del_after:
                            Bot.deleteMessage(chan, send['id'])
                            print("[{}][DELETE] {}".format(me, send['id']))
                        
                    elif mode == "simsimi":
                        res = Bot.getMessage(chan, "1")
                        getlast = list(reversed(res))[0]                
                        simi = simsimi(simi_lc, getlast['content'])

                        if conf['REPLY']:
                            send = Bot.replyMessage(chan, getlast['id'], simi)
                            print("[{}][{}][SIMSIMI] {}".format(me, chan, simi))
                        else:
                            send = Bot.sendMessage(chan, simi)
                            print("[{}][{}][SIMSIMI] {}".format(me, chan, simi))

                        if del_after:
                            Bot.deleteMessage(chan, send['id'])
                            print("[{}][DELETE] {}".format(me, send['id']))
            except:
                print(f"[Error] {token} : Token Salah Bos!")
        
        print("\n*****Tunggu {} detik***** \n".format(delay))
        time.sleep(delay)
        print ("Sukses | Jangan lupa Subscribe YT Trending Bos \n")

if __name__ == '__main__':
    try:
        main()
    except Exception as err:
        print(f"{type(err).__name__} : {err}")
        