import torch
from matplotlib import pyplot as plt
import numpy as np
import cv2
import os
import base64
import socket
import http.server
import socketserver

img = cv2.imread('G:\\Code_K\\GAGU\\yolo5\\MY1.jpg')
img2 = cv2.imread('G:\\Code_K\\GAGU\\yolo5\\MY2.jpg')

def send_frame():
    # энаписать серв который принимает хттп запросы и активирует функцию по триггеру
    # возможно он будет отправлять что-то куда-то
    # юзать виртуальное окружение pipenv типа поднимается проект со своими зависимостями
    # клиент должен быть запущен и цикл должен работать т.к. модель с детекцией лица долго грузиться.
    # гет запросы в фласке

    cap = cv2.VideoCapture(0)
    ret, frame = cap.read()
    #frame = img
    #frame = cv2.resize(frame, dsize=(50, 50))

    jpg_img = cv2.imencode('.jpg', img)
    b64_string1 = base64.b64encode(jpg_img[1]).decode('utf-8')

    jpg_img = cv2.imencode('.jpg', img2)
    b64_string2 = base64.b64encode(jpg_img[1]).decode('utf-8')


    from io import BytesIO

    files = {
        'camera_image': ('camera_image.jpg', b64_string1)
    }

    files2 = {
        'real_image': ('real_image.jpg', b64_string2)
    }


    import requests
    try:
        r = requests.post("http://localhost:10001", files=files)
        print('OK-1')
    except requests.exceptions.RequestException as e:
        print('Error')

    try:
        q = requests.post("http://localhost:10002", files=files2)
        print('OK-2')
    except requests.exceptions.RequestException as e:
        print('Error')

    cv2.imshow('YOLO', frame)
    cap.release()
    cv2.destroyAllWindows()



while True:
    PORT = 10000
    Handler = http.server.BaseHTTPRequestHandler
    with socketserver.TCPServer(("localhost", PORT), Handler) as httpd:
        #print("serving at port", PORT)
        if httpd.handle_request():
            print('1')
        else:
            #print('2')
            send_frame()
httpd.close()