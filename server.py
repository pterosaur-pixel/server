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
			break
	users.append(userUE+ ";" + str(num))
	print(users)
	lock = threading.Lock()
	connected = False
	connTo = []
	ctrequested = False
	requested = False
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
		if "$ls" in cdata:
			userL = ""
			for user in users:
				user = user.split(";")
				user = user[0]
				if user != userUE:
					userL += user
					userL += " "
			c.send(encrypt(userL).encode())

		#Snake is asking to connect
		elif "$connect" in cdata:
			requested = True
			gotU = False
			userTC = ""
			cTC = connections[0]
			try:
				userTC = cdata.strip("\n").split(" ")[2]
				gotU = True
			except:
				c.send(encrypt("Invalid syntax. You should do, $connect [username to connect to]").encode())
			#Find client to connect to from username
			if gotU:
				foundCT = False
				for user in users:
					if user.split(";")[0] == userTC:
						cTC = connections[int(user.split(";")[1])]
						foundCT = True
						break
				#Ask for connection from frog
				if not foundCT:
					c.send(encrypt("connection failed1").encode())
				else:
					try:
						cTC.send(encrypt(userUE+" wants to connect to you ($a/$d)").encode())
					except:
						c.send(encrypt("REjected").encode())

		#If frog declines:
#		elif "d" in cdata and not connected:

		#If frog accepts
		elif "$a" in cdata and not connected:
			d2 = ""
			try:
				d2 = cdata.split(" ")[2]
			except:
				c.send(encrypt("incorrect syntax").encode())
			#find username accepted
			print("connecting to " + d2)
			ctc = connections[0]
			foundCT = False
			#find client from username
			for user in users:
				if user.split(";")[0] == d2:
					ctc = connections[int(user.split(";")[1])]
					foundCT = True
					break
			#Tell snake the he accepts
			if not foundCT:
				c.send(encrypt("connection failed2").encode())
			else:
				try:
					ctc.send(encrypt("$dyr " + userUE).encode())
				except:
					c.send(encrypt("client isn't connected"))
		#snake recieves frog's acceptance
		elif "$dyr" in cdata:
			print("$dyr is in the cdata")
			d2 = cdata.split(" ")[1]
			ctc = connections[0]
			ftc = False
			for user in users:
				if user.split(";")[0] == d2:
					ctc = connections[int(user.split(";")[1])]
					ftc = True
					break
			print("user" +d2)
			#Telling frog if he did request a connection
			if ftc:
				try:
					if requested:
						req = "TRUE"
						connected = True
						try:
							connTo[0] = ctc
						except:
							connTo.append(ctc)
						c.send(encrypt("Connection success!").encode())
					else:
						req = "FALSE"
					req += "$yourRequest"
					ctc.send(encrypt(req).encode())
				except:
					print("Something went wrong")
		#Frog recieves connection verification
		elif "$yourRequest" in cdata:
			print("Request noted")
			if cdata.split("$")[0] == "TRUE":
				ctrequested = True
				print("ctreq")
			#If verification from snake comes through
			if ctrequested:
				print("Well, they did request")
				try:
					connected = True
					try:
						connTo[0] = ctc
					except:
						connTo.append(ctc)
					c.send(encrypt("Connection successful").encode())
				except:
					c.send(encrypt("connection failed3").encode())

			ctrequested = False
			cdata += "fish"

		elif cdata == "$close":
			print("Client closed")
			mes1 = "$closed" + userUE
			for i in connections:
				try:
					i.send(encrypt(mes1).encode())
				except:
					pass
			return
		elif "$closed" in cdata:
			print("closing here"+userUE)
			username = list(cdata)[7:]
			print(username)
			ctr = connections[0]
			try:
				if connTo[0] == username[0]:
					connected = False
					ctrequested = False
					requested = False
					c.send(encrypt(username[0] + " disconnected").encode())
					connTo[0] = None
			except:
				pass
			for user in users:
				if user.split(";")[0] == username[0]:
					#ctr = user.split(";")[1]
					#connections.remove(ctr)
					users.remove(user)
			#print(userUE)
			#print(connections)


		elif "$disconnect" in cdata and not "$disconnected" in cdata:
			print("disconnecting")
			mes1 = "$disconnected"
			try:
				connTo[0].send(encrypt("$disconnected").encode())
				connected = False
				ctrequested = False
				requested = False
				connTo[0] = None
				c.send(encrypt("succesful disconnect").encode())
			except:
				c.send(encrypt("something went wrong").encode())
		elif "$disconnected" in cdata:
			#print("This section is running")
			c.send(encrypt("Thanks for talking, friend. See you later!").encode())
			c.send(encrypt("client disconnected").encode())
			connected = False
			ctrequested = False
			requested = False
			connTo[0] = None

		else:
			if connected:
				try:
					connTo[0].send(encrypt(cdata).encode())
				except:
					#print("??????????")
					c.send(encrypt("client disconnected").encode())
					connected = False
					connTo[0] = connections[0]
			else:
				c.send(encrypt("Not connected to anyone").encode())
				#Broadcast code, don't delete
				#for client in connections:
				#	if client != c:
				#		client.send(encrypt(cdata).encode())
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

