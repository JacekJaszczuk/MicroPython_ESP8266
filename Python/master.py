from machine import Pin
#import asyncio
import socket
import uasyncio as asyncio

motor_sleep_time = 0.01

async def motor_run():
    d1 = Pin(5, Pin.OUT)
    d2 = Pin(4, Pin.OUT)
    d3 = Pin(0, Pin.OUT)
    d4 = Pin(2, Pin.OUT)
    while True:
        d4.off()
        d1.on()
        await asyncio.sleep(motor_sleep_time)
        d1.off()
        d2.on()
        await asyncio.sleep(motor_sleep_time)
        d2.off()
        d3.on()
        await asyncio.sleep(motor_sleep_time)
        d3.off()
        d4.on()
        await asyncio.sleep(motor_sleep_time)

async def web_serv_run():
    global motor_sleep_time
    mes = b"Ala ma kota! Arek ma psa!"
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(("", 8080))
    s.listen(5)
    s.settimeout(0.001)
    while True:
        try:
                conn, addr = s.accept()
        except Exception as e:
                print(e)
                await asyncio.sleep(0)
                continue
        print ("Już nie śpię")
        motor_sleep_time = motor_sleep_time + 0.01
        #print("Mamy połączenie od: {}", str(addr))
        # Rób tak ładniej
        print(f"Mamy połączenie od: {addr}")
        conn.send(b"HTTP/1.1 200 OK\n")
        conn.send(b"Content-Type: text/html\n")
        conn.send(b"Connection: close\n\n")
        conn.sendall(mes)
        conn.close()

loop = asyncio.get_event_loop()
loop.create_task(motor_run())
loop.create_task(web_serv_run())
loop.run_forever()