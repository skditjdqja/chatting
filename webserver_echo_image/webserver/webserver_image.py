import sys, socket, io



HOST, PORT = '', 8888
# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
# Bind the socket to the port
sock.bind((HOST,PORT))
sock.listen(1)
print 'starting up on port %s' % PORT
# Listen for incoming connections
#여기까지가 소켓프로그래밍 준비

while True:
    	# Wait for a connection
    	connection, client_address = sock.accept() 
        data = connection.recv(1024) #데이터를 받고
	#print data   
	filename = data.split() #받은데이터를 공백기준으로 나눔.
	#print nama file di terminal
	file1 =filename[1]
	file2 =file1[1:]
	print file2
        #baca nama file dri browser
	f= open(file2+".jpg",'r+') #읽기, 쓰기모드로 jpg파일을 열음
	jpgdata2 = f.read() #데이터를 jpgdata2에 저장
	f.close()
	http_response = "\HTTP/1.1 200 OK \n\n%s"%jpgdata2

        # Clean up the connection
	connection.sendall(http_response)
	connection.close()
