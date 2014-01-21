# coding: utf-8

import mimetypes
import SocketServer
import urllib2
import os.path

# Copyright 2014 Jason Reddekopp
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
#
# Furthermore it is derived from the Python documentation examples thus
# some of the code is Copyright © 2001-2013 Python Software
# Foundation; All Rights Reserved
#
# http://docs.python.org/2/library/socketserver.html
#
# run: python freetests.py

# try: curl -v -X GET http://127.0.0.1:8080/


class MyWebServer(SocketServer.BaseRequestHandler):
    
    def handle(self):
        self.data = self.request.recv(1024).strip()
        
        print ("Got a request of: %s\n" % self.data)
        if self.data.split()[0].__eq__("GET"):
            self.do_get(self.data)            
        self.request.sendall('HTTP/1.1 200 OK\r\n')
        self.request.sendall('Content-Type: text/css\n\n')
        

    def do_get(self, f):
        f = self.send_head(server)
        if f:
            f_data = f.read()
            f.close()
            self.request.sendall(f_data)
 
        
    def send_head(self, server):
        path = os.path.normpath(self.data.split()[1])
        path = urllib2.unquote(path)
        path = "www" + path
        
        print path
        if os.path.isdir(path):
            path = path + "index.html" if str(path).endswith('/') else path + "/index.html" 
        ctype = str(mimetypes.guess_type(path)[0])
        f = None
        try:
            f = open(path, 'rb')
            self.request.sendall('HTTP/1.1 200 OK\r\n')
            self.request.sendall('Content-Type: '+ctype+'\n\n')
        except IOError:
            self.request.sendall('HTTP/1.1 404 FILE NOT FOUND\r\n')
        return f
                
if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    SocketServer.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 9999
    server = SocketServer.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
    
            
    
