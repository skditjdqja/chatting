import sys, socket

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.setsockopt(socket.SQL_SOCKET, socket.SO_REUSEADDR,1)

# Bind the socket to the port
server_address = ('', 8888)
print >>sys.stderr, 'starting up on %s port %s' % server_address
sock.bind(server_address)

# Listen for incoming connections
sock.listen(1)

while True:
    	# Wait for a connection
    	print >>sys.stderr, 'waiting for a connection'
    	connection, client_address = sock.accept()
    	print >>sys.stderr, 'connection from', client_address
    	# Receive the data in small chunks and retransmit it
    	# while True:
        	data = connection.recv(1024)
        	print data
        	http_response = """\HTTP/1.1 200 \nOK"""
        	
        	#print >>sys.stderr, 'received "%s"' % data
            	#if data:
                #	print >>sys.stderr, 'sending data back to the client'
                #	connection.sendall(data)
            	#else:
                #	print >>sys.stderr, 'no more data from', client_address
                #	break

        # Clean up the connection
        connection.sendall(http_response)
	connection.close()

#TCP/IP 소켓을 생성하고
#생성된 소캣을 포트에 결합시킨다. 이때 포트번호는 8888이다.
#데이터 통신을 위해 항상 Listening을 하여 기다린다.
#클라이언트 주소와 소켓허용이 일치해야 통신이 가능하다.
#데이터는 1024크기를 받으며 받을 경우 출력을 하고 HTTP응답코드 200으로 한다.
#연결이 끝난 후 close 한다.