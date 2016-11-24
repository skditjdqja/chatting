import sys, socket, select, string

HOST = 'localhost' 
SOCKET_LIST = []
NAME_LIST = []
RECV_BUFFER = 4096 
PORT = 11000


def chat_server():

	#creating TCP/IP socket
	server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # IPv4 인터넷 프로토콜으로 소켓 생성
	server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) #소켓 레벨에서 이미 사용된 주소를 재사용 (bind) 하도록 한다.

	# binding the socket (available for 10)
	server_socket.bind((HOST, PORT)) # 소켓에 주소와 포트를 설정한다.
	server_socket.listen(10) # 통신할 수 있는 갯수를 10개로 제한

	# add server socket object to the list of readable connections
	SOCKET_LIST.append(server_socket) # 읽을 수 있는 연결을 담고 있는 SOCKET_LIST 배열에 서버 소켓 오브젝트를 추가한다.

	print "The chat server is started on Port " + str(PORT)
        print "and the Host is " + str(HOST)

	while True:
		# get the list sockets which are ready to be read through select
		# 4th arg, time_out  = 0 : poll and never block
		ready_to_read,ready_to_write,in_error = select.select(SOCKET_LIST,[],[],0) # select 함수를 통해 어떤 소켓이 통신을 할 준비가 되었는지를 선택한다.
	  
		for sock in ready_to_read: # 읽은 준비가 된 소켓에 대해서
			# when new connection request received
			if sock == server_socket: # 받은 요청에 대해서 소켓이 같다면, 즉 새로운 요청이 들어온다면
				sockfd, addr = server_socket.accept() # 서버로의 접속을 승인한 후
				SOCKET_LIST.append(sockfd) # 소켓 리스트에 추가한다.
				print "Client (%s, %s) is connected" % addr
				 
				broadcast(server_socket, sockfd, "[%s:%s] has joined the chat\n" % addr) # broadcast를 통해 서버에 접속해있는 모두에게 메시지를 전송한다.
			 
			# a message from a client, not a new connection
			else: # 클라이언트로부터의 메시지가 새로운 연결이 아닐 경우
				# process data received from client, 
				try: #클라이언트로부터의 데이터 프로세싱을 진행한다.
					# receiving data from the socket.
					data = sock.recv(RECV_BUFFER) # Receive 버퍼에 있는 데이터를 data로 저장시킨다.
					
					if data: # data가 참이라면, 즉 데이터가 손실이 없다면
						#broadcast(server_socket, sock, "\r" + '[' + str(sock.getpeername()) + '] ' + data)  
                                                #pemisah command dgn message
						temp1 = string.split(data[:-1]) # data의 문자열을 쪼갠 후 temp1에 집어넣는다.
                                                
						d=len(temp1) # d는 temp1의 길이이다.
                                                #jika kata prtama adlh "login", masuk ke fungsi login 
						if temp1[0]=="login" : # temp1의 내용이 login일 경우 로그인 시도를 하는 것으로서,
							log_in(sock, str(temp1[1])) # 소켓과 temp1[1]을 인자로 log_in 함수를 실행한다..
						#jika kata prtama adlh "send". Contoh "send toto hello"		
						elif temp1[0]=="send" : # 만약 temp1의 내용이 send일 경우,
							#logged itu utk status apakah user udh login ato blm
							logged = 0 # login 정보를 0, 즉 false로 바꾸고
							user = "" # 유저 정보는 아직 모른다.
                                                        #x adlh iterator sebanyak isi array NAME_LIST. ini utk cek apakah nama user udh masuk di NAME_LIST ato blm
							for x in range (len(NAME_LIST)): # NAME_LIST의 범위 안에서 각 요소에 대해 반복문을 수행한다.
                                                                #jika ada di array NAME_LIST, user tsb udh login
								if NAME_LIST[x]==sock: # 네임리스트에 소켓 정보가 존재할 경우
									logged=1 # 로그인을 true로 하여 로그인 된 것으로 설정한다.
                                                                        #masukkan nama user yg diinputkan ke variabel user, nnti disimpan di NAME_LIST
									user=NAME_LIST[x+1] # 유저 정보는 NAME_LIST에 추가된다.
							
                                                        #jika user blm login
							if logged==0: # 로그인 정보가 false일 경우,
								send_msg(sock, "You need to login to start a chat\n") # 로그인이 필요하다는 메시지를 보낸다.
							#jika udh login
							else: # 로그인 정보가 true일 경우,
								temp2="" # temp2는 내용이 없는 것으로 초기화하고,
                                                                #x adlh iterator sebanyak panjang temp1
								for x in range (len(temp1)): # temp1의 범위 안의 미지수 x에 대해서 x의 값을 변화시키며 반복문을 수행한다.
									if x>1: # x>1일 경우,
                                                                                #jika temp2 msh kosong, temp2 diisi kata dari index ke-2 temp1
										if not temp2: # temp1이 temp2와 다르다면
											temp2+=str(temp1[x]) #  temp2에 temp1[x]의 내용을 추가하고
                                                                                #jika temp2 udh ada isinya, temp2 diisi spasi dan kata selanjutnya
										else: # temp1이 temp2와 같다면,
											temp2+=" " # temp2에 공백을 추가한다.
											temp2+=str(temp1[x]) # temp2에 temp1[x]의 내용을 추가한다.
								#utk kirim message ke user yg dituju
								for x in range (len(NAME_LIST)): # NAME_LIST의 범위의 미지수 x에 대해 반복문을 수행한다.
									if NAME_LIST[x]==temp1[1]: # temp1[1]의 내용이 NAME_LIST에 존재한다면,
										send_msg(NAME_LIST[x-1], "["+user+"] : "+temp2+"\n") # 이름과 유저네임, 메시지를 전송한다.
															
						elif temp1[0]=="sendall" : # temp1[0]의 내용이 sendall 이라면,
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
								broadcast(server_socket, sock, "["+user+"] : "+temp2+"\n") # 위의 과정은 send와 동일하지만 sendall에서는 broadcast로 모든 유저에게 메시지를 보낸다.
							
                                                #utk liat daftar user yg ter-connect. contoh "list"
						elif temp1[0]=="list" : # temp1[0]의 내용이 list일 경우,
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
										temp2+=str(NAME_LIST[x]) # 위의 반복문을 통해 모든 NAME_LIST의 내용을 temp2에 추가한다.
								send_msg(sock, "[List of User(s)] : "+temp2+"\n") # 유저의 목록을 보여주는 메시지를 출력한다.
							
						elif temp1[0]=="whoami" : # temp1[0]의 내용이 whoami일 경우,
							g = 0 # 임시 변수 g를 0으로 설정
							for name in range (len(NAME_LIST)):
								if NAME_LIST[name]==sock: # 소켓이 NAME_LIST에 존재한다면
									g = 1 # g의 값을 1로 변경하고,
									send_msg(sock, "Username : "+str(NAME_LIST[name+1])+"\n") # 유저 이름을 알려준다.
							if g==0: # 소켓이 NAME_LIST에 존재하지 않으면,
								send_msg(sock, "You haven't login\n") # 아직 로그인하지 않았다는 메시지를 보낸다.
								
						else: # 위의 모든 경우에 해당하지 않는 알려지지 않은 명령어를 입력할 경우,
							print ('Invalid Command')
					else: # 만약 data가 false라면 손상된 것 (소켓이 닫힌 것) 이므로,
						# remove the socket that's broken    
						if sock in SOCKET_LIST:
							SOCKET_LIST.remove(sock) # 소켓 리스트에서 해당 소켓을 제거한다.

						# at this stage, no data means probably the connection has been broken
						broadcast(server_socket, sock, "The client (%s, %s) is offline\n" % addr) # 소켓이 제거된 클라이언트가 오프라인 임을 알린다.

				# exception 
				except: # 예외 사항에 대해서는,
					broadcast(server_socket, sock, "The client (%s, %s) is offline\n" % addr) # 클라이언트의 오프라인 여부를 알리고
					continue

	server_socket.close() # 소켓을 닫는다.
    
