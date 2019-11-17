import RPi.GPIO as GPIO
import time

from mfrc522 import SimpleMFRC522

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(21,GPIO.OUT,initial=GPIO.LOW)

reader = SimpleMFRC522()

try:
	while (True):
		print("init")
		id, text = reader.read()
		if(id==39583897861 or id==584189945031):
			print("OK")
			GPIO.output(21,GPIO.HIGH)
			time.sleep(2)
			GPIO.output(21,GPIO.LOW)
		elif(id==584195779439):
			exit()
		else:
			print("Nah")
finally:
	GPIO.cleanup()
