from machine import Pin
import socket
import uasyncio as asyncio
import json

# Zmienne globalne do sterowania silnika:
motor_sleep_time_base = 0.001
motor_direction = "L"
motor_sleep_time = motor_sleep_time_base * 10
motor_on = True
motor_czy_nastawy = False
motor_nastawy_kierunki = []
motor_nastawy_kroki = []
motor_nastawy_predkosci = []

async def motor_step_left(d1, d2, d3, d4):
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

async def motor_step_right(d1, d2, d3, d4):
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

def motor_set_speed(predkosc):
    global motor_sleep_time
    motor_sleep_time = motor_sleep_time_base * (100.0 - float(predkosc))

# Funkcja sterująca silnikiem:
async def motor_run():
    # Definiuj zmienne globalne:
    global motor_direction
    global motor_sleep_time
    global motor_on
    global motor_czy_nastawy
    global motor_nastawy_kierunki
    global motor_nastawy_kroki
    global motor_nastawy_predkosci

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
                await motor_step_left(d1, d2, d3, d4)
            elif motor_direction == "P":
                await motor_step_right(d1, d2, d3, d4)
            else:
                await asyncio.sleep(0)
        elif motor_czy_nastawy == True:
            # Obsługuj nastawy:
            i = 0
            print("Długość wektora z nastawami:", len(motor_nastawy_kierunki))
            while i < len(motor_nastawy_kierunki):
                print("Krok:", i)
                motor_set_speed(motor_nastawy_predkosci[i])
                j = 0
                while j < int(motor_nastawy_kroki[i]):
                    if j % 10 == 0:
                        print(j)
                    if motor_nastawy_kierunki[i] == "L":
                        await motor_step_left(d1, d2, d3, d4)
                    else:
                        await motor_step_right(d1, d2, d3, d4)
                    j = j + 1
                i = i + 1
            motor_czy_nastawy = False
        else:
            await asyncio.sleep(0)

async def web_serv_run():
    # Definiuj zmienne globalne:
    global motor_direction
    global motor_sleep_time
    global motor_on
    global motor_czy_nastawy
    global motor_nastawy_kierunki
    global motor_nastawy_kroki
    global motor_nastawy_predkosci

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
        data = b""
        buf = conn.recv(2048)
        data = buf
        print("Ile:", len(buf))
        while len(buf) == 536: # Są jeszcze jakieś dane do odebrania!
            buf = conn.recv(2048)
            data = data + buf
            print("Ile:", len(buf))
        print(data)
        print("Ilość odebranych bajtów to:", len(data))
        poz = data.find(b"{")
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
                motor_set_speed(dic["predkosc"])
                print("Twoja prędkość:", motor_sleep_time)
            except:
                pass
            try:
                motor_on = dic["power"]
                print("Silnik włączony:", motor_on)
            except:
                pass
            try:
                motor_nastawy_kierunki = dic["jsonDataFromFile"]["kierunek"]
                motor_nastawy_kroki = dic["jsonDataFromFile"]["kroki"]
                motor_nastawy_predkosci = dic["jsonDataFromFile"]["predkosc"]
                motor_on = False
                motor_czy_nastawy = True
                print("Ustawiono nastawy!")
            except:
                pass

        # Wyślij nagłówki HTML oraz stronę HTML do przeglądarki internetowej:
        conn.send(b"HTTP/1.1 200 OK\n")
        conn.send(b"Content-Type: text/html\n")
        conn.send(b"Connection: close\n\n")
        conn.sendall(html)
        print("Zamykamy już to połączenie!")
        conn.close()

loop = asyncio.get_event_loop()
loop.create_task(motor_run())
loop.create_task(web_serv_run())
loop.run_forever()