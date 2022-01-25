#  coding: utf-8 
import socketserver, os
import pdb



# Copyright 2013 Abram Hindle, Eddie Antonio Santos
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


G_DIRECTORY_ROOT = "www"#content directory


class MyWebServer(socketserver.BaseRequestHandler):
    
    def handle(self):
        self.data = self.request.recv(1024).strip()

        dataLines = self.data.decode("utf-8").split("\n")#get each line of request
        #deal with first line of header
        requestTypeName = dataLines[0].split(' ')[0]
        requestDirectory = dataLines[0].split(' ')[1]

        if requestTypeName == "GET":
            if os.path.isfile(G_DIRECTORY_ROOT + requestDirectory):
                pass
            else:#Directory doesn't exist
                self.request.sendall(bytearray("HTTP/1.1 404 Not Found\r\n",'utf-8'))
        else:#Request isn't get
            self.request.sendall(bytearray("HTTP/1.1 405 Method Not Allowed\r\n",'utf-8'))

        print("RequestType: {}\nRequestDir: {}\ndata: {}".format(requestTypeName, requestDirectory,dataLines))
        print("exists?: {}", os.path.isfile(G_DIRECTORY_ROOT + requestDirectory))
        #self.request.sendall(bytearray("OK",'utf-8'))
        #self.request.sendall(bytearray("HTTP/1.1 200 OK\r\n", 'utf-8'))




if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    socketserver.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = socketserver.TCPServer((HOST, PORT), MyWebServer)
    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
