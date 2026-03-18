#general libraries
import machine
import utime
#wireless communication libraries
import network
import socket
#humidity sensor libraries
#from machine import Pin
#import dht


#sensor_temp = machine.ADC(4) #temperature sensor
#conversion_factor = 3.3 / (65535) #conversion for Celcius
#led_green = machine.Pin(25, machine.Pin.OUT) #green LED (turn on AC)
#led_red = machine.Pin(25, machine.Pin.OUT) #red LED (control thermostat)
#sensor = dht.DHT22(Pin(2)) #dht object to gpio pin

#access point
ssid = 'coconut' #access point name
password = 'secure789!' #access point password

ap = network.WLAN(network.AP_IF)
ap.config(essid=ssid, password=password)
ap.active(True) #activate

while ap.active() == False:
    pass
print('Successful connection')
print(ap.ifconfig())


#socket server
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('', 80))
s.listen(5)



#temperature sensing function
##def read_temp():
   # while True:
    #    reading = sensor_temp.read_u16() * conversion_factor
     #   temp = 27 - (reading - 0.706)/0.001721
     #   print(temp)
     #   utime.sleep(2)
        
     #   if temp.value() > 26: #is temp too high?
        #    led_red.toggle(1)
     #   if temp.value() < 20: #is temp too low?
         #   led_red.toggle(1)
      #  else:
         #   led_red.toggle(0)
            
   # return temp


#humidity sensing function
#while True:
    #try:
       # utime.sleep(2)
      #  hum = sensor.humidity()
    #except OSError as e:
       # print('failed to read sensor.')

#webpage
def webpage():
    html = f"""
        <!DOCTYPE html>
            <html>
            <head>
                <meta http-equiv="refresh" content="2">
                <title style="background-color:SlateBlue;color:White;"> Shower Dashboard </title>
            </head>
            <body>
            
            <div>
                <h3 style="color:SlateBlue"> Room Stats </h3>
                <p>Current Temperature (C): {temp} </p>
                <p>Current Humidity (%): </p>
            </div>
            
            </body>
            </html>
            """
    #return webpage as string
    return str(html)

while True: #response when connection is received
    print('this works')
    conn, addr = s.accept()
    print('Have connection from %s' % str(addr))
    request = conn.recv(1024)
    
    #temp = get_temp() #get temp by calling function
    response = webpage() #respond to call by loading webpage
    print('this runs')
    
    conn.send("HTTP/1.1 200 OK\n")
    conn.send("Content-Type: text/html\n")
    conn.send("Connection: close\n\n")
    conn.sendall(response)
    conn.close()