#SSP Client
import socket   
import sys 
import struct
import time
 


class Client :
    def __init__(self,server_address,port):
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        except socket.error:
            print 'SOCKET ERROR'
            sys.exit()
             
        self.server_address = server_address;
        self.port = port;
         
        
        self.socket.connect((self.server_address , self.port))
     
        print 'Connected! ' + self.server_address
    
    def close(self):
        self.socket.close()

    def __del__(self):
        self.close()       
     
    def recv_stoplight(self,timeout=2): #Function to make sure entire stoplight file is received using a timeout
        the_socket = self.socket
        the_socket.setblocking(0)
        total_data=[];
        data='';
        begin=time.time()

        while 1:
            #if you got some data, then break after timeout
            if total_data and time.time()-begin > timeout:
                break
             
            #if you got no data at all, wait a little longer, twice the timeout
            elif time.time()-begin > timeout*2:
                break
             
            #recv something
            try:
                data = the_socket.recv(8192)
                if data:
                    total_data.append(data)
                    #change the beginning time for measurement
                    begin=time.time()
                else:
                    #sleep for sometime to indicate a gap
                    time.sleep(0.1)
            except:
                pass
         
        #join all parts to make final string
        return ''.join(total_data)
 
    def send_resp(self, moves): #send moves in the form of a string
        self.socket.send(moves)

    def wrap_recv(): #wrapper for recv_stoplight
        print recv_stoplight()
            
    def wrap_send(): #wrapper for send_resp
        moves = '-1'.join(iter(raw_input, sentinel))
        send_resp(moves)        

