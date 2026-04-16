import socket
import time
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

with  socket.socket() as s:
	#s.setblocking(False)
	port = 12348
	s.connect(("127.0.0.1", port))
	#s.setblocking(False)
	rec = False
	while not rec:
		try:
			print(decrypt(s.recv(1024).decode()))
			rec = True
		except:
			pass
	#print(s.getblocking())
	s.send(encrypt("Thank you for hosting").encode())
	time.sleep(0.25)
	s.send(encrypt("Thank you again").encode())
	inp = input("Message: ")
	while inp != "$close":
		s.send(encrypt(inp).encode())
		inp = input("Messsage: ")
	time.sleep(0.25)
	s.send(encrypt("close").encode())
#	while True:
#		cdata = s.recv(1024).decode()
