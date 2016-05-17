#!/usr/bin/python

'''Kafka Producer for publishing packets received from CC3200 over serial'''
import sys
import logging
import serial
from time import *
import datetime, string
import os
from pykafka import KafkaClient



uart = os.environ['UARTPATH']  #Set environment in docker
ser = serial.Serial(uart, 115200, timeout = 1)
hostip = os.environ['SERVERIP'] #Set environment in docker
client = KafkaClient(hosts=""+hostip+":9092")
datatopic = os.environ['TOPIC'] #Set environment in docker
topic = client.topics[datatopic]

client.update_cluster()

logging.basicConfig(stream=sys.stdout, level=logging.INFO)


# UART Read
# Publish async with kafka producer
# Consumer reads on the other end and timestamps while inserting into 
# Influx DB



def SendPacket(packet):
    '''Send Packet with sync producer'''
  # SEND PACKET if Valid
    with topic.get_sync_producer() as sync_producer:
        sync_producer.produce(packet)


producer = topic.get_producer(delivery_reports=False)


def SendAsync(packet):  
    '''Send Packet with Async producer'''
    logging.info("Sending Packet\n")
    producer.produce(packet)



packet = ""
first = True
#TODO: add reset board feature using signal.alarm
while True:
	try:
		data = ser.read(1)
		# packet += data

		if data == ']':
		    packet += data
		    SendAsync(packet)
		    packet = ""
		    first = True

		elif first:
		    packet += data
		    first = False
		else:
		    packet += data
		    first = True
	except (KeyboardInterrupt, SystemExit):
		# f.close()
		# Gracefully close serial conn and kill AsyncProd
		ser.close()
		logging.info('Interrupted')
		producer.stop() 
		sys.exit(0)





