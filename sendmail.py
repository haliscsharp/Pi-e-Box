#!/usr/bin/env python

import smtplib

USER  = "adauthentication@gmail.com"
PASSWORD = "password"

server=smtplib.SMTP('smtp.gmail.com',587)

server.starttls()

server.login(USER,PASSWORD)

msg = "Subject:RFID box opened\nTest!"

server.sendmail("RFID_BOX","destination@gmail.com",msg)

server.quit()
