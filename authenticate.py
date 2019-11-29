#!/usr/bin/env python

# mail + general
import poplib
import smtplib
import string, random
import StringIO, rfc822
import logging
import time

time.sleep(3)

# authentication
import pyotp
# IO
import RPi.GPIO as GPIO
# RFID
from mfrc522 import SimpleMFRC522

SERVER = "pop.gmail.com"
USER  = "adauthentication@gmail.com"
PASSWORD = "password"

RELAY=21
LED_G=14
LED_R=18

green=False # keep track of led color

# initialize GPIO pin
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(RELAY,GPIO.OUT,initial=GPIO.LOW) # Relay
GPIO.setup(LED_G,GPIO.OUT,initial=GPIO.LOW) # green led
GPIO.setup(LED_R,GPIO.OUT,initial=GPIO.LOW) # red led

# turn on GPIO pin
def gON(g_num):
	GPIO.output(g_num,GPIO.HIGH)

# turn off GPIO pin
def gOFF(g_num):
	GPIO.output(g_num,GPIO.LOW)

closed = True

#print("start")
reader = SimpleMFRC522()

gON(LED_R)
time.sleep(1)
gOFF(LED_R)
gON(LED_G)
time.sleep(1)
gOFF(LED_G)

try:
	while (True):
		if (closed):
			# waiting for RFID read
			nfcId, text = reader.read()
			if(nfcId==1019974132615):
				# joker card
				gON(LED_G)
				
				# open relay for 3 sec
				gON(RELAY)
				time.sleep(3)
				gOFF(RELAY)
				
				gOFF(LED_G)
				
				closed=False
				
				# send email
				smtpserver=smtplib.SMTP('smtp.gmail.com',587)
				smtpserver.starttls()

				smtpserver.login(USER,PASSWORD)

				msg = "Subject:RFID box opened\nHello!\n\nYour NFC box has been opened with the JOKER card!"
				smtpserver.sendmail("RFID_BOX","consolewriteline86@gmail.com",msg)

				smtpserver.quit()
			elif(nfcId==39583897861 or nfcId==584189945031):
				# correct RFID
				#print("OK")
				
				gON(LED_G)
				
				# connecting to server
				popserver = poplib.POP3_SSL(SERVER)

				# login
				popserver.user(USER)
				popserver.pass_(PASSWORD)

				# list items on popserver
				resp, items, octets = popserver.list()

				# download the first message in the list
				id, size = string.split(items[len(items)-1])
				resp, text, octets = popserver.retr(id)

				# convert list to Message object
				text = string.join(text, "\n")
				file = StringIO.StringIO(text)
				message = rfc822.Message(file)

				lastEmailReceived=message['Date']
				newEmail=False

				#print("initialized")
				
				gOFF(LED_G)
				
				timeLimit=25
				initialTime=time.time()

				while newEmail == False and time.time()-initialTime < timeLimit:
					#print(time.time()-initialTime)
					
					# connect to server
					popserver = poplib.POP3_SSL(SERVER)
					
					# login
					popserver.user(USER)
					popserver.pass_(PASSWORD)
					
					# list items on popserver
					resp, items, octets = popserver.list()
					
					# download the first message in the list
					id, size = string.split(items[len(items)-1])
					resp, text, octets = popserver.retr(id)
					
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
					gON(LED_R)
					time.sleep(2)
					gOFF(LED_R)
				elif authPassword == message["Subject"]:
					# correct password
					gON(LED_G)
					
					# open relay for 3 sec
					gON(RELAY)
					time.sleep(3)
					gOFF(RELAY)
					
					gOFF(LED_G)
					closed = False
					
					# send email
					smtpserver=smtplib.SMTP('smtp.gmail.com',587)
					smtpserver.starttls()

					smtpserver.login(USER,PASSWORD)

					msg = "Subject:RFID box opened\nHello!\n\nYour NFC box has been opened! (NFC id = " + str(nfcId) + ")"
					smtpserver.sendmail("RFID_BOX","consolewriteline86@gmail.com",msg)

					smtpserver.quit()
				else:
					# incorrect password
					gON(LED_R)
					time.sleep(2)
					gOFF(LED_R)
			elif (nfcId == 584195779439):
				# special, exit program card
				gON(LED_G)
				time.sleep(1)
				gOFF(LED_G)
				gON(LED_R)
				time.sleep(1)
				gOFF(LED_R)
				
				exit()
			else:
				# Wrong RFID
				gON(LED_R)
				time.sleep(2)
				gOFF(LED_R)
		else:
			# waiting for RFID read
			nfcId, text = reader.read()
			if(nfcId == 39583897861 or nfcId == 584189945031 or nfcId==1019974132615):
				# correct RFID / joker card
				gON(LED_G)
				
				gON(RELAY)
				time.sleep(3)
				gOFF(RELAY)
				
				gOFF(LED_G)
				closed = True
			elif (nfcId == 584195779439):
				exit()
			else:
				# wrong RFID
				gON(LED_R)
				time.sleep(2)
				gOFF(LED_R)

finally:
	GPIO.cleanup()
