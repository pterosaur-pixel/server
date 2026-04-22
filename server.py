import ipaddress
import threading
import socket
import select
data = "This is the data: "
data2 = "This is the data2: "
def encrypt(string):
	letters = list(string)
	enc = ""
	for let in letters:
		orded = ord(let)+32
		while orded > 127:
			orded = orded - 127
		enc += str(orded)
		enc += " "
	enc = enc[:-1]
	return enc
def decrypt(string):
	nums = string.split(" ")
	let = ""
	for i in nums:
		num = int(i)
		num -= 32
		if num < 0:
			num += 127
		let += chr(num)
	return let

def clientThread(c, addr, connnections, users):
	print("got connection from", addr)
	userUE = (decrypt(c.recv(1024).decode()))
	num = 0
	for i in range(0, len(connections)):
		if connections[i] == c:
			num = i
			#print(num)
			break
	users.append(userUE+ ";" + str(num))
	print(users)
	lock = threading.Lock()
	connected = False
	connTo = []
	while True:
		cdata = c.recv(1024)
		if cdata == (b''):
			print("Disconnected: ", addr)
			with lock:
				connections.remove(c)
				for i in users:
					if i.split(";")[0] == userUE:
						users.remove(i)
			return
		cdata = decrypt(cdata.decode())
		if cdata == "ls":
			for user in users:
				user = user.split(";")
				user = user[0]
				if user != userUE:
					c.send(encrypt(user).encode())

		#This is the guy who wants to connect
		elif "$connect" in cdata:
			#print("Is my code even running?") Noto to me later: It really wasn't I forgot the $
			gotU = False
			userTC = ""
			cTC = connections[0]
			try:
				userTC = cdata.strip("\n").split(" ")[1]
				gotU = True
			except:
				c.send(encrypt("Invalid syntax. You should do, $connect [username to connect to]").encode())

			#print(gotU)
			if gotU:
				for user in users:
					print(user)
					if user.split(";")[0] == userTC:
						cTC = connections[int(user.split(";")[1])]
						print(cTC)
						break
				try:
					cTC.send(encrypt("Connected to by " + userUE).encode())
					connected = True
					connTo.append(cTC)
				except:
					c.send(encrypt("REjected").encode())


#		elif not connected and cdata == "connect":
#			c.send(encrypt("Input username of client you wish to connect with").encode())
#			userTC = decrypt(c.recv(1024).decode())
#			cTC = []
#			for user in users:
#				user = user.split(";")
#				if user[0] == userTC:
#					cTC = connections[int(user[1])]
#					cTC.send(encrypt(userUE + "%" + "would like to connect with you($a/$d)").encode())
#					try:
#						if decrypt(c.recv(1024).decode()) == "$connection accepted":
#							connected = True
#							connTo = cTC
#						break;
#					except:
#						c.send(encrypt("connection failed").encode())
#		elif connected and cdata == "connect":
#			c.send(encrypt("already connected").encode())
		#elif "$a/$d" in cdata:
		#	print("a/d")
#		elif not connected and "$a/$d" in cdata:
#			print(cdata)
#			cdata = cdata.split("%")
#			cTC = []
#			for user in users:
#				user = user.split(";")
#				if user[0] == cdata[0]:
#					cTC = connections[int(user[1])]
					#c.send(encrypt("connection accepted").encode())
#					try:
#						cTC.send(encrypt("$connection accepted").encode())
#						connTo = cTC
#					except:
#						c.send(encrypt("connection failed").encode())


		else:
			if connected:
				connTo[0].send(encrypt(cdata).encode())
			else:
				for client in connections:
					if client != c:
						client.send(encrypt(cdata).encode())
		print(cdata)

with socket.socket() as s:
	s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	print(s.getblocking())
	users = []
	connections = []
	port = 12348
	s.bind(("", port))
	print("socket binded")
	s.listen(2)
	while True:
		c, addr = s.accept()
		connections.append(c)
		t1 = threading.Thread(target = clientThread, daemon = True, args=(c, addr, connections, users,))
		t1.start()

