import socketserver
import http.server
import logging
import cgi
import cv2
import numpy as np
import asyncio
from threading import Thread

stop_thread = False

def face_recognition_method():
    import face_recognition
    import base64

    #decoded_img = np.fromstring(ServerHandler1.camera_image, dtype=np.uint8)
    # photo_from_client = decoded_img.reshape((50, 50, 3))
    string_cam = ''
    for i,char in enumerate(ServerHandler1.b64):
        if i!=0 and i!=1 and i!= len(ServerHandler1.b64):
            string_cam = string_cam+char
    decoded_data1 = base64.b64decode((string_cam))
    img_file = open('camera.jpg', 'wb')
    img_file.write(decoded_data1)
    img_file.close()


    string_real = ''
    for i,char in enumerate(ServerHandler2.b64):
        if i!=0 and i!=1 and i!= len(ServerHandler2.b64):
            string_real = string_real+char
    decoded_data2 = base64.b64decode((string_real))
    img_file = open('bd_image.jpg', 'wb')
    img_file.write(decoded_data2)
    img_file.close()


    photo_pattern = 'G:\\Code_K\\GAGU\\bd_image.jpg'
    photo_from_client = 'G:\\Code_K\\GAGU\\camera.jpg'

    import os

    os.remove(photo_pattern)
    os.remove(photo_from_client)

    #decoded_img = np.fromstring(ServerHandler2.real_image, dtype=np.uint8)
    #photo_pattern = decoded_img.reshape((50, 50, 3))

    image_real = face_recognition.load_image_file(photo_pattern)
    image_predict = face_recognition.load_image_file(photo_from_client)
    my_face_encoding = face_recognition.face_encodings(image_real)[0]
    try:
        my_face_encoding = face_recognition.face_encodings(image_real)[0]
    except Exception as e:
        print('Лица не обнаружено')
        # точка выхода


    known_faces = [
        my_face_encoding
    ]
    verdict = False
    face_encodings = face_recognition.face_encodings(image_predict)
    for face_encoding in face_encodings:
        match = face_recognition.compare_faces(known_faces, face_encoding,
                                               tolerance=0.55)  # тут во время теста на фокус-группе надо толерантность крутить
        # лиц может быть несколько и на каждый надо дать вердикт, по идее обрезка в клиенте поможет этого избежать
        if match[0]:
            verdict = True

    if verdict:
        print('Сеанс продолжается')
    else:
        print('Дисконеннкт')
        # точка выхода


PORT_C = 8001
PORT_BD = 8002

class ServerHandler1(http.server.SimpleHTTPRequestHandler):
    b64 = ''
    def do_GET(self):
        logging.error(self.headers)
        http.server.SimpleHTTPRequestHandler.do_GET(self)

    def do_POST(self):
        logging.error(self.headers)
        form = cgi.FieldStorage(
            fp=self.rfile,
            headers=self.headers,
            environ={'REQUEST_METHOD': 'POST',
                     'CONTENT_TYPE': self.headers['Content-Type'],
                     })
        for item in form.list:
            logging.error(item)
        http.server.SimpleHTTPRequestHandler.do_GET(self)
        #print('1 Server live')
        with open("data1.txt", "w") as file:
            for key in form.keys():
                ServerHandler1.b64 = str(form.getvalue(str(key)))
                file.write(str(form.getvalue(str(key))))



class ServerHandler2(http.server.SimpleHTTPRequestHandler):
    b64 = ''
    def do_GET(self):
        logging.error(self.headers)
        http.server.SimpleHTTPRequestHandler.do_GET(self)

    def do_POST(self):
        logging.error(self.headers)
        form = cgi.FieldStorage(
            fp=self.rfile,
            headers=self.headers,
            environ={'REQUEST_METHOD': 'POST',
                     'CONTENT_TYPE': self.headers['Content-Type'],
                     })
        for item in form.list:
            logging.error(item)
        http.server.SimpleHTTPRequestHandler.do_GET(self)
        #print('2 Server live')

        with open("data2.txt", "w") as file:
            for key in form.keys():
                file.write(str(form.getvalue(str(key))))
                ServerHandler2.b64 = str(form.getvalue(str(key)))

PORT_C = 10001
PORT_BD = 10002

async def server_1():
    Handler1 = ServerHandler1
    httpd1 = socketserver.TCPServer(("", PORT_C), Handler1)
    httpd1.serve_forever()

async def server_2():
    Handler2 = ServerHandler2
    httpd2 = socketserver.TCPServer(("", PORT_BD), Handler2)
    httpd2.serve_forever()

def start_server1():
    while not stop_thread:
        loop1 = asyncio.new_event_loop()
        asyncio.set_event_loop(loop1)
        loop1.run_until_complete(server_1())
        loop1.close()
    return 0


def start_server2():
    while not stop_thread:
        loop2 = asyncio.new_event_loop()
        asyncio.set_event_loop(loop2)
        loop2.run_until_complete(server_2())
        loop2.close()
    return 0

thread1 = Thread(target=start_server1, args=())
thread1.start()
thread2 = Thread(target=start_server2, args=())
thread2.start()

while True:
    PORT = 10003
    Handler = http.server.BaseHTTPRequestHandler
    with socketserver.TCPServer(("localhost", PORT), Handler) as httpd:
        #print("serving at port", PORT)
        if httpd.handle_request():
            print('1')
        else:
            print('2')
            face_recognition_method()
httpd.close()
stop_thread = True