import socket
def run_server(addr):
    '''send command'''
    s = socket.socket()
    s.bind(addr)
    s.listen()
    try:
        while True:
            # start to accecpt connections and send commands to the target
            c, c_addr = s.accept()
            print(f"[connect] {c_addr}")
            cmd = input("Enter command: ")
            cmd = cmd.encode("utf-8")
            c.send(cmd)
            # get target returned msg
            msg = c.recv(1024)
            msg = msg.decode("utf-8")
            print(msg)
            c.close()
    except KeyboardInterrupt:
        print("end server")
    exit(1)
if __name__ == '__main__':
    ADDR = ('127.0.0.1',8888)
    run_server(ADDR)