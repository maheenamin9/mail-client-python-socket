from socket import *
import ssl
import base64

bufferSize = 2048

def create_auth_message(user: str, password: str):
  str = "\x00"+user+"\x00"+password
  base64_str = base64.b64encode(str.encode())
  return "AUTH PLAIN " + base64_str.decode()

socket = socket(AF_INET, SOCK_STREAM)
socket.settimeout(5)
ssl_socket = ssl.wrap_socket(socket)
ssl_socket.connect(("smtp.gmail.com", 465))

def recv_msg():
  try:
    return ssl_socket.recv(bufferSize).decode()
  except timeout:
    pass

def send_msg(message, expect_return_msg=True):
  ssl_socket.send(f"{message}\r\n".encode())
  if expect_return_msg:
    recv = recv_msg()
    print(recv)
    return recv

def ehlo():
  return send_msg("ehlo Maheen")

def login(user, password):
  auth_msg = create_auth_message(user, password)
  send_msg(auth_msg)

def quit():
  return send_msg("QUIT")

def send_mail(msg, from_addr, to_addr):
  send_msg(f"MAIL FROM:<{from_addr}>")
  send_msg(f"RCPT TO:<{to_addr}>")
  send_msg(f"DATA")
  send_msg(f"SUBJECT: Hye! Maheen here\r\n", expect_return_msg=False)
  send_msg(msg, expect_return_msg=False)
  send_msg(".")

ehlo()
login("maheenamin9@gmail.com", "zvlyyrliymgooyqw")
send_mail("I am Maheen;) I am studing BS computer science in UET New Campus.",
          "maheenamin9@gmail.com", "cs18b670@gmail.com")
quit()

