import sys
import socket
import select
import string

HOST = 'localhost' 
SOCKET_LIST = []
NAME_LIST = []
RECV_BUFFER = 4096 
PORT = 1


def chat_server():

	sys.stdout.write('Port : ')
	PORT = int(sys.stdin.readline())
	
	#creating TCP/IP socket
	server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

	# binding the socket (available for 10)
	server_socket.bind((HOST, PORT))
	server_socket.listen(10)

	# add server socket object to the list of readable connections
	SOCKET_LIST.append(server_socket)

	print "The chat server is started on Port " + str(PORT)

	while True:
		# get the list sockets which are ready to be read through select
		# 4th arg, time_out  = 0 : poll and never block
		ready_to_read,ready_to_write,in_error = select.select(SOCKET_LIST,[],[],0)
	  
		for sock in ready_to_read:
			# when new connection request received
			if sock == server_socket: 
				sockfd, addr = server_socket.accept()
				SOCKET_LIST.append(sockfd)
				print "Client (%s, %s) is connected" % addr
				 
				broadcast(server_socket, sockfd, "[%s:%s] has joined the chat\n" % addr)
			 
			# a message from a client, not a new connection
			else:
				# process data received from client, 
				try:
					# receiving data from the socket.
					data = sock.recv(RECV_BUFFER)
					
					if data:
						#broadcast(server_socket, sock, "\r" + '[' + str(sock.getpeername()) + '] ' + data)  
						temp1 = string.split(data[:-1])
				
						d=len(temp1)
						if temp1[0]=="login" :
							log_in(sock, str(temp1[1]))
								
						elif temp1[0]=="send" :
							
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
								for x in range (len(temp1)):
									if x>1:
										if not temp2:
											temp2+=str(temp1[x])
										else:
											temp2+=" "
											temp2+=str(temp1[x])
								
								for x in range (len(NAME_LIST)):
									if NAME_LIST[x]==temp1[1]:
										send_msg(NAME_LIST[x-1], "["+user+"] : "+temp2+"\n")
								
						elif temp1[0]=="sendall" :
							
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
								broadcast(server_socket, sock, "["+user+"] : "+temp2+"\n")
							
						elif temp1[0]=="list" :
							logged = 0
							for x in range (len(NAME_LIST)):
								if NAME_LIST[x]==sock:
									logged=1
							
							if logged==0:
								send_msg(sock, "You need to login to start a chat\n")
							
							else:
								temp2=""
								for x in range (len(NAME_LIST)):
									if x%2==1:
										temp2+=" "
										temp2+=str(NAME_LIST[x])
								send_msg(sock, "[List of User(s)] : "+temp2+"\n")
							
						elif temp1[0]=="whoami" :
							g = 0
							for name in range (len(NAME_LIST)):
								if NAME_LIST[name]==sock:
									g = 1
									send_msg(sock, "Username : "+str(NAME_LIST[name+1])+"\n")
							if g==0:
								send_msg(sock, "You haven't login\n")
								
						else:
							print ('Invalid Command')
					else:
						# remove the socket that's broken    
						if sock in SOCKET_LIST:
							SOCKET_LIST.remove(sock)

						# at this stage, no data means probably the connection has been broken
						broadcast(server_socket, sock, "The client (%s, %s) is offline\n" % addr) 

				# exception 
				except:
					broadcast(server_socket, sock, "The client (%s, %s) is offline\n" % addr)
					continue

	server_socket.close()
    
# broadcast chat messages to all connected clients
def broadcast (server_socket, sock, message):
    for x in range (len(NAME_LIST)):
		
        # send the message only to peer
        if NAME_LIST[x] != server_socket and NAME_LIST[x] != sock and x%2==0 :
            try :
                NAME_LIST[x].send(message)
            except :
                # broken socket connection
                NAME_LIST[x].close()
                # broken socket, remove it
                if NAME_LIST[x] in SOCKET_LIST:
                    SOCKET_LIST.remove(NAME_LIST[x])
 
def send_msg (sock, message):
	try:
		sock.send(message)
	except:
		sock.close()
		
		if sock in SOCKET_LIST:
			SOCKET_LIST.remove(sock)

def log_in (sock, user):
	g = 0
	f = 0
	for name in NAME_LIST:
		if name == user:
			g = 1
		if name == sock:
			f = 1
	
	if f==1:
		send_msg(sock, "You already have a username\n")
	elif g==1:
		send_msg(sock, "Username already exist. Enter another name\n")
	else:
		NAME_LIST.append(sock)
		NAME_LIST.append(user)
		send_msg(sock, "Login success. You can start a conversation now\n")
	
chat_server()
