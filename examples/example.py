#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This is an SDK that allows you to connect to the AWS IoT Platform using python.
Copyright (c) 2015 Lyndon James Swan

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""
__author__ = 'Monkee Magic <magic.monkee.magic@gmail.com>'
__version__ = '2.0.1'

"""
The purpose of this script is to subscribe to the virdata topic and setup the RFID reader

It is meant to be daemonized - it will exit and respawn on error

"""
#################vvvvvvvvvv
# IMPORTS
#################----------
import serial
from grovepi import *
from aws_iot_sdk import AWSIoTSDK
import json
import daemon
import daemon.pidlockfile
###############^^^^^^^^^^^^^^^

################vvvvvvvvvvvvv
################vvvvvvvvvvvv
# GLOBALS
###############-------------
client_id = 'phillipatheplant'
topic_subscribe = '$aws/things/phillipatheplant/shadow/update/accepted'
topic_publish = "$aws/things/phillipatheplant/shadow/update/"
mqtthost = "AFT2R5GDIHWIB.iot.us-east-1.amazonaws.com"
mqttport = 8883
rootca ="/opt/ptp/Root-CA.pem"
privatekey ="/opt/ptp/760dde32cd-private.pem.key"
cert="/opt/ptp/760dde32cd-certificate.pem.crt"

#################^^^^^^^^^^^
################^^^^^^^^^^^^^

##################################vvvvvvvvv
# NON IMPORT CLASSES
##################################---------

    pass

def connected():
    aws.subscribe(topic_subscribe, qos=1)
    print("connected")

def all_off():
    pinMode(led1,"OUTPUT")
    pinMode(led2,"OUTPUT")
    pinMode(led3,"OUTPUT")

    #send a reset
    digitalWrite(led1,1)             # Send HIGH to switch on LED
    digitalWrite(led2,1)             # Send HIGH to switch on LED
    digitalWrite(led3,1)             # Send HIGH to switch on LED

def on_connect(client, userdata, flags, rc):
    #setText("CONNACK\n" + str(rc))
    #setRGB(200,200,200)
    connected()

def on_message(client, userdata, message):
    #('payload', ': ', '{"state":{"desired":{"state":"Fire"},"reported":{}},"metadata":{"desired":{"state":{"timestamp":1444885012}},"reported":{}},"version":34,"timestamp":1444885012}')
    jason = json.loads(message.payload)
    global state
    state = jason['state']['desired']['state']
    if state == "Alert":
        alert()
    elif state == "OK":
        ok()
    elif state == "Clear":
        clear()
    elif state == "Fire":
        event()
    else:
        ok()

def on_publish(client, userdata, mid):
    pass

def on_log(client, obj, level, string):
    pass

def on_subscribe(client, obj, level, string):
    pass

def on_disconnect(client, userdata, rc):
    #setText("DISCONNECT\n" + str(rc))
    #setRGB(200,200,200)
    pass

def switcher():
    global state
    for case in switch(state):
        if case("Fire"):
            state = "Alert"
            break
        if case("Alert"):
            state = "Clear"
            break
        if case("Clear"):
            state = "OK"
            break
        if case("OK"): pass
        if case():
            state = "Fire"
############################################################^^^^^^^^


##################vvvvvvvvvv
# BEGIN
##################----------
startup()
#################^^^^^^^^^^^


###################vvvvvvvvvv
# RESET LIGHTS and Stuff
all_off()
##################^^^^^^^^^^^

##################vvvvvvvvvvv
# PLATFORM CONNECT
##################-----------
aws = AWSCoreLib()
#connectToBroker(self, client_id, private_key, certificate_key, mqtthost, mqttport=8883, userdata=None, CACert="Root-CA.pem"):
aws.connectToBroker(client_id, privatekey, cert, mqtthost)
###################^^^^^^^^^^^

################vvvvvvvvvvvvv
# SUBSCRIBE
# this is important so we know what the device is on boot
aws.subscribe(topic_subscribe, qos=1)
################^^^^^^^^^^^^^^

##################vvvvvvvvvvvvv
# CALLBACK CITY
client = aws.exposeClient()
#################--------------
client.on_connect = on_connect
client.on_disconnect = on_disconnect
client.on_message = on_message
client.on_message = on_subscribe
client.on_publish = on_publish
client.on_log = on_log
################^^^^^^^^^^^^^^^^^

##################vvvvvvvvvvv
# NETWORK THREAD LOOP - to background
##################----------
aws.unblockedStart()
#################^^^^^^^^^^^^

####DEOMON
pidfile = daemon.pidlockfile.PIDLockFile("/var/run/ptp.pid")
with daemon.DaemonContext(pidfile=pidfile):
    ###################vvvvvvvvvvv
    # RFID SERIAL READER and MAIN THREAD
    ###################-----------
    ser = serial.Serial('/dev/ttyAMA0', 9600, timeout=rfid_timing_sensitivity)
    ##################------------
    while True:
        #### READ FOB
        fob = ser.readline()
        ###### ignore blank reads
        if fob == "":
            cardint =""
        else:
            card = fob[3:-3]
            try:
                cardint = int(card, 16)
            except:
                cardint = ""

        ###### OK crappy check fobs for action
        secure = False
        for case in switch(cardint):
            if case(867302): pass
            if case(758082): pass
            if case(3993708):
                secure = True
                #setText("AUTHORISED:\n" + str(cardint))
                #setRGB(255,255,255)
                break
            if case(): # default
                continue
        if secure is True:
            reported = state
            switcher()
            aws.publish(topic_publish, payload='{"desired": {"state": "' + state + '"},"reported": {"state": "' + reported + '"}}', qos=1)

    ###################^^^^^^^^^^^^^^^^^

ser = serial.Serial('/dev/ttyAMA0', 9600, timeout=rfid_timing_sensitivity)
##################------------
while True:
    #### READ FOB
    fob = ser.readline()
    ###### ignore blank reads
    #print("read",fob)
    if fob == "":
        cardint =""
    else:
        card = fob[3:-3]
        try:
            cardint = int(card, 16)
        except:
            cardint = ""

    ###### OK crappy check fobs for action
    secure = False
    for case in switch(cardint):
        if case(867302): pass
        if case(758082): pass
        if case(3993708):
            secure = True
            #setText("AUTHORISED:\n" + str(cardint))
            #setRGB(255,255,255)
            break
        if case(): # default
            continue
    if secure is True:
        reported = state
        switcher()
        #print(reported,state)
    aws.publish(topic_publish, payload='{"state":{"desired": {"state": "' + state + '"},"reported": {"state": "' + reported + '"}}}', qos=1)