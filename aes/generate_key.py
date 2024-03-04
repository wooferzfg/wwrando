import os
import secrets

key_file = open("aes_key.py", "w")
key_file.write("AES_KEY=" + str(os.urandom(32)))
key_file.close()

key_file = open("aes_iv.py", "w")
key_file.write("AES_IV=" + str(secrets.randbits(256)))
key_file.close()
