from socket import *

def smtp_client(port=1025, mailserver= '127.0.0.1'):
    msg = "\r\n My message"
    endmsg = "\r\n.\r\n"

    # Choose a mail server (e.g. Google mail server) if you want to verify the script beyond GradeScope

    # Create socket called clientSocket and establish a TCP connection with mailserver and port

    # Fill in start
    # mailserver = ("127.0.0.1", 1025)
    clientSocket = socket(AF_INET, SOCK_STREAM)
    clientSocket.connect((mailserver, port))
    # Fill in end

    recv = clientSocket.recv(1024).decode()

    #print(recv)
    #if recv[:3] != '220':
        #print('220 reply not received from server.')

    # Send HELO command and print server response.
    heloCommand = 'HELO Alice\r\n'
    clientSocket.send(heloCommand.encode())
    recv1 = clientSocket.recv(1024).decode()
    #print(recv1)
    #if recv1[:3] != '250':
        #print('Fail 1')

    # Send MAIL FROM command and handle server response.
    # Fill in start
    mailFrom = "MAIL FROM: <srn9327@nyu.edu> \r\n"
    clientSocket.send(mailFrom.encode())
    recv2 = clientSocket.recv(1024).decode()
    #print(recv2)  # You can use these print statement to validate return codes from the server.
    #if recv2[:3] != '250':
        #print('Fail 2')
    # Fill in end

    # Send RCPT TO command and handle server response.
    # Fill in start
    RCPTTO = "RCPT TO: <srn9327@nyu.edu> \r\n"
    clientSocket.send(RCPTTO.encode())
    recv3 = clientSocket.recv(1024).decode()
    #print(recv3)
    #if recv3[:3] != '250':
        #print('Fail 3')
    # Fill in end
""""
    # Send DATA command and handle server response.
    # Fill in start
    data = "DATA\r\n"
    clientSocket.send(data.encode())
    recv4 = clientSocket.recv(1024).decode()
    #print(recv4)
    #if recv4[:3] != '250':
        #print('Fail 4')
    # Fill in end

    # Send message data.
    # Fill in start
    subjectLine = "SMTP Assignment \r\n"
    clientSocket.send(subjectLine.encode())
    body = "Message"
    clientSocket.send(body.encode())
    # Fill in end

    # Message ends with a single period, send message end and handle server response.
    # Fill in start
    clientSocket.send(endmsg.encode())
    #print(recv1)
    #if recv1[:3] != '250':
        #print('Fail 5')
    # Fill in end

    # Send QUIT command and handle server response.
    # Fill in start
    clientSocket.send("QUIT \r\n".encode())
    recv5 = clientSocket.recv(1024).decode()
    if recv5[:3] != '250':
        print('Fail 6')
    clientSocket.close()
    # Fill in end
"""
if __name__ == '__main__':
    smtp_client(1025, '127.0.0.1')
