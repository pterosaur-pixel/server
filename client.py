import socket
import time
with  socket.socket() as s:
	#s.setblocking(False)
	port = 12348
	s.connect(("127.0.0.1", port))
	#s.setblocking(False)
	rec = False
	while not rec:
		try:
			print(s.recv(1024).decode())
			rec = True
		except:
			pass
	#print(s.getblocking())
	s.send("Thank you for hosting".encode())
	time.sleep(0.25)
	s.send("Thank you again".encode())
	inp = input("Message: ")
	while inp != "$close":
		s.send(inp.encode())
		inp = input("Messsage: ")
	time.sleep(0.25)
	s.send("close".encode())
#	while True:
#		cdata = s.recv(1024).decode()
