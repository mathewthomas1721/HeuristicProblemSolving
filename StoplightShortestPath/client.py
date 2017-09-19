#Socket client example in python
 
import socket   #for sockets
import sys  #for exit
import struct
import time
 
#create an INET, STREAMing socket

class Client :
    def __init__(self,server_address,port):
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        except socket.error:
            print 'Failed to create socket'
            sys.exit()
             
        print 'Socket Created'
         
        self.server_address = server_address;
        self.port = port;
         
        '''try:
            remote_ip = socket.gethostname()
         
        except socket.gaierror:
            #could not resolve
            print 'Hostname could not be resolved. Exiting'
            sys.exit()'''
         
        
        self.socket.connect((self.server_address , self.port))
     
        print 'Socket Connected to ' + self.server_address
    
    def close(self):
        self.socket.close()

    def __del__(self):
        self.close()       
     
    def recv_stoplight(self,timeout=2):
        #make socket non blocking
        the_socket = self.socket
        the_socket.setblocking(0)
         
        #total data partwise in an array
        total_data=[];
        data='';
         
        #beginning time
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
 
    def send_resp(self, moves):
        #moves in the form of a string
        #print moves
        self.socket.send(moves)

    def wrap_recv():
        print recv_stoplight()
            
    def wrap_send():
        moves = '-1'.join(iter(raw_input, sentinel))
        send_resp(moves)        

