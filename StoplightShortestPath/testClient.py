from client import Client

client = Client('192.168.0.31',12345)

#print "recvstop"
print client.recv_stoplight()

f = open ('moves', "rb")
l = f.read()
#print l
client.send_resp(l)

