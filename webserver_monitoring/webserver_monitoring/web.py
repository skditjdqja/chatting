import sys, socket, io


HOST, PORT = '', 8182 # 호스트와 포트를 정의한다.
# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # IPv4 방식의 소켓 생성
#sock.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
# Bind the socket to the port
sock.bind((HOST,PORT)) # 소켓의 주소와 포트 지정
sock.listen(1000) # 1000개의 연결 허용
print 'starting up on port %s' % PORT
# Listen for incoming connections

while True: # 무한 루프를 통해 계속 수행한다.
    	# Wait for a connection
    	connection, client_address = sock.accept() # accept 함수를 통해 연결을 승인한다.
        data = connection.recv(1024) # 1024의 버퍼로 소켓으로부터 들어오는 데이터를 수신한다.
	#print data   
	filename = data.split() # split 함수를 통해 data의 내용을 단어 단위로 쪼갠다.
	#print nama file di terminal
	file1 =filename[1] # file 1은 첫 단어이고 	
	file2 =file1[1:] # file 2는  file1의 인덱싱 1부터 마지막까지를 의미한다.
	print file2 # file2의 내용을 출력한다.
        #baca nama file dri browser
	#f= open(file2+".jpg",'r+')
	#imgdata2 = f.read()
	imgdata2 = 'Yes' # imgdata2의 내용은 Yes 라는 문자열이다.
	#f.close()
	http_response = "\HTTP/1.1 200 OK \n\n%s"%imgdata2 # 문자열이다.

        # Clean up the connection
	connection.sendall(http_response) # 연결로 http_response를 보낸다.
	connection.close() # 연결을 종료한다.
