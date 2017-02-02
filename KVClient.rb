$:.push('gen-rb')
$:.unshift 'thrift/lib/rb/lib'

require 'thrift'

require 'k_v_interface'

begin
  port = ARGV[0] || 8000

  transport = Thrift::BufferedTransport.new(Thrift::Socket.new('localhost', port))
  protocol = Thrift::BinaryProtocol.new(transport)
  client = KVInterface::Client.new(protocol)

  transport.open()

  client.ping()

  client.set_element('pruebita','ruby')

  result = client.list_elements()
  puts result

  transport.close()

rescue Thrift::Exception => tx
  print 'Thrift::Exception: ', tx.message, "\n"
end
