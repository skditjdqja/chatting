import sys
import socket
import select
import pickle 
import time
import string
 
def chat_client():

	sys.stdout.write('Host : ')
	host = sys.stdin.readline()
	
	sys.stdout.write('Port : ')
	port = int(sys.stdin.readline())
     
    # create TCP/IP socket
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
     
    # connect to remote host
	try :
		s.connect((host, port))
	except :
		print 'Client is unable to connect'
		sys.exit()
     
	print 'Client is now connected to remote host. You can start a conversation'
	sys.stdout.write('>> '); sys.stdout.flush()
     
	while 1:
		socket_list = [sys.stdin, s]
		 
		# Get the list sockets which are readable
		ready_to_read,ready_to_write,in_error = select.select(socket_list , [], [])
		 
		for sock in ready_to_read:      
		
			if sock == s:
				# incoming message from remote server, s
				data = sock.recv(4096)
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
				temp = sys.stdin.readline()
				temp1 = string.split(temp[:-1])
				
				d=len(temp1)
				if temp1[0]=="login" :
					if d>2:
						print('The username is invalid')
					elif d<2:
						print('Login need username. Enter your username')
					else:
						s.send(temp)
						
				elif temp1[0]=="send" :
					if d<3:
						print('Invalid Send Command')
					else:
						s.send(temp)
						
				elif temp1[0]=="sendall" :
					if d<2:
						print("Invalid SendAll Command")
					else:
						s.send(temp)
						
				elif temp1[0]=="list" :
					if d>1:
						print('List does not have parameter')
					else:
						s.send(temp)
						
				elif temp1[0]=="whoami" :
					if d>1:
						print('Whoami does not have parameter')
					else:
						s.send(temp)
						
				else:
					print ('Invalid Command')
				
				#s.send(temp)
				sys.stdout.write('>> '); sys.stdout.flush() 


chat_client()
