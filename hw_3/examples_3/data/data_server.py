""" Программа сервера для получения приветствия от клиента и отправки ответа """

from socket import socket, AF_INET, SOCK_STREAM

SERV_SOCK = socket(AF_INET, SOCK_STREAM)
SERV_SOCK.bind(('', 8007))  # присваивает сокету указанный адрес
SERV_SOCK.listen(1)  # переводит сокет в режим ожидания входящих соединений

try:
    while True:
        CLIENT_SOCK, ADDR = SERV_SOCK.accept()  # принимает соединение и возвращает кортеж (conn, address).
        # В поле conn возвращается новый объект сокета, который может использоваться для приема и передачи
        # данных через соединение. В поле address возвращается адрес сокета с другой стороны соединения;
        DATA = CLIENT_SOCK.recv(4096)  # принимает данные из сокета
        print(f"Сообщение: {DATA.decode('utf-8')} было отправлено клиентом: {ADDR})")
        MSG = 'Привет, клиент'
        CLIENT_SOCK.send(MSG.encode('utf-8'))  # посылает данные через сетевое соединение
        CLIENT_SOCK.close()
finally:
    SERV_SOCK.close()
