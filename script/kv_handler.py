#!/usr/bin/python
# -*- coding: iso-8859-15 -*-

import logging
import sys, serial
from time import *
import datetime, string
import os
import consul


# kv_handler

def enum(**enums):
    return type('Enum', (), enums)

Status = enum(ERR='ERROR', OK=['OK', 'ready', 'no change'], BUSY='busy')
logging.basicConfig(stream=sys.stdout, level=logging.INFO)
mac = os.environ['MAC']

c = consul.Consul()

# modified code from: http://www.instructables.com/id/Easy-ESP8266-WiFi-Debugging-with-Python/step2/Software/
def send_cmd( sCmd, waitTm=2, retry=2 ):
	lp = 0
	ret = ""

	logging.info( "Sending command: %s" % sCmd )

	for i in range(retry):
		ser.flushInput()
		ser.write( sCmd + "\n" )
		ret = ser.readline()	# Eat echo of command.
		sleep( 0.2 )
		while( lp < waitTm or 'busy' in ret):
			if( ser.inWaiting() ):
				ret = ser.readline().strip( "\r\n" )
				logging.debug( ret )
				#lp = 0
			if( ret in Status.OK ): break
			# if( ret == 'ready' ): break
			if( ret == Status.ERR ): break
			sleep( 1 )
			lp += 1

		sleep(1)
		if( ret in Status.OK ): break

	logging.info( "Command result: %s" % ret )
	return ret

port = os.environ['UARTPATH']
#Baud rate should be: 9600 or 115200
speed = 115200

index, status = c.kv.get('status/all')
i, value = c.kv.get("status/"+mac+"")

indexint, intvl = c.kv.get('interval')
# check if the parameter is set
if intvl['Flags'] == 1 :
	os.system('stop kafka.py')
	ser = serial.Serial(port,speed, timeout = 1) # add timeout to make sure that error will return when nodes are dead
	if ser.isOpen():
	    ser.close()
	ser.open()
	ser.isOpen()
	
	send_cmd( "CFG" )
	num = intvl['Value']
	 # Deal with configurations
	if( 'OK' in send_cmd( "CFG+INTVL="+num+"") ):
		response = c.kv.put("status/"+mac+"", 'OK')
		logging.info(response)
		response = c.kv.put("status/all", 'PENDING')
		logging.info(response)
		response = c.kv.put("interval", num) 
		logging.info(response)
	else:
		logging.info( "update Consul K/V for channel failed." )
		response = c.kv.put("status/"+mac+"", 'ERROR')
		logging.info(response)
		response = c.kv.put("status/all", 'PENDING')
		logging.info(response)
	ser.close()


# Restart the concentrator
if (status['Flags'] == 1 and value['Flags'] != 1):
	ser = serial.Serial(port,speed, timeout = 1) # add timeout to make sure that error will return when nodes are dead
	if ser.isOpen():
	    ser.close()
	ser.open()
	ser.isOpen()

	if( 'OK' in send_cmd( "RESTART") ): 
		ser.close()
		logging.info( "update Consul K/V Status" )
		response = c.kv.put("status/"+mac+"", 'RUNNING', flags=1)
		logging.info(response)
		os.system('start /root/kafka.py')
	else:
		logging.info( "Restart failed." )
		response = c.kv.put("status/"+mac+"", 'ERROR')
		logging.info(response)
	ser.close()

