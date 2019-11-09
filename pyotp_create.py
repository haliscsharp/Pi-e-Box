import pyotp

pyotp.totp.TOTP('R2PV7PH25AM5I5LU').provisioning_uri("RFID_BOX", issuer_name="RFID box")
