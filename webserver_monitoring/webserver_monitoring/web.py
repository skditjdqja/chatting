import sys, socket, io


HOST, PORT = '', 8182 # ȣ��Ʈ�� ��Ʈ�� �����Ѵ�.
# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # IPv4 ����� ���� ����
#sock.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
# Bind the socket to the port
sock.bind((HOST,PORT)) # ������ �ּҿ� ��Ʈ ����
sock.listen(1000) # 1000���� ���� ���
print 'starting up on port %s' % PORT
# Listen for incoming connections

while True: # ���� ������ ���� ��� �����Ѵ�.
    	# Wait for a connection
    	connection, client_address = sock.accept() # accept �Լ��� ���� ������ �����Ѵ�.
        data = connection.recv(1024) # 1024�� ���۷� �������κ��� ������ �����͸� �����Ѵ�.
	#print data   
	filename = data.split() # split �Լ��� ���� data�� ������ �ܾ� ������ �ɰ���.
	#print nama file di terminal
	file1 =filename[1] # file 1�� ù �ܾ��̰� 	
	file2 =file1[1:] # file 2��  file1�� �ε��� 1���� ������������ �ǹ��Ѵ�.
	print file2 # file2�� ������ ����Ѵ�.
        #baca nama file dri browser
	#f= open(file2+".jpg",'r+')
	#imgdata2 = f.read()
	imgdata2 = 'Yes' # imgdata2�� ������ Yes ��� ���ڿ��̴�.
	#f.close()
	http_response = "\HTTP/1.1 200 OK \n\n%s"%imgdata2 # ���ڿ��̴�.

        # Clean up the connection
	connection.sendall(http_response) # ����� http_response�� ������.
	connection.close() # ������ �����Ѵ�.
