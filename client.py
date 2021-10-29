# Client Side script
import socket
import os
from time import ctime
from threading import Thread


######################################
# TODO automate server hosting on ngrok #
#####################################


# creating the socket object
client = socket.socket()

# host and port
# TODO replace HOST and PORT with user inpy=uts
HOST = os.getenv('HOST') or 'localhost'
PORT = os.getenv('PORT') or 6969

BUFF = 2048		# Max Buffer size

name = input("\n\033[38;5;84mWhat should people call you? :\033[0m ")
send_name = "$name: " + name

col, row = os.get_terminal_size(0)
padding = (col - 20) // 2 - 2

try:
    # add a retry mech
    client.connect((HOST, PORT))
except:
    print("\033[1;31m[-] Server is taking a nap 😪\033[0m\n")
    exit(0)

print()
print("+" + "="*padding +
      "\033[4m| Welcome to \033[1mChatBOX |\033[0m" + "="*padding + "+")
print(f"\n\033[3m[+] You are Logged in as \033[0;1;38;5;82m{name}\033[0m")
print()


def showMsg(msg, newJoin):
    if newJoin:
        print("\b\b\b\b\b\b     \n\033[38;5;135m" + msg + '\033[0m')
    else:
        print('\b\b\b\b\b\b' + msg + '\n\033[38;5;46mYou>>', end=' \033[0m')


def receive():
    while True:
        try:
            message = client.recv(BUFF).decode()

            if message == "$$":
                client.send(send_name.encode())
            elif message.startswith('$#'):
                message = message[2:]
                showMsg(message, 1)
            else:
                showMsg(message, 0)

        except:
            print(
                "\n\033[1;31m[!] Unexpected error occurred\n[-] Terminating connnection with server\033[0m")
            client.close()
            break


def write():
    receive_thread = Thread(target=receive)
    receive_thread.start()

    while True:
        msg = input('\033[38;5;46mYou>>\033[0m ')
        timestamp = '(' + '\033[38;5;45m' + ctime()[11:16] + '\033[0m' + ')'

        msg = '\033[38;5;47m' + msg + '\033[0m'
        msg = '\033[38;5;196m[ \033[0m' + '\033[38;5;190m' + name + \
            '\033[0m' + '\033[38;5;196m ]\033[0m' + timestamp + ': ' + msg

        client.send(msg.encode())


write()
