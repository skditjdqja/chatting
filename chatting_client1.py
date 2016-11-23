import sys, socket, select
 
def chat_client():#클라이언트 함수
    # connect to which server
    if(len(sys.argv) < 3) :#받는 인자가 3개 미만일 때
        print 'Enter the Host name and the Port address'
        sys.exit()#출력하고 종료

    # host is 'localhost' and port is 10000
    host = sys.argv[1]#첫번째인자는 호스트
    port = int(sys.argv[2])#두번째인자는 포트번호이다
     
    # create TCP/IP socket
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)#소켓 생성함수

    s.settimeout(2)
     
    # connect to remote host
    try :
        s.connect((host, port))#받은 호스트와 포트를 이용해 연결한다.
    except :#연결되지않을 경우
        print 'Client is unable to connect'#연결되지않음
        sys.exit()#종료
     
    print 'Client is now connected to remote host. You can start sending messages'# 성공 메시지
    sys.stdout.write('[Holmes]: '); sys.stdout.flush()#[Holmes]: message 이런식으로 출력된다 (메시지입력창)
     
    while 1:
        socket_list = [sys.stdin, s]
         
        # Get the list sockets which are readable
        ready_to_read,ready_to_write,in_error = select.select(socket_list , [], [])# ready_to_read는 읽을 준비가 된 포트, ready_to_write은 쓸 준비가 된 포트, in_error는 에러메시지를 담은 것들을 select가 모아준다.
         
        for sock in ready_to_read:#읽을 준비가 될 포트들             
            if sock == s:#읽을 메시지가 있는 경우
                # incoming message from remote server, s
                data = sock.recv(4096)#메시지를 읽는다.
                if not data :#실패시 메시지출력 후 종료
                    print '\nYou are disconnected from chat server'
                    sys.exit()
                else :#성공시
                    #print data
                    sys.stdout.write(data)#읽은 데이터 출력 후다시 클라이언트가 메시지 입력 
                    sys.stdout.write('[Holmes]: '); sys.stdout.flush()     
            
            else :#유저가 메시지를 입력하는 경우
                # user entered a message
                msg = sys.stdin.readline()#메시지를임력받고
                s.send(msg)#보낸다
                sys.stdout.write('[Holmes]: '); sys.stdout.flush() 

if __name__ == "__main__":#서버측에서의 메시지로 유추

    sys.exit(chat_client())# 클라이언트 종료

    #2016.11.23 chatting_client1.py 수정완료, chatting_clinet2.py는 모든 내용이 같고 Holmes가 Watson으로 바뀌어있음.
