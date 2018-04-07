
# Import necessary libraries for commuunication and display use

import time
import Adafruit_DHT
import pyrebase
from gpiozero import LED
import RPi.GPIO as GPIO
import re


config = {
    "apiKey": "AIzaSyD03IMGuSv8LLBKvStkOJJm6cath-yTbKg",
    "authDomain": "model-2.firebaseapp.com",
    "databaseURL": "https://model-2.firebaseio.com",
    "storageBucket": "model-2.appspot.com",
    
  }
# GPIO config:
# GPIO10 is configured for de opening and closing water motor

GPIOWater= LED(10)


firebase = pyrebase.initialize_app(config)
db = firebase.database()

# Sensor should be set to Adafruit_DHT.DHT11,
# Adafruit_DHT.DHT22, or Adafruit_DHT.AM2302.

sensor = Adafruit_DHT.DHT22


# Example using a Raspberry Pi with DHT sensor
# connected to GPIO4

pin = 4

# Counter to store every minute the values

count = 0

# Control water level sensor:

pinwater = 17
GPIO.setup(pinwater, GPIO.IN)

def callback(pinwater):
    if GPIO.input(pinwater):
        print("No water detected")
    else:
        print("Water detected")

GPIO.add_event_detect(pinwater, GPIO.BOTH, bouncetime= 600)
GPIO.add_event_callback(pinwater,callback)




# Main body of code

try:
    while True:
        
        #Start firebase
        
        OpenWater = db.child("TReal").child("values").child("open").get()
        hour = time.strftime("%H:%M:%S")
        date = time.strftime("%x")
        secods = time.strftime("%S")
        day = time.strftime("%A")
        hora = time.strftime('%H')

        
        
        #If OPenWater is true open the water pump
        
        if OpenWater.val():
            GPIOWater.on()
            print("Motor Pump is Open")
        else:
            GPIOWater.off()
            print("Motor Pump is Close")
        
          
        # Try to grab a sensor reading.  Use the read_retry method which will retry up
        # to 15 times to get a sensor reading (waiting 2 seconds between each retry).

        humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
        humidity = round(humidity, 1)
        temperature = round(temperature, 1)

        # Note that sometimes you won't get a reading and
        # the results will be null (because Linux can't
        # guarantee the timing of calls to read the sensor).
        # If this happens try again!

        if humidity is not None and temperature is not None:

            print('Temp={0:0.1f}*C  Humidity={1:0.1f}%'.format(temperature, humidity))

            # Update Firebase

            dato ={"temperature":temperature,"humidity":humidity, "time":hour,"day":hora + day}
            db.child("TReal/values").update(dato)
            if (count == 60):

                db.child("values").push(dato)
                count = 0
                
            print( temperature)
            print(humidity)
            print(date, hour)
            count = count +1
              

            
               
        else:
            print('Failed to get reading. Try again!')

        print(day)
        print(hour)
        name = hora + day
        print(name)
        Temp = []
        Hum = []
        # (day == "Thursday") and
        if  re.match("..:00:2.",hour):

            all_dates = db.child("values").get()

            print(all_dates)

            for value in all_dates.each():

                obj = value.val()
                print(int(obj["temperature"]))
                Temp.append(int(obj["temperature"]))
                Hum.append(int(obj["humidity"]))
                
            # Update Firebase
            
            dato ={"HMax":max(Hum),"HMin":min(Hum),"TMax":max(Temp),"TMim":min(Temp),"Name":name, "Picture": name}
            db.child("Videos").push(dato)
               
            print("Tmperatura max",max(Temp))
            print("Tmperatura min",min(Temp))
            time.sleep(8)
            
             

        time.sleep(1)


       
except KeyboardInterrupt: # If there is a KeyboardInterrupt (when you press ctrl+c), exit the program and cleanup
    print("Cleaning up!")
   
