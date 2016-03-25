import socket

HOST, PORT = 'localhost', 8000
sock = socket.socket()
sock.bind((HOST, PORT))
sock.listen(10)
buf = 2048

while True:
    conn, addr = sock.accept()
    request = conn.recv(buf)
    result = request.split('\n')[0].split(' ')[1]
    path = '/' + result
    if path == '/':
            path ='/index.html' 
    file = open(path, 'r')
    conn.send("""HTTP/1.1 200 OK\nContent-Type: text/html\n\n\n""" + file.read())
    file.close()
    conn.close()
sock.close()
