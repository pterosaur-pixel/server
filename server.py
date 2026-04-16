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

def clientThread(c, addr):
	print("got connection from", addr)
	while True:
		cdata = c.recv(1024)
		if cdata == (b''):
			print("Disconnected: ", addr)
			return
		cdata = decrypt(cdata.decode())
		print(cdata)

with socket.socket() as s:
	s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	print(s.getblocking())
	port = 12348
	s.bind(("", port))
	print("socket binded")
	s.listen(2)
	while True:
		c, addr = s.accept()
		t1 = threading.Thread(target = clientThread, daemon = True, args=(c, addr,))
		t1.start()

