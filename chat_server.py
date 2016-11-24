import sys, socket, select, string

HOST = 'localhost' 
SOCKET_LIST = []
NAME_LIST = []
RECV_BUFFER = 4096 
PORT = 11000


def chat_server():

	#creating TCP/IP socket
	server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # IPv4 ���ͳ� ������������ ���� ����
	server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) #���� �������� �̹� ���� �ּҸ� ���� (bind) �ϵ��� �Ѵ�.

	# binding the socket (available for 10)
	server_socket.bind((HOST, PORT)) # ���Ͽ� �ּҿ� ��Ʈ�� �����Ѵ�.
	server_socket.listen(10) # ����� �� �ִ� ������ 10���� ����

	# add server socket object to the list of readable connections
	SOCKET_LIST.append(server_socket) # ���� �� �ִ� ������ ��� �ִ� SOCKET_LIST �迭�� ���� ���� ������Ʈ�� �߰��Ѵ�.

	print "The chat server is started on Port " + str(PORT)
        print "and the Host is " + str(HOST)

	while True:
		# get the list sockets which are ready to be read through select
		# 4th arg, time_out  = 0 : poll and never block
		ready_to_read,ready_to_write,in_error = select.select(SOCKET_LIST,[],[],0) # select �Լ��� ���� � ������ ����� �� �غ� �Ǿ������� �����Ѵ�.
	  
		for sock in ready_to_read: # ���� �غ� �� ���Ͽ� ���ؼ�
			# when new connection request received
			if sock == server_socket: # ���� ��û�� ���ؼ� ������ ���ٸ�, �� ���ο� ��û�� ���´ٸ�
				sockfd, addr = server_socket.accept() # �������� ������ ������ ��
				SOCKET_LIST.append(sockfd) # ���� ����Ʈ�� �߰��Ѵ�.
				print "Client (%s, %s) is connected" % addr
				 
				broadcast(server_socket, sockfd, "[%s:%s] has joined the chat\n" % addr) # broadcast�� ���� ������ �������ִ� ��ο��� �޽����� �����Ѵ�.
			 
			# a message from a client, not a new connection
			else: # Ŭ���̾�Ʈ�κ����� �޽����� ���ο� ������ �ƴ� ���
				# process data received from client, 
				try: #Ŭ���̾�Ʈ�κ����� ������ ���μ����� �����Ѵ�.
					# receiving data from the socket.
					data = sock.recv(RECV_BUFFER) # Receive ���ۿ� �ִ� �����͸� data�� �����Ų��.
					
					if data: # data�� ���̶��, �� �����Ͱ� �ս��� ���ٸ�
						#broadcast(server_socket, sock, "\r" + '[' + str(sock.getpeername()) + '] ' + data)  
                                                #pemisah command dgn message
						temp1 = string.split(data[:-1]) # data�� ���ڿ��� �ɰ� �� temp1�� ����ִ´�.
                                                
						d=len(temp1) # d�� temp1�� �����̴�.
                                                #jika kata prtama adlh "login", masuk ke fungsi login 
						if temp1[0]=="login" : # temp1�� ������ login�� ��� �α��� �õ��� �ϴ� �����μ�,
							log_in(sock, str(temp1[1])) # ���ϰ� temp1[1]�� ���ڷ� log_in �Լ��� �����Ѵ�..
						#jika kata prtama adlh "send". Contoh "send toto hello"		
						elif temp1[0]=="send" : # ���� temp1�� ������ send�� ���,
							#logged itu utk status apakah user udh login ato blm
							logged = 0 # login ������ 0, �� false�� �ٲٰ�
							user = "" # ���� ������ ���� �𸥴�.
                                                        #x adlh iterator sebanyak isi array NAME_LIST. ini utk cek apakah nama user udh masuk di NAME_LIST ato blm
							for x in range (len(NAME_LIST)): # NAME_LIST�� ���� �ȿ��� �� ��ҿ� ���� �ݺ����� �����Ѵ�.
                                                                #jika ada di array NAME_LIST, user tsb udh login
								if NAME_LIST[x]==sock: # ���Ӹ���Ʈ�� ���� ������ ������ ���
									logged=1 # �α����� true�� �Ͽ� �α��� �� ������ �����Ѵ�.
                                                                        #masukkan nama user yg diinputkan ke variabel user, nnti disimpan di NAME_LIST
									user=NAME_LIST[x+1] # ���� ������ NAME_LIST�� �߰��ȴ�.
							
                                                        #jika user blm login
							if logged==0: # �α��� ������ false�� ���,
								send_msg(sock, "You need to login to start a chat\n") # �α����� �ʿ��ϴٴ� �޽����� ������.
							#jika udh login
							else: # �α��� ������ true�� ���,
								temp2="" # temp2�� ������ ���� ������ �ʱ�ȭ�ϰ�,
                                                                #x adlh iterator sebanyak panjang temp1
								for x in range (len(temp1)): # temp1�� ���� ���� ������ x�� ���ؼ� x�� ���� ��ȭ��Ű�� �ݺ����� �����Ѵ�.
									if x>1: # x>1�� ���,
                                                                                #jika temp2 msh kosong, temp2 diisi kata dari index ke-2 temp1
										if not temp2: # temp1�� temp2�� �ٸ��ٸ�
											temp2+=str(temp1[x]) #  temp2�� temp1[x]�� ������ �߰��ϰ�
                                                                                #jika temp2 udh ada isinya, temp2 diisi spasi dan kata selanjutnya
										else: # temp1�� temp2�� ���ٸ�,
											temp2+=" " # temp2�� ������ �߰��Ѵ�.
											temp2+=str(temp1[x]) # temp2�� temp1[x]�� ������ �߰��Ѵ�.
								#utk kirim message ke user yg dituju
								for x in range (len(NAME_LIST)): # NAME_LIST�� ������ ������ x�� ���� �ݺ����� �����Ѵ�.
									if NAME_LIST[x]==temp1[1]: # temp1[1]�� ������ NAME_LIST�� �����Ѵٸ�,
										send_msg(NAME_LIST[x-1], "["+user+"] : "+temp2+"\n") # �̸��� ��������, �޽����� �����Ѵ�.
															
						elif temp1[0]=="sendall" : # temp1[0]�� ������ sendall �̶��,
						#contoh "sendall hi everybody"	
							logged = 0
							user = ""
							for x in range (len(NAME_LIST)):
								if NAME_LIST[x]==sock:
									logged=1
									user=NAME_LIST[x+1]
							
							if logged==0:
								send_msg(sock, "You need to login to start a chat\n")
							
							else:
								temp2=""
								for x in range(len(temp1)):
									if x!=0:
										if not temp2:
											temp2=str(temp1[x])
										else:
											temp2+=" "
											temp2+=temp1[x]
                                                                #broadcast ini utk kirim pesan ke semua user yg online
								broadcast(server_socket, sock, "["+user+"] : "+temp2+"\n") # ���� ������ send�� ���������� sendall������ broadcast�� ��� �������� �޽����� ������.
							
                                                #utk liat daftar user yg ter-connect. contoh "list"
						elif temp1[0]=="list" : # temp1[0]�� ������ list�� ���,
							logged = 0
							for x in range (len(NAME_LIST)):
								if NAME_LIST[x]==sock:
									logged=1
							
							if logged==0:
								send_msg(sock, "You need to login to start a chat\n")
							
							else:
								temp2=""
                                                                #cari nama user dri index ganjil array NAME_LIST (soalnya disimpan dgn urutan alamat, nama, alamat, nama) 
								for x in range (len(NAME_LIST)):
									if x%2==1:
										temp2+=" "
										temp2+=str(NAME_LIST[x]) # ���� �ݺ����� ���� ��� NAME_LIST�� ������ temp2�� �߰��Ѵ�.
								send_msg(sock, "[List of User(s)] : "+temp2+"\n") # ������ ����� �����ִ� �޽����� ����Ѵ�.
							
						elif temp1[0]=="whoami" : # temp1[0]�� ������ whoami�� ���,
							g = 0 # �ӽ� ���� g�� 0���� ����
							for name in range (len(NAME_LIST)):
								if NAME_LIST[name]==sock: # ������ NAME_LIST�� �����Ѵٸ�
									g = 1 # g�� ���� 1�� �����ϰ�,
									send_msg(sock, "Username : "+str(NAME_LIST[name+1])+"\n") # ���� �̸��� �˷��ش�.
							if g==0: # ������ NAME_LIST�� �������� ������,
								send_msg(sock, "You haven't login\n") # ���� �α������� �ʾҴٴ� �޽����� ������.
								
						else: # ���� ��� ��쿡 �ش����� �ʴ� �˷����� ���� ��ɾ �Է��� ���,
							print ('Invalid Command')
					else: # ���� data�� false��� �ջ�� �� (������ ���� ��) �̹Ƿ�,
						# remove the socket that's broken    
						if sock in SOCKET_LIST:
							SOCKET_LIST.remove(sock) # ���� ����Ʈ���� �ش� ������ �����Ѵ�.

						# at this stage, no data means probably the connection has been broken
						broadcast(server_socket, sock, "The client (%s, %s) is offline\n" % addr) # ������ ���ŵ� Ŭ���̾�Ʈ�� �������� ���� �˸���.

				# exception 
				except: # ���� ���׿� ���ؼ���,
					broadcast(server_socket, sock, "The client (%s, %s) is offline\n" % addr) # Ŭ���̾�Ʈ�� �������� ���θ� �˸���
					continue

	server_socket.close() # ������ �ݴ´�.
    
