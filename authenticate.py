# mail + general
import poplib
import string, random
import StringIO, rfc822
import logging
import time

time.sleep(5)

# authentication
import pyotp
# IO
import RPi.GPIO as GPIO
# RFID
from mfrc522 import SimpleMFRC522

SERVER = "pop.gmail.com"
USER  = "adauthentication@gmail.com"
PASSWORD = "password"

# initialize GPIO pin
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(21,GPIO.OUT,initial=GPIO.LOW)

print("start")
reader = SimpleMFRC522()

try:
	# waiting for RFID read
	id, text = reader.read()
	
	if(id==39583897861 or id==584189945031):
		print("OK")
		
		# connecting to server
		server = poplib.POP3_SSL(SERVER)

		# login
		server.user(USER)
		server.pass_(PASSWORD)

		# list items on server
		resp, items, octets = server.list()

		# download the first message in the list
		id, size = string.split(items[len(items)-1])
		resp, text, octets = server.retr(id)

		# convert list to Message object
		text = string.join(text, "\n")
		file = StringIO.StringIO(text)
		message = rfc822.Message(file)

		lastEmailReceived=message['Date']
		newEmail=False

		print("initialized")

		timeLimit=25
		initialTime=time.time()

		while newEmail == False and time.time()-initialTime < timeLimit:
			print(time.time()-initialTime)
			# connect to server
			server = poplib.POP3_SSL(SERVER)
			
			# login
			server.user(USER)
			server.pass_(PASSWORD)
			
			# list items on server
			resp, items, octets = server.list()
			
			# download the first message in the list
			id, size = string.split(items[len(items)-1])
			resp, text, octets = server.retr(id)
			
			# convert list to Message object
			text = string.join(text, "\n")
			file = StringIO.StringIO(text)
			message = rfc822.Message(file)
			
			# check for new email
			if message['Date'] != lastEmailReceived:
				newEmail = True

		# get 2FA password
		authPassword=pyotp.TOTP("UAFXHLEV3PJH3BUG").now()
		
		# compare received message with password
		if time.time()-initialTime >= timeLimit:
			# time exceeded
			print("Too late :/")
		elif authPassword == message["Subject"]:
			# correct password
			print("Correct ", message["Subject"], " = ", authPassword)
			
			# open relay for 3 sec
			GPIO.output(21,GPIO.HIGH)
			time.sleep(3)
			GPIO.output(21,GPIO.LOW)
		else:
			# incorrect password
			print("Incorrect ", message["Subject"], " != ", authPassword)
	else:
		print("Nah")
finally:
	GPIO.cleanup()

