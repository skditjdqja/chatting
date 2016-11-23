import sys, socket, select, time, string
 
def chat_client():

	# connect to which server
        if(len(sys.argv) < 3) : # 인자값이 2개 미만값이 입력 되었을 때
                print 'Enter the Host name and the Port address'
                sys.exit()                              # 프로세스 종료

        # host is 'localhost' and port is 10000
        host = sys.argv[1] #첫번재 입력받은 값을 host로 저장
        port = int(sys.argv[2]) # 두번재 입력받은 값을 port에 저장 
     
    # create TCP/IP socket
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #소켓 생성
     
    # connect to remote host
	try :
		s.connect((host, port)) #연결을 시도 
	except :
		print 'Client is unable to connect' #연결이 실패했을 때 예외처리 
		sys.exit()
     
	print 'Client is now connected to remote host. You can start a conversation'
	sys.stdout.write('>> '); sys.stdout.flush()  #입력대기
     
	while 1:
		socket_list = [sys.stdin, s] 
		 
		# Get the list sockets which are readable
		ready_to_read,ready_to_write,in_error = select.select(socket_list , [], [])
		 
		for sock in ready_to_read:      
		
			if sock == s:
				# incoming message from remote server, s
				data = sock.recv(4096) #recv가 0을 반환하면 연결이 끊긴것.
				if not data : 
					print '\nYou are disconnected from chat server'
					sys.exit()
				else :
					#print data
					sys.stdout.write(data)
					sys.stdout.write('>> '); sys.stdout.flush()     
			
			else :
				# user entered a message
				msg = []
                                # menyediakan input utk masukkan kata
				temp = sys.stdin.readline() #입력값을 temp에 저장
				# temp1 khusus buat command
				temp1 = string.split(temp[:-1]) # 개행문자를 기준으로 temp를 분리시켜서 temp1에 저장한거같다.
				# d adlh panjang array temp1
				d=len(temp1)
				# jika kata pertama adlh "login"
				if temp1[0]=="login" :  # login [name] 이케 입력
                                        # command "login" tdk boleh lbh dari 2 kata
					if d>2:
						print('The username is invalid') #
                                        # command "login" tdk boleh kurang dri 2 kata
					elif d<2:
						print('Login need username. Enter your username')
                                        # klo memenuhi kriteria, kirim pesan ke server
					else:
						s.send(temp) #name을 서버로 전송
				# jika kata prtama adlh "send"		
				elif temp1[0]=="send" :
                                        # command "send" hrus lbh dri 3 kata. contoh "send toto hello"
					if d<3:
						print('Invalid Send Command')
					else:
						s.send(temp)
						
				elif temp1[0]=="sendall" : 
					if d<2:
						print("Invalid SendAll Command")
					else:
						s.send(temp)
						
				elif temp1[0]=="list" : # list만 입력
					if d>1:
						print('List does not have parameter')
					else:
						s.send(temp)
						
				elif temp1[0]=="whoami" : #whoami만 입력
					if d>1:
						print('Whoami does not have parameter')
					else:
						s.send(temp)
						
				else:
					print ('Invalid Command')
				
				#s.send(temp)
				sys.stdout.write('>> '); sys.stdout.flush() 


chat_client()