# broadcast chat messages to all connected clients
def broadcast (server_socket, sock, message): # broadcast 함수를 정의한다.
    for x in range (len(NAME_LIST)): # NAME_LIST의 모든 인자에 대해서,
		
        # send the message only to peer
        if NAME_LIST[x] != server_socket and NAME_LIST[x] != sock and x%2==0 : #NAME_LIST의 값이 server_socket, sock의 값과 같지 않고 짝수일 때, 즉 피어일 경우
            try :
                NAME_LIST[x].send(message) # 메시지를 보낸다.
            except :
                # broken socket connection
                NAME_LIST[x].close() # 예외일 경우 소켓을 닫고
                # broken socket, remove it
                if NAME_LIST[x] in SOCKET_LIST: # 소켓이 SOCKET_LIST에 존재할 경우
                    SOCKET_LIST.remove(NAME_LIST[x]) # 소켓을 제거한다.
 
def send_msg (sock, message): # send_msg를 정의한다.
	try:
		sock.send(message) # 메시지 전송을 시도한다.
	except:
		sock.close() # 예외사항의 경우 소켓을 닫고,
		
		if sock in SOCKET_LIST:
			SOCKET_LIST.remove(sock) # 소켓리스트에서 소켓을 제거한다.

def log_in (sock, user): # log_in 함수를 정의한다.
	g = 0 
	f = 0
	for name in NAME_LIST:
		if name == user:
			g = 1
		if name == sock:
			f = 1
	
        #jika user sblmnya udh login tapi dia login lg
	if f==1: # f가 true일 경우는 name과 sock의 값이 같은 것이므로 이미 유저네임이 존재하는 것이다.
		send_msg(sock, "You already have a username\n") # 유저네임이 이미 존재한다고 알린다.
        #jika user memilih nama yg sblmya udh terdaftar
	elif g==1: # g가 true일 경우는 이미 username이 NAME_LIST에 존재하는 것이므로 이미 사용되고 있는 username이다.
		send_msg(sock, "Username already exist. Enter another name\n") # 이미 사용되고 있는 username임을 알린다.
	else: # 위의 사항이 모두 해당되지 않으면 로그인이 정상적으로 완료된 것으로서,
                #data user (alamat, nama) dimasukkan ke array NAME_LIST
		NAME_LIST.append(sock) # NAME_LIST에 sock을 추가하고,
		NAME_LIST.append(user) # NAME_LIST에 user를 추가한다.
		send_msg(sock, "Login success. You can start a conversation now\n") # 로그인 성공을 알린다.
	
chat_server()
