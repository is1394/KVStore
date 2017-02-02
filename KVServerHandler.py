import glob
import sys

sys.path.insert(0,'gen-py')
# sys.path.insert(0,glob.glob('thrift/lib/py/build/lib*')[0])

from KVServer import KVInterface
from KVServer.ttypes import KVMessage, KVException, KVCollection

from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol
from thrift.server import TServer


class KVServerHandler:
    def __init__(self):
        self.collection = KVCollection([])

    def ping(self):
        print("PING")

    def del_element(self,key):
        try:
            for kvmessage in self.collection.elements:
                if kvmessage.value.has_key(key):
                    value = kvmessage.value.get(key)
                    self.collection.elements.remove(kvmessage)
                    print("DEL - Element deleted Key:{},Value:{}".format(key,value))
                    return True
        except:
            return False
            raise KVException(why="Something wrong, Element not found :(")

    def set_element(self, key, value):
        try:
            new_element = KVMessage({key:value})
            for kvmessage in self.collection.elements:
                if kvmessage.value.has_key(key):
                    raise KVException(why="Element doesn't create, Key already exists")
            self.collection.elements.append(new_element)
            print("SET - New element created Key:{},Value:{}".format(key,value))
            return new_element
        except KVException:
            raise KVException(why="Element doesn't create, Key already exists")
        except Exception:
            raise KVException(why="Something wrong, Element doesn't create")

    def get_element(self,key):
        try:
            for kvmessage in self.collection.elements:
                if kvmessage.value.has_key(key):
                    value = kvmessage.value.get(key)
            if value:
                print("GET - Get element Key:{},Value:{}".format(key,value))
                return value
            else:
                raise KVException(why="Something wrong, Element doesn't exist")
        except KVException:
            raise KVException(why="Something wrong, Element doesn't exist")
        except:
            raise KVException(why="Something wrong, Element not found :(")

    def list_elements(self):
        key_list = []
        for element in self.collection.elements:
            value = element.value.keys()[0]
            key_list.append(value)
        print("LIST - List Elements")
        return key_list
