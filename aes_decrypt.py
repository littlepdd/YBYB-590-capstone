import base64
from Cryptodome.Cipher import AES
import sys
from Cryptodome import Random
import os

KEY = '0000000000000000'.encode('utf-8')
IV = b'0000000000000000'  # 自定IV向量


class AES_ENCRYPT():
    def __init__(self):
        self.aes = AES.new(KEY, AES.MODE_CBC, IV)

    # return type bytes
    def encrypt(self, bytes):
        add = 16 - len(bytes) % 16
        add %= 16

        bytes += (b'\0' * add)

        return self.aes.encrypt(bytes)
        # return type bytes

    def decrypt(self, bytes):
        bytes = self.aes.decrypt(bytes)
        return bytes.strip(b'\0')


MyAES = AES_ENCRYPT()


def encrypt_file(allfilename):
    # path_name=os.path.split(allfilename)
    print(allfilename)
    with open(allfilename, 'rb') as bin:
        bindata = bin.read()
        en_str = MyAES.encrypt(bindata)
        with open(allfilename[:-4] + ".png", 'wb') as out:
            out.write(en_str)
    #os.remove(allfilename)
def decrypt_file(allfilename):
    with open(allfilename, 'rb') as bin:
        bindata = bin.read()
        en_str = MyAES.decrypt(bindata)
        with open(allfilename[:-4], 'wb') as out:
            out.write(en_str)

#encrypt_file(r"C:\Users\Meng Linghao\Desktop\test1.zip")
print(sys.argv[1])
decrypt_file(sys.argv[1])
