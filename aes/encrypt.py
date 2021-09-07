import binascii
import pyaes
import sys

from aes_iv import AES_IV
from aes_key import AES_KEY

input_path = sys.argv[1]
output_path = sys.argv[2]

file_to_encrypt = open(input_path, "r")
content_to_encrypt = file_to_encrypt.read()

aes = pyaes.AESModeOfOperationCTR(AES_KEY, pyaes.Counter(AES_IV))
ciphertext = aes.encrypt(content_to_encrypt)
encrypted = binascii.hexlify(ciphertext)

encrypted_output = open(output_path, "wb")
encrypted_output.write(binascii.hexlify(ciphertext))
encrypted_output.close()

encrypted_input = open(output_path, "r")

aes2 = pyaes.AESModeOfOperationCTR(AES_KEY, pyaes.Counter(AES_IV))
decrypted = aes2.decrypt(binascii.unhexlify(encrypted_input.read()))
