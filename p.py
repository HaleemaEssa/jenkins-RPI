import RPi.GPIO as GPIO
import time
import pika
import random
import os
####Sound Sensor ###
import adafruit_dht
from board import *
channel1 = 6 #for sound
GPIO.setmode(GPIO.BCM)  
GPIO.setup(channel1, GPIO.IN)
credentials = pika.PlainCredentials('haleema', '4chyst')
parameters = pika.ConnectionParameters('192.168.0.126',
                                   5672,
                                   '/',
                                   credentials)

connection = pika.BlockingConnection(parameters)

channel = connection.channel()

channel.exchange_declare(exchange='logs', exchange_type='fanout')

def callback1(channel1):
    if GPIO.input(channel1):
        return('0')
    else:
        return('1')
    return sound    #
    sound=0
GPIO.add_event_detect(channel1, GPIO.BOTH, bouncetime=300)  # let us know when the pin goes HIGH or LOW
GPIO.add_event_callback(channel1, callback1)  # assign function to GPIO PIN, Run function on change
def checkdht():
    for i in range(10):
        try:
            sound=callback1(channel1)
            message=str(sound)
            channel.basic_publish(exchange='logs', routing_key='', body= message)
            print ("sent %r" %message) 

        except RuntimeError:
            pass
        time.sleep(5)

while True:
    checkdht()

connection.close()
