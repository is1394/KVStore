# -*- coding: utf-8 -*-
import glob
import sys

sys.path.insert(0,'gen-py')
# sys.path.insert(0,glob.glob('thrift/lib/py/build/lib*')[0])

from KVUserInputException import KVUserInputException
from KVServerHandler import KVServerHandler
from KVServer import KVInterface
from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol
from thrift.server import TServer

class KVServer():
    __label = "Single Server Key-Value Store"
    __port = 9000

    def input_port(self,port):
        if port.isdigit() == True:
            self.__port = int(port)
            print("Server listening in the port {}".format(self.__port))
        else:
            print("Invalid port")
            sys.exit(0)

    def serve(self):
        print(self.__label)

        if len(sys.argv) == 1:
            print("Server Listening in the default port {}".format(self.__port))
        elif len(sys.argv) == 2:
            self.input_port(sys.argv[1])

        handler = KVServerHandler()
        processor = KVInterface.Processor(handler)
        self.transport = TSocket.TServerSocket(port=self.__port)
        tfactory = TTransport.TBufferedTransportFactory()
        pfactory = TBinaryProtocol.TBinaryProtocolFactory()

        self.server = TServer.TThreadPoolServer(processor, self.transport, tfactory, pfactory)
        self.server.setNumThreads(2)
        print('Starting the server...')
        self.server.serve()

    def stop(self):
        self.transport.close()
        print('done.')


if __name__ == '__main__':
    server =  KVServer()
    try:
        server.serve()
    except KeyboardInterrupt:
        print("Exit")
    finally:
        server.stop()
        sys.exit(0)