# broadcast chat messages to all connected clients
def broadcast (server_socket, sock, message): # broadcast �Լ��� �����Ѵ�.
    for x in range (len(NAME_LIST)): # NAME_LIST�� ��� ���ڿ� ���ؼ�,
		
        # send the message only to peer
        if NAME_LIST[x] != server_socket and NAME_LIST[x] != sock and x%2==0 : #NAME_LIST�� ���� server_socket, sock�� ���� ���� �ʰ� ¦���� ��, �� �Ǿ��� ���
            try :
                NAME_LIST[x].send(message) # �޽����� ������.
            except :
                # broken socket connection
                NAME_LIST[x].close() # ������ ��� ������ �ݰ�
                # broken socket, remove it
                if NAME_LIST[x] in SOCKET_LIST: # ������ SOCKET_LIST�� ������ ���
                    SOCKET_LIST.remove(NAME_LIST[x]) # ������ �����Ѵ�.
 
def send_msg (sock, message): # send_msg�� �����Ѵ�.
	try:
		sock.send(message) # �޽��� ������ �õ��Ѵ�.
	except:
		sock.close() # ���ܻ����� ��� ������ �ݰ�,
		
		if sock in SOCKET_LIST:
			SOCKET_LIST.remove(sock) # ���ϸ���Ʈ���� ������ �����Ѵ�.

