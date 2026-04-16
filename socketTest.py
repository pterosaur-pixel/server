import ipaddress
import socket
import select
data = "This is the data: "
data2 = "This is the data2: "
with socket.socket() as s:
	s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	#s.setblocking(False)
	print(s.getblocking())
	port = 12348
	s.bind(("", port))
	print("socket binded")
	s.listen(2)
#	got1 = False
#	while not got1:
#		try:
	c, addr = s.accept()
#	got1 = True
	#	except:
#		pass
#	got2 = False
#	while not got2:
	s.settimeout(0.1)
	try:
		c2, addr2 = s.accept()
		print(c2)
#	got2 = True
	except:
		c2 = None
	print("got connection from",  addr)
	c.send("Thank you for connecting".encode())
	if c2 != None:
		c2.send("Thank you for connecting".encode())
		print("got conn from", addr2)
	cdata = c.recv(1024).decode()
	try:
		cdata2 = c2.recv(1024).decode()
	except:
		cdata2 = None
	print("cdata")
	print(cdata)
	print(cdata2)
	closed1 = False
	closed2 = False
	#for i in range(0, 2):
	while cdata.strip("\n") != "close" or cdata2.strip("\n") != "close":
		if c2 == None:
			s.settimeout(0.1)
			try:
				c2, addr2 = s.accept()
				c2.send("Thank you for connecting".encode())
				print("got conn from", addr2)
				cdata2 = c2.recv(1024).decode()
				closed2 = False
			except:
				c2 = None
		if cdata.strip("\n") != "close":
			try:
				#print(1)
				readable,_,_ = select.select([c], [],[], 0.1)
				#print(readable)
				if c in readable:
					cdata = c.recv(1024).decode()
					#print("got data")
					if cdata != None and not closed1:
						print(cdata)
						data += cdata
			except:
				pass
		else:
			closed1 = True
		#print(closed2)
		if c2 != None and cdata2.strip("\n") != "close" and not closed2:
			try:
				#print("Could read from client number 2")
				readable,_,_ = select.select([c2], [], [], 0.1)
				#print(2)
				#print(readable)
				if c2 in readable:
					cdata2 = c2.recv(1024).decode()
					#print("got data 2")
					if cdata2 != None and not closed2:
						print(cdata2)
						data2 += cdata2
			except:
				pass
		else:
			closed2 = True
		#cdata = c.recv(1024).decode()
	print("cdata")
	print(cdata)
	print(cdata2)
	c.close()
#print(data)
