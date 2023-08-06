#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import socket
import json
import os 
import threading
import psutil
import logging
import signal


logging.basicConfig(level=os.environ.get("LOGLEVEL", "INFO"),
                    format='%(asctime)s - [%(process)d] %(levelname)s : %(message)s'
                    #filename='app.log', filemode='w', 
                    )
logger = logging.getLogger()



logger.info("START")

MAXLENGTH = 1024*1024*1024
DATAS = {}
UDS = "/tmp/varsity.uds"

if os.path.exists(UDS): os.remove(UDS)    

# HOST = '0.0.0.0'
# PORT = 24680
# s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
# s.bind((HOST, PORT))
#################################################
s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
s.bind(UDS)

def okmg(v) :
    if v < 1024 : 
        return str(v) + " oct"
    elif v < 1024 * 1024 : 
        return str(round(v / 1024 , 2)) + " ko"
    elif v < 1024 * 1024 *1024: 
        return str(round(v / (1024 * 1024) , 2)) + " Mo"
    else : 
        return str(round(v / (1024 * 1024 * 1024) , 2)) + " Go"

def vc_drop_db(client, db) :
    del DATAS[db]
    return True

def vc_get_memory(client, db) :
    process = psutil.Process(os.getpid())
    byte = process.memory_info().rss
    return okmg(byte)

def vc_var_count(client, db) :
    return len(DATAS[db].keys())

def vc_var_list(client, db) :
    return list(DATAS[db].keys())

class ClientThread(threading.Thread):

    def __init__(self, clientsocket):
        threading.Thread.__init__(self)
        self.client = clientsocket
        
        self.database = self.client.recv(64).strip().decode('utf-8')
        if self.database not in DATAS :
            DATAS[self.database] = {}
            
        logger.info("[+] %s connected to %s" % (self.name, self.database) )

    def run(self): 

        while True :
            buffer = self.client.recv(MAXLENGTH)
            if not buffer : break

            try :
                cmd = json.loads(buffer)

                for db, data in cmd.items() :
                    if db not in DATAS :
                        DATAS[db] = {}
               
                # READ
                if type(data) == str :
                    resp = DATAS[db].get(data, None)

                # WRITE / DELETE
                elif len(data) == 2 :
                    if data[1] is None :
                        if data[0] in DATAS.keys() : 
                            del DATAS[db][data[0]]    
                    else : 
                        DATAS[db][data[0]] = data[1]
                    resp = True

                # RETURN FUNCTION RESULT
                else :
                    fct = data[0]
                    args = [self.client] + data[2:]
                    resp = globals()[fct](*args)
                        
                self.client.sendall(json.dumps(resp).encode('utf-8'))
            except Exception as e :
                self.client.sendall("ERROR : {0}".format(e).encode('utf-8'))
        
        logger.info("[-] %s closed" % self.name)


if __name__ == '__main__':
    try:
        while True:
            s.listen(2)
            client, tmp = s.accept()

            logger.info(threading.active_count())

            th =  ClientThread(client)
            th.daemon = True
            th.start()
            
    except KeyboardInterrupt:
        pass

    if os.path.exists(UDS): os.remove(UDS)    

    #with open('persist.srv', 'w') as fp : json.dump(DATAS, fp)