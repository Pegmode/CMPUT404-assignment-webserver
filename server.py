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


#GlobalDefines
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
                self.parseAndHandleFile(requestDirectory)

            elif os.path.isfile(G_DIRECTORY_ROOT + requestDirectory + "index.html"):
                self.parseAndHandleFile(requestDirectory+ "index.html")

            else:#Directory doesn't exist
                self.request.sendall(bytearray("HTTP/1.1 404 Not Found\r\n",'utf-8'))
                #print("Got a request for file that doesn't exist")

        else:#Request isn't get
            self.request.sendall(bytearray("HTTP/1.1 405 Method Not Allowed\r\n",'utf-8'))
            #print("Got an unsupported request")

    def returnContent(self, ContentType, path):#return a valid file
        f = open(path)
        msg = 'HTTP/1.1 200 OK\r\nContent-Type: {}\r\n\r\n{}'.format(ContentType, f.read())
        f.close() 
        self.request.sendall(bytearray(msg, "utf-8"))

    def parseAndHandleFile(self, requestDirectory):
        if requestDirectory[-5:] == ".html":
            self.returnContent("text/html", G_DIRECTORY_ROOT +  requestDirectory)
            #print("HTML page requested!")

        elif requestDirectory[-4:] == ".css":
            self.returnContent("text/css", G_DIRECTORY_ROOT +  requestDirectory)
            #print("CSS page requested!")

        else:
            self.request.sendall(bytearray("HTTP/1.1 404 Not Found\r\n",'utf-8'))
            #print("Got a request for an unsupported file")
    




if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    print("Starting server....")
    socketserver.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = socketserver.TCPServer((HOST, PORT), MyWebServer)
    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
