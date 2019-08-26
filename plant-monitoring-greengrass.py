import RPi.GPIO as GPIO
import dht11
import time
import datetime
import ADC0832
#Greengrass core
import greengrasssdk
import platform
import json
from threading import Timer

# Creating a greengrass core sdk client
client = greengrasssdk.client('iot-data')

my_platform = platform.platform()

# initialize GPIO
def init():
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BOARD)
    GPIO.cleanup()
    ADC0832.setup()

# read data using pin 12
instance = dht11.DHT11(pin=16)


# This is a dummy handler and will not be invoked
# Instead the code above will be executed in an infinite loop for our example
def function_handler(event, context):
    return


def monitor_loop():
    result_TeHu = instance.read()
    result_Moi = ADC0832.getResult()
    moisture = 255 - result_Moi
    
    #if result_TeHu.is_valid():
    #    print("Time Stamp: " + str(datetime.datetime.now()))
    #    print("Temperature: %d C" % result_TeHu.temperature)
    #    print("Humidity: %d %%" % result_TeHu.humidity) 
    #    print("Moisture: %d " % moisture)
    client.publish(
                    topic='monitor/input',
                    payload=json.dumps({'message': 'Sent from Greengrass Core running on platform: {}. Temperature: {} C Humidity: {} percent Moisture: {}'.format(my_platform,result_TeHu.temperature,result_TeHu.humidity,moisture )})
                    )
    Timer(5, monitor_loop).start()

init()
monitor_loop()
