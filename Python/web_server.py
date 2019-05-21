# Web serwer w Pythonie, zbudowany na gniazdkach.
print("Python WWW Server")

import socket
#mes = b"Ala ma kota!"
fd = open("../Test_HTML/json_exchange.html", "r")
mes = bytes(fd.read(), "UTF-8")
fd.close()

def web_serv():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(("", 8080))
    s.listen(5)
    s.settimeout(0.5)

    while True:
        try:
                conn, addr = s.accept()
        except Exception as e:
                print(e)
                continue
        print ("Już nie śpię")
        print("Mamy połączenie od: {}", str(addr))
        data = conn.recv(2048)
        print(data)
        #poz = data.find("ala")
        poz = data.find(b"{\"")
        print(poz)
        print("Data type: ", type(data))
        sub_string = data[poz:]
        print("Sub type: ", type(sub_string))
        print(sub_string)
        print(sub_string.hex())
        print("O rany")
        conn.send(b"HTTP/1.1 200 OK\n")
        conn.send(b"Content-Type: text/html\n")
        conn.send(b"Connection: close\n\n")
        conn.sendall(mes)
        conn.close()

web_serv()

'''
import time
from machine import Pin

d1 = Pin(5, Pin.OUT)
d2 = Pin(4, Pin.OUT)
d3 = Pin(0, Pin.OUT)
d4 = Pin(2, Pin.OUT)

def silnik():
    while True:
        d4.off()
        d1.on()
        time.sleep_ms(10)
        d1.off()
        d2.on()
        time.sleep_ms(10)
        d2.off()
        d3.on()
        time.sleep_ms(10)
        d3.off()
        d4.on()
        time.sleep_ms(10)
'''