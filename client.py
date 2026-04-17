import socket
import time
import threading
import signal
from prompt_toolkit import prompt
from prompt_toolkit.patch_stdout import patch_stdout
inp = ""
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
	#with patch_stdout():
	while True:
		s.settimeout(0.5)
		try:
			print(decrypt(s.recv(1024).decode()), flush = True)
		except:
			pass

def getMess(inp):
	with patch_stdout():
	#global inp
		while True:
			print("this works ish")
			s.send(encrypt(inp).encode())
			inp = input("Message: ")
			if inp == "$close":
				return


with  socket.socket() as s:
	port = 12348
	s.connect(("127.0.0.1", port))
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
