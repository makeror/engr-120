#general libraries
import machine
import utime
import math

#wireless communication libraries
import network
import socket

#humidity sensor libraries
from machine import Pin
import dht


tempsensor = machine.ADC(28) 					#temperature sensor
conversion_factor = 3.3 / (65535) 				#conversion for Celcius
led_green = machine.Pin(25, machine.Pin.OUT) 	#green LED (turn on AC)
led_red = machine.Pin(25, machine.Pin.OUT) 		#red LED (control thermostat)
sensor = dht.DHT22(Pin(2)) 						#dht object to gpio pin


def gettemp():
    readtemp = tempsensor.read_u16()
    temp = round((((1/(1/298+(1/3960)*math.log((65535/(readtemp)-1)))) - 273)*0.73),1)
    return str(temp)

def gethum():
    try:
        sensor.measure()
        hum = sensor.humidity()
        return str(hum)
    except OSError as e:
        print('Sensor not read')

def getocc():
    occ = 0
    return str(occ)

def motor():
    turn = 0
    return str(turn)

def alerts(temp, hum, occ):
    tlert = "No Current Alerts"
    halter = "No Current Alerts"
    oalert = "No Current Alerts"
    if temp > 30:
        taltert = "High Temperature"
    if hum > 80:
        halert = "High Humidity"
    if occ = 1:
        oalert = "Currently Occupied"
    
    return hlert
    return talert
    return oalert

def webpage(temp, hum, occ):
    html = f"""
        <!DOCTYPE html>
            <html>
            <head>
                <meta http-equiv'"refresh" content="2">
            <style>
.page { display: none; }
.page:target { display: block; }
.vbutton {
                    background-color: #000066;
                    color: white;
                    font-size: 15px;
                    padding: 12px;
                    border: none;
                    border-radius: 15px:
                    cursor: pointer;
                    text-align: center;
                    }
                .vbutton:hover {
                    background-color: powderblue;
                    color: #000066;
                    }
                    body {
                    background-color: #e6e6e6;
                    color: white;
                    font-family: helvetica;
                    font-size: 70%;
                    }
                p {
                    color: #000066;
                    }
     
            .alert {
              padding: 20px;
              background-color: #f44336; /* Red */
              color: white;
              margin-bottom: 15px;
            }


            .closebtn {
              margin-left: 15px;
              color: white;
              font-weight: bold;
              float: right;
              font-size: 22px;
              line-height: 20px;
              cursor: pointer;
              transition: 0.3s;
            }

            .closebtn:hover {
            color: black;
            }
</style>
</head>
<body>
<ul>
<button class= "vbutton"><a href="#page1">Residents</a></button>
<button class= "vbutton"><a href="#page2">Maintenance Staff</a></button>
</ul>

<div id="page1" class="page">
<h1>Residents</h1>
<p>                <p style="text-align:center;"> Occupancy Status: {occ} </p>
<a href="#head">Go to Home</a>
</div>

<div id="page2" class="page">
<h1>Maintenance Staff</h1>
<p> <p style="text-align:center;"> Temperature: {temp} </p>
                <p style="text-align:center;"> Humidity: {hum} </p>
                <p style="text-align:center;"> Occupancy Status: {occ} </p>
                <button class="vbutton"> <a href=""> Turn on HVAC </a> </button>
                
<a href="#head">Go to Home</a>
<div class="alert">
if(temp > 45)
    <span class="closebtn" onclick="this.parentElement.style.display='none';">&times;</span>
  Temperature alert: excessive heat
</div>
</div>

</body>
</html>
     
            """
    return str(html) 	#return webpage as string


#access point
ssid = 'coconut' 		#access point name
password = 'secure789!' #access point password

ap = network.WLAN(network.AP_IF)
ap.config(essid=ssid, password=password)
ap.active(True) 		#activate

while ap.active() == False:
    pass
print('Successful connection')
print(ap.ifconfig())	#get Pico IP address


#socket server
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('', 80))
s.listen(5)

        
     #   if temp.value() > 26: #is temp too high?
          #  led_red.toggle(1)
     #   if temp.value() < 20: #is temp too low?
         #   led_red.toggle(1)
     #   else:
          #  led_red.toggle(0)
            
  #  return temp


#humidity sensing function
#while True:
    #try:
       # utime.sleep(2)
       # hum = sensor.humidity()
    #except OSError as e:
       # print('failed to read sensor.')

while True: #response when connection is received
    conn, addr = s.accept()
    print('Have connection from %s' % str(addr))
    request = conn.recv(1024)
    
    temp = gettemp()				#get temp by calling function
    hum = gethum()					#get hum by calling function
    occ = getocc()					#get occ by calling function
    response = webpage(temp, hum, occ) 	#respond to call by loading webpage
    print('this runs')
    hum = gethum()
    print(hum)
    
    conn.send("HTTP/1.1 200 OK\n")
    conn.send("Content-Type: text/html\n")
    conn.send("Connection: close\n\n")
    conn.sendall(response)
    conn.close()
