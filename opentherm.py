import socket
import sys
import textwrap
import paho.mqtt.client as mqtt

from vars import *
mqtt_topic = "otgw_wmt6"

def on_connect(self, client, userdata, flags, rc):
    print("MQtt connected with result code "+ str(rc))

MQTT_HOST = "192.168.1.169"
MQTT_PORT = 1883

class MessageProcessor():
    def __init__(self):
        client = mqtt.Client()
        client.on_connect = on_connect
        client.connect(MQTT_HOST, MQTT_PORT, 60)
        client.publish(mqtt_topic + "/log", "#Connected")
        self.mqttClient = client

    def processLine(self, line):
        l = line.rstrip()
        pp = self.parseLine(l)
        print('received ', l, ' ', pp)
        self.mqttClient.publish(mqtt_topic + "/log", l)

        if pp[1] in [READ_ACK, WRITE_ACK]:
            if pp[6] != '':
                self.publish(pp[6], pp[5])
            else:
                print("work: " + pp[2])

    def publish(self, topic, message):
        if not isinstance(message, list):
            self.mqttClient.publish(mqtt_topic + "/stream/" + topic, message)
        else:
            #print("message = {0}".format(message))
            message.reverse()
            idx = 0
            for v in message:
                tt = "{0}_{1}".format(topic, idx)
                #print("pub {0} {1}".format(tt, v))
                idx = idx + 1
                self.mqttClient.publish(mqtt_topic + "/stream/" + tt, v)

    def getMsgType(self, b):
        return (b >> 4) & 0x7

    def parseLine(self, l):
        lineType = l[0]
        if lineType in ['T', 'B', 'A']:
            #print('parse line ', l)
            cmdTypeTmp, cmd, b1, b0 = textwrap.wrap(l[1:], 2)
            cmdType = self.getMsgType(int(cmdTypeTmp, 16))
            cmd = int(cmd, 16)
            
            val = ''
            topic = ''
            if cmd in data_id.keys():
                idInfo = data_id[cmd]
                cmd = idInfo[0]
                if len(idInfo) > 2:
                    val = idInfo[2](b1, b0)
                    #print ('has formatter ', val)
                if len(idInfo) > 3:
                    topic = idInfo[3]
            else:
                cmd = "unknown {0}".format(cmd)
            return (lineType, cmdType, cmd, b1, b0, val, topic)
        else:
            print('other ', l)
            return ('O', l)
