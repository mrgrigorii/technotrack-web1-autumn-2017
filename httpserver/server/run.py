# -*- coding: utf-8 -*-
import socket
import os

list_files_in_media = os.listdir('./files/')
url_files = ['/media/' + i for i in list_files_in_media]

def pars_request(request):
    args = {}
    for line in request.split('\n'):
        if line[0:3] == 'GET': args['GET'] = line[4:].split('HTTP')[0].strip(' ')
        elif line[0:10] == 'User-Agent': args['User-Agent'] = line[12:].strip('\r')
    return args

def response_200(response_text):
    response = ['HTTP/1.1 200 OK', 
                '',
                response_text]
    return '\n'.join(response)

def response_404(response_text):
    response = ['HTTP/1.1 404 Not found', 
                '',
                response_text]
    return '\n'.join(response)

def get_response(request):
    response_text = ''
    args = pars_request(request)
    if args['GET'] == '/':
        response_text = 'Hello mister!\nYou are: (' + args['User-Agent'] + ')'
    elif args['GET'] == '/test/':
        response_text = request
    elif args['GET'] == '/media/':
        response_text = '\n'.join(list_files_in_media)
    elif args['GET'][0:7] == '/media/':
        if args['GET'] in url_files:
            with open('./files/' + args['GET'].split('/')[-1], 'r') as f:
                response_text = f.read()
        else:
            return response_404("File not found")
    else:
        return response_404("Page not found")

    return response_200(response_text)


server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind(('localhost', 8000))  # Связываем сокет с хостом "localhost" и портом "8000"
server_socket.listen(0)  # Режип прослушивания, максимальная очередь "0"

print 'Started'

while 1:
    try:
        (client_socket, address) = server_socket.accept()
        print 'Got new client', client_socket.getsockname()  # Фиксируем подключение клиента, выводим хост и порт клиента
        request_string = client_socket.recv(2048)  # Принимаем данные от клиента по 2048 байт, по кускам
        client_socket.send(get_response(request_string))  # Высылаем ответ на запрос клиента
        client_socket.close()
    except KeyboardInterrupt:  #  Перехватываем в консоли ctrl + C
        print 'Stopped'
        server_socket.close()  # Закрываем сокет перед завершением программы
        exit()
