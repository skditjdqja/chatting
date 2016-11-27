import sys, socket, select

HOST = 'localhost' 
SOCKET_LIST = []
RECV_BUFFER = 4096 
PORT = 11000


def chat_server():

    #creating TCP/IP socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    # binding the socket
    server_socket.bind((HOST, PORT))
    server_socket.listen(10)
 
    # add server socket object to the list of readable connections
    SOCKET_LIST.append(server_socket)
 
    print "The chat server is started on Port " + str(PORT)
    print "and the Host is " + str(HOST)
 
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
                        # there is something in the socket
                        broadcast(server_socket, sock, "\r" + '[' + str(sock.getpeername()) + '] ' + data)  
                    else:
                        # remove the socket that's broken    
                        if sock in SOCKET_LIST:
                            SOCKET_LIST.remove(sock)

                        # at this stage, no data means probably the connection has been broken
                        broadcast(server_socket, sock, "Client (%s, %s) is offline\n" % addr) 

                # exception 
                except:
                    broadcast(server_socket, sock, "Client (%s, %s) is offline\n" % addr)
                    continue

    server_socket.close()
    
# broadcast chat messages to all connected clients
def broadcast (server_socket, sock, message):
    for socket in SOCKET_LIST:
        # send the message only to peer
        if socket != server_socket and socket != sock :
            try :
                socket.send(message)
            except :
                # broken socket connection
                socket.close()
                # broken socket, remove it
                if socket in SOCKET_LIST:
                    SOCKET_LIST.remove(socket)
 
if __name__ == "__main__":

    sys.exit(chat_server())

#호스트는 로컬호스트며 버퍼의 사이즈는 4096, 그리고 통신포트번호는 11000이다.
#chat_server의 함수에서 TCP/IP 소켓을 생성하며 생성된 소켓을 적용, 그리고 서버에 추가 시킨다.
#새로운 연결 요청을 받았을 때, 클라이언트 측 소켓과 서버 소켓일 일치할 경우 서버 소켓을 받고 리스트에 추가한다. 그리고 해당 클라이언트의 IP주소를 띄우고 동시에 is connected 메시지를 띄운다.
#클라이언트에게 메시지를 받고 연결이 되지 않을 때 다시 시도를 하고 받았던 소켓리스트를 제거한다.
#예외처리로써 클라이언트가 오프라인일 경우에 예외처리한다.
#통신을 마치면 소켓을 닫는다.
#모든 클라이언트가 연결된 서버 내에 메시지를 전송할 때 브로드케스트로 한다.
#이때 예외사항으로 소켓연결이 손상된 것은 소켓리스트에서 제거한다.