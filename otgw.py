import socket
import sys
import textwrap
import paho.mqtt.client as mqtt

import threading

from vars import *
from time import sleep

mqtt_topic = "otgw_wmt6"

def on_connect(self, client, userdata, flags, rc):
    print("MQtt connected with result code "+ str(rc))

class MessageProcessor(threading.Thread):
    def __init__(self, sock, mqttClient):
        threading.Thread.__init__(self)
        self.name = "MessageProcessor"
        self.sock = sock
        self.mqttClient = mqttClient

    def run(self):
        try:
            fp = self.sock.makefile(mode='r', buffering=1)
            lines = 0

            while lines < 100000000:
                lines = lines + 1
                l = fp.readline(1024)
                l = l.rstrip()
                pp = self.parseLine(l)
                print('received ', lines, ' ', l, ' ', pp)
                self.mqttClient.publish(mqtt_topic + "/log", l)
                if pp[1] in [READ_ACK, WRITE_ACK]:
                    if pp[6] != '':
                        self.publish(pp[6], pp[5])
                    else:
                        print("work: " + pp[2])

        finally:
                print('closing socket')
                self.sock.close()

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
            cmdType, cmd, b1, b0 = textwrap.wrap(l[1:], 2)
            cmdType = self.getMsgType(int(cmdType, 16))
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

class GatewaySocket():

    def __init__(self):
        #threading.Thread.__init__(self)
        self.name = "GatewaySocket"
        self.sock = self.openConnction()
        self.startMqtt()

    def startProcessing(self):
        p = MessageProcessor(self.sock, self.mqttClient)
        p.start()

    def get_constants(self, prefix):
        """Create a dictionary mapping socket module
        constants to their names.
        """
        return {
            getattr(socket, n): n
            for n in dir(socket)
            if n.startswith(prefix)
        }

    def openConnction(self, ):
        families = self.get_constants('AF_')
        types = self.get_constants('SOCK_')
        protocols = self.get_constants('IPPROTO_')
        sock = socket.create_connection(("192.168.1.189", 6883))

        print('Family  :', families[sock.family])
        print('Type    :', types[sock.type])
        print('Protocol:', protocols[sock.proto])
        print()            
        sock.send(b'PS=0\r\n')
        return sock

    def startMqtt(self):
        client = mqtt.Client()
        client.on_connect = on_connect
        client.connect("192.168.1.169", 1883, 60)
        client.publish(mqtt_topic + "/log", "#Connected")
        self.mqttClient = client


otgw = GatewaySocket()
otgw.startProcessing()
print("socket read thread started")

#otgw.startProcessing()
