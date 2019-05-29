from machine import Pin
import socket
import uasyncio as asyncio
import json

# Zmienne globalne do sterowania silnika:
motor_sleep_time_base = 0.001
motor_direction = "L"
motor_sleep_time = motor_sleep_time_base * 10
motor_on = True

# Funkcja sterująca silnikiem:
async def motor_run():
    # Definiuj zmienne globalne:
    global motor_direction
    global motor_sleep_time
    global motor_on

    # Definicje pinów:
    d1 = Pin(5, Pin.OUT)
    d2 = Pin(4, Pin.OUT)
    d3 = Pin(0, Pin.OUT)
    d4 = Pin(2, Pin.OUT)

    # Pętla główna silnika:
    while True:
        # Sprawdź czy silnik ma być uruchomiony:
        if motor_on == True:
            # Sprawdź w którą stronę kręcić silnikiem:
            if motor_direction == "L":
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
            elif motor_direction == "P":
                d4.off()
                d3.on()
                await asyncio.sleep(motor_sleep_time)
                d3.off()
                d2.on()
                await asyncio.sleep(motor_sleep_time)
                d2.off()
                d1.on()
                await asyncio.sleep(motor_sleep_time)
                d1.off()
                d4.on()
                await asyncio.sleep(motor_sleep_time)
            else:
                await asyncio.sleep(0)
        else:
            await asyncio.sleep(0)

async def web_serv_run():
    # Definiuj zmienne globalne:
    global motor_direction
    global motor_sleep_time
    global motor_on

    # Otwórz i przeczytaj plik HTML do serwowania na serwerze:
    html_file = open("index.html", "rb")
    html = html_file.read()
    html_file.close()

    # Utwórz gniazdko sieciowe TCP:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(("", 8080))   # Binduj gniazdko na localhost'ice oraz porcie 8080.
    s.listen(5)          # Maksmyalna liczba połączeń na gniazdku to 5.
    s.settimeout(0.001)  # Timeout gniazdka.

    # Główna pętla serwera:
    while True:
        try:
            # Czekaj na połączenie:
            conn, addr = s.accept()
        except Exception as e:
            # Mamy timeout lub inny błąd:
            await asyncio.sleep(0)
            continue

        # Mamy połączenie, obsługujemy je:
        conn.settimeout(None) # Wyłącz timeout bo nie da się przesłać dużych komunikatów.
        print("Mamy połączenie od: {}", str(addr))

        # Odbierz odpowiedź z serwera:
        data = conn.recv(2048)
        print(data)
        poz = data.find(b"{\"")
        # Szukaj JSONa:
        if poz == -1:
                print("Nie ma JSONa!")
        else:
                print("Jest JSON!")
                json_str = data[poz:]
                print("Twój JSON:", json_str)
                dic = json.loads(json_str)
                # Ustaw nastawy silnika:
                try:
                    motor_direction = dic["kierunek"]
                    print("Twój kierunek:", motor_direction)
                except:
                    pass
                try:
                    motor_sleep_time = motor_sleep_time_base * (100.0 - float(dic["predkosc"]))
                    print("Twoja prędkość:", motor_sleep_time)
                except:
                    pass
                
                try:
                    motor_on = dic["power"]
                    print("Silnik włączony:", motor_on)
                except:
                    pass

        # Wyślij nagłówki HTML oraz stronę HTML do przeglądarki internetowej:
        conn.send(b"HTTP/1.1 200 OK\n")
        conn.send(b"Content-Type: text/html\n")
        conn.send(b"Connection: close\n\n")
        conn.sendall(html)
        conn.close()

loop = asyncio.get_event_loop()
loop.create_task(motor_run())
loop.create_task(web_serv_run())
loop.run_forever()