def log_in (sock, user): # log_in �Լ��� �����Ѵ�.
	g = 0 
	f = 0
	for name in NAME_LIST:
		if name == user:
			g = 1
		if name == sock:
			f = 1
	
        #jika user sblmnya udh login tapi dia login lg
	if f==1: # f�� true�� ���� name�� sock�� ���� ���� ���̹Ƿ� �̹� ���������� �����ϴ� ���̴�.
		send_msg(sock, "You already have a username\n") # ���������� �̹� �����Ѵٰ� �˸���.
        #jika user memilih nama yg sblmya udh terdaftar
	elif g==1: # g�� true�� ���� �̹� username�� NAME_LIST�� �����ϴ� ���̹Ƿ� �̹� ���ǰ� �ִ� username�̴�.
		send_msg(sock, "Username already exist. Enter another name\n") # �̹� ���ǰ� �ִ� username���� �˸���.
	else: # ���� ������ ��� �ش���� ������ �α����� ���������� �Ϸ�� �����μ�,
                #data user (alamat, nama) dimasukkan ke array NAME_LIST
		NAME_LIST.append(sock) # NAME_LIST�� sock�� �߰��ϰ�,
		NAME_LIST.append(user) # NAME_LIST�� user�� �߰��Ѵ�.
		send_msg(sock, "Login success. You can start a conversation now\n") # �α��� ������ �˸���.
	
chat_server()
