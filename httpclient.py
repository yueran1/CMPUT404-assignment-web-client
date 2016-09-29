#!/usr/bin/env python
# coding: utf-8
# Copyright 2016 Abram Hindle, https://github.com/tywtyw2002, and https://github.com/treedust
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

# Do not use urllib's HTTP GET and POST mechanisms.
# Write your own HTTP GET and POST
# The point is to understand what you have to send and get experience with it

import sys
import socket
import re
# you may use urllib to encode data appropriately
import urllib

def help():
    print "httpclient.py [GET/POST] [URL]\n"

class HTTPResponse(object):
    def __init__(self, code=200, body=""):
        self.code = code
        self.body = body

class HTTPClient(object):

    def get_host_port(self,url):
      

	Request_URI=url.strip("/")
        Request_URI=Request_URI.strip("http://")
	Request_URI_List=Request_URI.split("/",1)
	
	#Split out the Host and Port information we want
	Host_Port=Request_URI_List[0]
	Host=Host_Port.split(":")[0]

	#If port is sepecifed in the path, return it directly
	#Otherwise, set port to default 80
	if len(Host_Port.split(":"))>1:
		Port=int(Host_Port.split(":")[1])
		
	else:
		Port=80
	
	#Assign all the address directory to the Variable path
	path="/"+"/".join(Request_URI_List[1:])
	
	
        return Host, Port, path

    def connect(self, host, port):
        # use sockets!
	# Use sockets to establish the Tcp connection
	client=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	client.connect((host,port))
        return client

    def get_code(self, data):
	#Split the response data and get the code
	code=int(data.split(" ")[1])      
	return code

    def get_headers(self,method,host,port,path,args):
	header= method + " "+path+ " HTTP/1.1\r\nHost: " + host + "\r\n"
	header= header+ "Connection: close\r\n"
	header= header+ "Accept-Encoding: */*\r\n"
	
	#This part handle the http POST method	
	if method == "POST":
	    if args == None:
		length = "0"
		body = ""
	    else:
		#use urllib to encode data appropriately
	    	body= urllib.urlencode(args,True)
	    	length = str(len(body))
	    header = header + "Content-type: application/x-www-form-urlencoded\r\n"
	    header = header + "Content-Length: " + length + "\r\n\r\n"
	    header = header + body
	header = header + "\r\n"
	return header

    def get_body(self, data):
        
	content=data.split("\r\n\r\n")
	body=content[1]
	return body

    # read everything from the socket
    def recvall(self, sock):
        buffer = bytearray()
        done = False
        while not done:
            part = sock.recv(1024)
            if (part):
                buffer.extend(part)
            else:
                done = not part
        return str(buffer)

    def GET(self, url, args=None):
        code = 500
        body = ""
        
	#Get host,port and path through function
	host,port,path=self.get_host_port(url)
	
	#Establish connect, and send the header we get
	client=self.connect(host,port)
	#Pass the http method GET and host,port,path and args to form header	
	header=self.get_headers("GET",host,port,path,args)
	client.sendall(header)
	data=self.recvall(client)
	client.close()	
	print data

	code=self.get_code(data)
	body=self.get_body(data)
	
        
        return HTTPResponse(code, body)

    def POST(self, url, args=None):
        code = 500
        body = ""
	
	host,port,path=self.get_host_port(url)
	client=self.connect(host,port)
	#Pass the http method POST and host,port,path and args to form header	
	header=self.get_headers("POST",host,port,path,args)
	client.sendall(header)

	data=self.recvall(client)
	client.close()	
	print data

	code=self.get_code(data)
	
	body=self.get_body(data)
        
        return HTTPResponse(code, body)

    def command(self, url, command="GET", args=None):
        if (command == "POST"):
            return self.POST( url, args )
        else:
            return self.GET( url, args )
    
if __name__ == "__main__":
    client = HTTPClient()
    command = "GET"
    if (len(sys.argv) <= 1):
        help()
        sys.exit(1)
    elif (len(sys.argv) == 3):
        print client.command( sys.argv[2], sys.argv[1] )
    else:
        print client.command( sys.argv[1] )   
