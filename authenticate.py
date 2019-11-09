#!/usr/bin/env python

import poplib
import string, random
import StringIO, rfc822
import logging

import pyotp

SERVER = "pop.gmail.com"
USER  = "adauthentication@gmail.com"
PASSWORD = "password"

# connect to server
logging.debug('connecting to ' + SERVER)
server = poplib.POP3_SSL(SERVER)
#server = poplib.POP3(SERVER)

# login
logging.debug('logging in')
server.user(USER)
server.pass_(PASSWORD)

# list items on server
logging.debug('listing emails')
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

#print(message["Date"])

while newEmail == False:
	#time.sleep(5)
	#print(time.ctime())
	
	# connect to server
	logging.debug('connecting to ' + SERVER)
	server = poplib.POP3_SSL(SERVER)
	#server = poplib.POP3(SERVER)
	
	# login
	logging.debug('logging in')
	server.user(USER)
	server.pass_(PASSWORD)
	
	# list items on server
	logging.debug('listing emails')
	resp, items, octets = server.list()
	
	# download the first message in the list
	id, size = string.split(items[len(items)-1])
	resp, text, octets = server.retr(id)
	
	# convert list to Message object
	text = string.join(text, "\n")
	file = StringIO.StringIO(text)
	message = rfc822.Message(file)
	
	#print(message["Date"])
	
	if message['Date'] != lastEmailReceived:
		newEmail = True
		print("email found")
	else:
		print("no email found")

#print(message['Subject'])
authPassword=pyotp.TOTP("UAFXHLEV3PJH3BUG").now()
if authPassword==message["Subject"]:
	print("OK ", message["Subject"], " = ", authPassword)
else:
	print("NO ", message["Subject"], " != ", authPassword)
