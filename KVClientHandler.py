import glob
import sys
import socket
import json
import yaml
from xml.etree.ElementTree import Element, SubElement
from xml.etree import ElementTree
from xml.dom import minidom



sys.path.insert(0,'gen-py')
sys.path.insert(0,glob.glob('thrift/lib/py/build/lib*')[0])


from KVServer import KVInterface
from KVServer.ttypes import KVMessage, KVException

from thrift import Thrift
from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol

class KVClientHandler():
    port = 9000
    host = 'localhost'
    __label = "Key-Value Store Client"
    client = None
    def __init__(self):
        print(self.__label)

    def input_port(self,port):
        if port.isdigit() == True:
            self.port = int(port)
            print("Client try to use port {}".format(self.port))
        else:
            print("Invalid port")
            sys.exit(0)

    def input_host(self,host):
        try:
            socket.inet_aton(host)
            socket_answer = True
        except:
            socket_answer = False

        if host == 'localhost':
            print("Client try to connect to {}".format(self.host))
        elif socket_answer:
            self.host = host
            print("Client try to connect to {}".format(self.host))
        else:
            print("Invalid host")
            sys.exit(0)

    def work(self):
        # Make socket
        self.transport = TSocket.TSocket(self.host,self.port)

        # Buffering is critical. Raw sockets are very slow
        self.transport = TTransport.TBufferedTransport(self.transport)

        # Wrap in a protocol
        self.protocol = TBinaryProtocol.TBinaryProtocol(self.transport)

        # Create a client to use the protocol encoder
        self.client = KVInterface.Client(self.protocol)

        # Connect!
        self.transport.open()

    def ping(self):
        self.client.ping()
        print("ping()")

    def exit(self):
        self.transport.close()
        print("Exit Client, Good Bye")
        sys.exit(0)

    def help(self):
        print('')
        print('Usage {}'.format(self.__label))
        print('')
        print('Functions')
        print('help : List the commands support by the client')
        print('ping : Make a ping to server')
        print('get <key> [OPTIONS] : Returns the value associated with that key')
        print('set <key, value> : Store the key with the associated value ')
        print('del <key> : Delete the key with the associated value')
        print('list [OPTIONS] : Returns the list of all stored keys. NO returns the values associated with those keys.')
        print('exit: Terminates the connection to the server and terminates client execution.')
        print('[OPTIONS]:')
        print('\t --xml: returns the data in xml format')
        print('\t --json: returns the data in json format')
        print('\t --yml: returns the data in yaml format')
        print('')

    def list(self):
        return self.client.list_elements()

    def list_xml(self):
        keys = Element('keys')
        elements = self.client.list_elements()
        for element in elements:
            child = SubElement(keys,'key')
            child.text = element
        rough_string = ElementTree.tostring(keys, 'utf-8')
        reparsed = minidom.parseString(rough_string)
        return reparsed.toprettyxml(indent="  ")


    def list_json(self):
        elements = self.client.list_elements()
        return json.dumps({'keys':elements})

    def list_yaml(self):
        elements = self.client.list_elements()
        return yaml.dump({'keys': elements}, default_flow_style=False)

    def set(self, key, value):
        # validate here
        self.client.set_element(key = key,value = value)

    def get(self,key):
        return self.client.get_element(key = key)

    def get_xml(self,key):
        value = self.client.get_element(key= key)
        kvmessage = Element('KVMessage')
        keyxml = SubElement(kvmessage,'key')
        keyxml.text= key
        valuexml = SubElement(kvmessage,'value')
        valuexml.text= value
        rough_string = ElementTree.tostring(kvmessage, 'utf-8')
        reparsed = minidom.parseString(rough_string)
        return reparsed.toprettyxml(indent="  ")

    def get_json(self,key):
        value = self.client.get_element(key= key)
        return json.dumps({'KVMessage':{'value':value,'key':key}})

    def get_yaml(self,key):
        value = self.client.get_element(key= key)
        return yaml.dump({'KVMessage':{'key':key,'value':value}}, default_flow_style=False)

    def delete(self,key):
        return self.client.del_element(key= key)
