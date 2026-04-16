import socket
import time
import threading
import signal
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

def listenTo(s):
	while True:
		s.settimeout(0.5)
		try:
			print(decrypt(s.recv(1024).decode()))
		except:
			pass

def getMess(inp):
	while True:
		s.send(encrypt(inp).encode())
		inp =input("Message: ")
		if inp == "$close":
			return


with  socket.socket() as s:
	port = 12348
	s.connect(("127.0.0.1", port))
	rec = False
	while not rec:
		try:
			print(decrypt(s.recv(1024).decode()))
			rec = True
		except:
			pass
	s.send(encrypt("Thank you for hosting").encode())
	time.sleep(0.25)
	s.send(encrypt("Thank you again").encode())
	inp = input("Message: ")
	t1 = threading.Thread(target = getMess, args = (inp,))
	t1.start()
	while inp != "$close":
		s.settimeout(0.5)
		try:
			print(decrypt(s.recv(1024).decode()))
		except:
			pass
	time.sleep(0.25)
	t1.join()
	s.send(encrypt("close").encode())
