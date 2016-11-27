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

#ȣ��Ʈ�� ����ȣ��Ʈ�� ������ ������� 4096, �׸��� �����Ʈ��ȣ�� 11000�̴�.
#chat_server�� �Լ����� TCP/IP ������ �����ϸ� ������ ������ ����, �׸��� ������ �߰� ��Ų��.
#���ο� ���� ��û�� �޾��� ��, Ŭ���̾�Ʈ �� ���ϰ� ���� ������ ��ġ�� ��� ���� ������ �ް� ����Ʈ�� �߰��Ѵ�. �׸��� �ش� Ŭ���̾�Ʈ�� IP�ּҸ� ���� ���ÿ� is connected �޽����� ����.
#Ŭ���̾�Ʈ���� �޽����� �ް� ������ ���� ���� �� �ٽ� �õ��� �ϰ� �޾Ҵ� ���ϸ���Ʈ�� �����Ѵ�.
#����ó���ν� Ŭ���̾�Ʈ�� ���������� ��쿡 ����ó���Ѵ�.
#����� ��ġ�� ������ �ݴ´�.
#��� Ŭ���̾�Ʈ�� ����� ���� ���� �޽����� ������ �� ��ε��ɽ�Ʈ�� �Ѵ�.
#�̶� ���ܻ������� ���Ͽ����� �ջ�� ���� ���ϸ���Ʈ���� �����Ѵ�.