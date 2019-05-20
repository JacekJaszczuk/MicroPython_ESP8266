# Web serwer w Pythonie, zbudowany na gniazdkach.
print("Python WWW Server")

import socket
mes = b"Ala ma kota!"

def web_serv():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(("", 80))
    s.listen(5)

    while True:
        conn, addr = s.accept()
        print("Mamy połączenie od: {}", str(addr))
        conn.send(b"HTTP/1.1 200 OK\n")
        conn.send(b"Content-Type: text/html\n")
        conn.send(b"Connection: close\n\n")
        conn.sendall(mes)
        conn.close()

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