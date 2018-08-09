import socket
import os
import time
import datetime
import threading
from threading import Thread

class Cache:
    def __init__(self):
        self.cache_lifetime = {}
        self.cache_last_three = ["f1","f2","f3"]
        self.f1 = open("file1","rw")
        self.f2 = open("file2","rw")
        self.f3 = open("file3","rw")
        self.f1.close()
        self.f2.close()
        self.f3.close()

    def check_exists(self,file_name):
        for key, values in self.cache_lifetime.iteritems():
            if file_name in values:
                return True
        return False

    def store_val(self,file_name,mod_time):
        fp = self.get_file_no()
        if fp in self.cache_lifetime:
            del self.cache_lifetime[fp]
        self.cache_lifetime[fp] = {file_name:mod_time}
        return fp

    def get_file_var(self,fileN):
        for key, values in self.cache_lifetime.iteritems():
            if fileN in values:
                return key
        return False

    def get_file_no(self):
        f_no = self.cache_last_three.pop(0)
        self.cache_last_three.append(f_no)
        return f_no

    def get_map(self,fp):
        if(fp == "f1"):
            return "file1"
        elif(fp == "f2"):
            return "file2"
        elif(fp == "f3"):
            return "file3"

    def get_time(self,filename):
        temp = self.get_file_var(filename)
        for key,values in self.cache_lifetime.iteritems():
            if key == temp:
                for k,v in values.iteritems():
                    return v

web_cache = Cache()
flag_file_mod = 0;


port = 12345
host = ""

print 'Server listening....'

while True:

    #Socket for the Client side connection
    s = socket.socket()
    s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
    s.bind((host, port))
    s.listen(1)
    #Socket for the server connection
    s2 = socket.socket()
    s2.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
    s2.connect((host, 20000))

    conn, addr = s.accept()
    print 'Got connection from', addr
    Temp = conn.recv(1024)

    if(Temp != ''):
        no = Temp.find('http://localhost:20000')
        Temp = Temp.replace('http://localhost:20000','')
        filename = Temp[no+1:no+20].partition(" HTTP/1.1")[0]
        bufferN = ""

        if(not web_cache.check_exists(filename)):
            time_pokemon = time.time()
            loc = Temp.find("If-Modified-Since: ")
            if loc != -1:
                loc2 = Temp.find("GMT")
                Temp = Temp[:loc] + Temp[loc2+5:]
            s2.send(Temp)
            print Temp
            while True:
                Recv = s2.recv(1024)
                if(Recv !=''):
                    bufferN = bufferN + Recv
                if not Recv:
                    break
            print "BUFFER N : " + bufferN + " </>"
            file_p = web_cache.store_val(filename,time_pokemon)
            cache_file = open(web_cache.get_map(file_p),"w+")
            cache_file.write(bufferN)
            cache_file.close()
            cache_file = open(web_cache.get_map(file_p),"r")
            lines = cache_file.readlines()
            print web_cache.get_map(file_p)
            print lines
            cache_file.close()
        else:
            print "In Buffer"
            loc = Temp.find("If-Modified-Since: ")
            time_pokemon = web_cache.get_time(filename)
            if loc != -1:
                loc2 = Temp.find("GMT")
                Temp = Temp[:loc] + Temp[loc2+5:]
            Temp = Temp.replace("\r\n\r\n","\r\n")
            Temp += "If-Modified-Since: " + str(datetime.datetime.fromtimestamp(int(time_pokemon)).strftime("%a %b  %d %H:%M:%S %Y"))
            Temp += "\r\n\r\n"
            s2.send(Temp)
            flag_file_mod = 1
            while True:
                Recv = s2.recv(1024)
                if not Recv:
                    break
                if(Recv.find('304 Not Modified')!= -1):
                    flag_file_mod = 0
                    break
                elif(Recv.find('200 OK') != -1):
                    bufferN = bufferN + Recv

            print "Modified: " + str(flag_file_mod)

            if (not flag_file_mod):
                f_name = web_cache.get_file_var(filename)
                if(f_name):
                    f_po = web_cache.get_map(f_name)
                    f_pointer = open(f_po,"rw+")
                    while True:
                        Recv = f_pointer.read(1024)
                        if(Recv !=''):
                            bufferN = bufferN + Recv
                        if not Recv:
                            break
                else:
                    print "404"
            elif (flag_file_mod):
                time_pokemon = time.time()
                file_p = web_cache.store_val(filename,time_pokemon)
                cache_file = open(web_cache.get_map(file_p),"w+")
                cache_file.write(bufferN)
                cache_file.close()
                cache_file = open(web_cache.get_map(file_p),"r")
                lines = cache_file.readlines()
                cache_file.close()

        conn.send(bufferN)
        conn.close()
        s.close()
        s2.close()
print('Done sending')
