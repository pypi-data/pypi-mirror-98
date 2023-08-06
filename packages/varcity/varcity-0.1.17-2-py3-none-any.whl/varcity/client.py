#!/usr/bin/env python3

import socket
import json

# HOST = '127.0.0.1'
# PORT = 24680
# s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# s.connect((HOST, PORT))

class VarcityClient():

    def __init__(self,buffer_size = 1024 * 1024 * 1024, database = "default", uds = "/tmp/varsity.uds"):
        self.MAXLENGTH = buffer_size
        self.database = database
        self.socket = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        self.socket.connect(uds)
        self.socket.sendall(self.database.encode('utf-8').ljust(64))

    def close(self, ):
        self.socket.close()
        pass

    def get(self, name): 
        self.socket.sendall(json.dumps({self.database: name}).encode('utf-8'))
        return json.loads(self.socket.recv(self.MAXLENGTH))

    def set(self, name, value): 
        self.socket.sendall(json.dumps({self.database : [name, value]}).encode('utf-8'))
        return json.loads(self.socket.recv(self.MAXLENGTH))

    def vc_drop_db(self,):
        return self.get(['vc_drop_db', None, self.database])

    def vc_get_memory(self,):
        return self.get(['vc_get_memory', None, self.database])

    def vc_var_count(self,):
        return self.get(['vc_var_count', None, self.database])

    def vc_var_list(self,):
        return self.get(['vc_var_list', None, self.database])

    
