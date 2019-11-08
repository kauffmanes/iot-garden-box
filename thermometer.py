import glob
import time
from datetime import datetime, timedelta
import RPi.GPIO as GPIO
import requests

GPIO.setmode(GPIO.BOARD)

# set pins of each lamp
lamp1 = 21 # top left white
lamp2 = 19 # front bottom white
lamp3 = 15 # bottom red
lamp4 = 13 # top red

GPIO.setup(lamp1, GPIO.OUT)
GPIO.output(lamp1, GPIO.HIGH)

GPIO.setup(lamp2, GPIO.OUT)
GPIO.output(lamp2, GPIO.HIGH)

GPIO.setup(lamp3, GPIO.OUT)
GPIO.output(lamp3, GPIO.HIGH)

GPIO.setup(lamp4, GPIO.OUT)
GPIO.output(lamp4, GPIO.HIGH)

base_dir = '/sys/bus/w1/devices/'
device_folder = glob.glob(base_dir + '28*')[0]
device_file = device_folder + '/w1_slave'

LOW_THRESHOLD = 60

# reads the raw data from the probe
def read_temp_raw():
    f = open(device_file, 'r')
    lines = f.readlines()
    f.close()
    return lines
 
# outputs Celcius and Fahrenheit values
def read_temp():
    lines = read_temp_raw()
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = read_temp_raw()
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        temp_string = lines[1][equals_pos+2:]
        temp_c = float(temp_string) / 1000.0
        temp_f = temp_c * 9.0 / 5.0 + 32.0
        # return temp_c, temp_f
        return temp_f

def get_day_data():
    response = requests.get('https://api.sunrise-sunset.org/json?lat=40.442169&lng=-79.994957')
    parsed = response.json()
    #print(parsed)
    return parsed['results']

def get_today():
    return datetime.strptime('01/08/2015','%d/%m/%Y').date()

day_length = None
solar_noon = None

today = get_today()

try:
    while True:

        # if the day has changed or the day length isn't set (first run)
         #if get_today() != today or day_length is None:
          #  today = get_today()
           # day_data = get_day_data()
            #print(day_data)
            #day_length = day_data['day_length']
            #solar_noon = datetime.strptime(day_data['solar_noon'], '%H:%M:%S %p')
            
            #print(day_length)
            #print(solar_noon)

        # if the time that there's daylight is less than 12 hours, and it's3
        # between the end of the day and two hours after, 
        # turn on the lights for that time difference
       # now = datetime.now()
        
        #if 12 - day_length > 0 and (now > solar_noon) and now < solar_noon + timedelta(hours=2):

            # turn on the lights 2 hours after the daylight ends for extra light
         #   GPIO.output(lamp1, GPIO.LOW)
          #  GPIO.output(lamp2, GPIO.LOW)

        curr_temp = read_temp() 
        print(curr_temp)
        
        if curr_temp < LOW_THRESHOLD:
            #GPIO.output(lamp1, GPIO.LOW) 
            #GPIO.output(lamp2, GPIO.LOW)
            GPIO.output(lamp3, GPIO.LOW)
            GPIO.output(lamp4, GPIO.LOW)
        else:
            #GPIO.output(lamp1, GPIO.HIGH)
            #GPIO.output(lamp2, GPIO.HIGH)
            GPIO.output(lamp3, GPIO.HIGH)
            GPIO.output(lamp4, GPIO.HIGH)
        time.sleep(1)


except KeyboardInterrupt:
    print("Quitter")
    GPIO.cleanup()
