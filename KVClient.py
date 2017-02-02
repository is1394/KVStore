import glob
import sys
import shlex

sys.path.insert(0,'gen-py')
sys.path.insert(0,glob.glob('thrift/lib/py/build/lib*')[0])

from KVServer import KVInterface
from KVServer.ttypes import KVMessage, KVException
from KVClientHandler import KVClientHandler
from KVUserInputException import KVUserInputException

from thrift import Thrift
from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol

class KVClient():
    client_handler = None

    def connect(self):
        self.client_handler = KVClientHandler()
        if len(sys.argv) == 1:
            print("Client try to connect to host:port by default: {}:{}".format(self.client_handler.host,self.client_handler.port))
        elif len(sys.argv) == 3:
            self.client_handler.input_host(sys.argv[1])
            self.client_handler.input_port(sys.argv[2])
        self.client_handler.work()

    def expr(self,text):
        input_elements = shlex.split(text)
        command = input_elements[0]
        if command.lower() == 'help':
            if len(input_elements) == 1:
                self.client_handler.help()
            else:
                raise KVUserInputException("Sorry invalid input, help doesn't recive arguments")
        elif command.lower() == 'ping':
            if len(input_elements) == 1:
                self.client_handler.ping()
            else:
                raise KVUserInputException("Sorry invalid input, ping doesn't recive arguments")
        elif command.lower() == 'exit':
            if len(input_elements) == 1:
                self.client_handler.exit()
            else:
                raise KVUserInputException("Sorry invalid input, exit doesn't recive arguments")
        elif command.lower() == 'get':
            if len(input_elements) == 1:
                raise KVUserInputException("Missing arguments, needs the key for the element to get")
            elif len(input_elements) == 2:
                value = self.client_handler.get(input_elements[1])
                print ("key:{}, value:{}".format(input_elements[1],value))
            elif len(input_elements) == 3:
                if input_elements[2] == '--xml':
                    print self.client_handler.get_xml(input_elements[1])
                elif input_elements[2] == '--json':
                    print self.client_handler.get_json(input_elements[1])
                elif input_elements[2] == '--yml':
                    print self.client_handler.get_yaml(input_elements[1])
                else:
                    raise KVUserInputException("Sorry invalid option, --xml --json --yml are valid options")
            else:
                raise KVUserInputException("Sorry invalid input, get only recive command key and options, try typing help for more information")
        elif command.lower() == 'set':
            if len(input_elements) == 1:
                raise KVUserInputException("Missing arguments, needs the key and value")
            elif len(input_elements) == 2:
                raise KVUserInputException("Missing arguments, needs the value for the input key")
            elif len(input_elements) == 3:
                self.client_handler.set(key = input_elements[1], value= input_elements[2])
            else:
                raise KVUserInputException("Sorry invalid input, set only recive command key and value, try typing help for more information")
        elif command.lower() == 'list':
            if len(input_elements) == 1:
                print self.client_handler.list()
            elif len(input_elements) == 2:
                if input_elements[1] == '--xml':
                    print self.client_handler.list_xml()
                elif input_elements[1] == '--json':
                    print self.client_handler.list_json()
                elif input_elements[1] == '--yml':
                    print self.client_handler.list_yaml()
                else:
                    raise KVUserInputException("Sorry invalid option, --xml --json --yml are valid options")
            else:
                raise KVUserInputException("Sorry invalid input, list only recive command and options, try typing help for more information")
        elif command.lower() == 'del':
            if len(input_elements) == 1:
                raise KVUserInputException("Missing arguments, needs the key for the element to delete")
            elif len(input_elements) == 2:
                result = self.client_handler.delete(key = input_elements[1])
                if result == True:
                    print("Element Delete")
                else:
                    print("Something wrong, element doesn't delete")
            else:
                raise KVUserInputException("Sorry invalid input, del only recive command and key, try typing help for more information")
        else:
            raise KVUserInputException(" Sorry invalid input, try typing help for more information")




if __name__ == '__main__':
    try:
        Client = KVClient()
        Client.connect()
        while True:
            try:
                text = raw_input('KVClient> ')
            except EOFError:
                break
            if not text:
                continue
            try:
                operation  = Client.expr(text)
            except KVUserInputException as kvue:
                print("ERROR: {}".format(kvue.message))
            except KVException as kve:
                print("ERROR: {}".format(kve.why))
    except Thrift.TException as tx:
        print("Error: {}".format(tx.message))
        sys.exit(0)
