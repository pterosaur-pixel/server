import socket
import time
import threading
import signal
import random
import sys
from prompt_toolkit import prompt
from prompt_toolkit.patch_stdout import patch_stdout
inp = ""
userUE = random.randrange(100, 300)
userUE = str(userUE)
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
	connected = False
	#with patch_stdout():
	while True:
		s.settimeout(0.5)
		try:
			recData = decrypt(s.recv(1024).decode())
#			s.send(encrypt("recieved").encode())
#			print("hello???")
#			if "$a/$d" in recData:
#				s.send(encrypt(recData))
#			elif recData == "$connection accepted":
#				s.send(encrypt(recData))
			print("recData")
			print(recData)
			if " connected to you" in recData and not connected:
				data2 = recData.split(" ")[0]
				inp = "$connect " + data2
				s.send(encrypt(inp).encode())
				connected = True
#			print(decrypt(s.recv(1024).decode()), flush = True)
		except:
			pass

def getMess(inp):
	with patch_stdout():
	#global inp
		while True:
			#print("this works ish")
			s.send(encrypt(inp).encode())
			inp = prompt("Message: ")
			if inp == "$close":
				return

if len(sys.argv) == 2:
	host = sys.argv[1]
else:
	host = "127.0.0.1"

with  socket.socket() as s:
	port = 12348
	s.connect((host, port))
	s.send(encrypt(userUE).encode())
	inp = input("Message: ")
	t1 = threading.Thread(target = getMess, args=(inp,), daemon = True)
	t1.start()
	t2 = threading.Thread(target = listenTo, args = (s,), daemon = True)
	t2.start()
	#while inp != "$close":
	#	s.settimeout(0.5)
		#try:
			#print(decrypt(s.recv(1024).decode()))
			#inp = input("Message")
		#except:
		#	pass
	#time.sleep(0.25)
	t1.join()
	t2.join()
	s.send(encrypt("close").encode())
