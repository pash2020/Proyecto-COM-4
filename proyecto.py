import speech_recognition as sr
import pyttsx3
import time
import cv2
import numpy as np
import pytesseract
from PIL import Image
from subprocess import call
from gtts import gTTS
import pygame
import re
import pandas as pd
from pandas import ExcelWriter
from datetime import date




Dosis=[]
tipo=[]
Nombre=[]
Apellido=[]
Edad=[]
DPI=[]

r = sr.Recognizer()
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', 'mb-es2')
engine.setProperty('rate',150)

while True:
   
    call(["fswebcam", "--no-banner", "-r", "640x480", "prueba1.jpg"])
    img = cv2.imread("prueba1.jpg")
    img_gs = cv2.imread('prueba1.jpg', cv2.IMREAD_GRAYSCALE)


    nombre = img_gs[0:80, 370:700]
    contrast_nombre = cv2.addWeighted(nombre, 0.5, np.zeros(nombre.shape, nombre.dtype), 0, 0)
    cv2.imwrite('nombre.jpg', contrast_nombre)
    text_nombre = pytesseract.image_to_string(contrast_nombre)

    apellido = img_gs[80:150, 350:700]
    contrast_apellido = cv2.addWeighted(apellido, 0.5, np.zeros(apellido.shape, apellido.dtype), 0, 0)
    cv2.imwrite('apellido.jpg', contrast_apellido)
    text_apellido = pytesseract.image_to_string(contrast_apellido)

    dpi = img_gs[0:65, 0:400]
    contrast_dpi = cv2.addWeighted(dpi, 0.5, np.zeros(dpi.shape, dpi.dtype), 0, 0)
    cv2.imwrite('dpi.jpg', contrast_dpi)
    text_dpi = pytesseract.image_to_string(contrast_dpi)

    fecha = img_gs[300:375, 370:650]
    contrast_fecha = cv2.addWeighted(fecha, 0.8, np.zeros(fecha.shape, fecha.dtype), 0, 0)
    cv2.imwrite('fecha.jpg', contrast_fecha)
    text_fecha = pytesseract.image_to_string(contrast_fecha)

    text_nombre= re.findall(r'[A-Z]+', text_nombre, re.M)
    print(text_nombre)
    if len(text_nombre) != 0:
        if text_nombre[0] == "NOMBRE":
            text_nombre.pop(0)
    nombre = " ".join(text_nombre)
    print(nombre)
       
    text_apellido= re.findall(r'[A-Z]+', text_apellido, re.M)
    apellido = " ".join(text_apellido)
    print(apellido)
   
    def edad(fdpi, fa):
    #dia int
        d = re.search(r'\d{2}', fdpi)
        dia = int(d[0])

    #mes string
        m = re.search(r'\D{3}', fdpi)
        mes = str(m[0])

    #año int
        a = re.findall(r'\d{4}', fdpi)
        agno = int(a[0])

    #fecha actual-desgloce
        faa = re.findall(r'\d{4}', fa)
        fam__ = re.findall(r'-\d{2}-', fa)
        fam_ = str(fam__[0])
        fam = re.findall(r'\d{2}', fam_)
        fad__ = re.findall(r'-\d{2}$', fa)
        fad_ = str(fad__[0])
        fad = re.findall(r'\d{2}', fad_)
        Aactual = int(faa[0])
        Mactual = int(fam[0])
        Dactual = int(fad[0])

    #meses
        if mes == "ENE":
            mes_t = "enero"
            mes_n = 1
        elif mes == "FEB":
            mes_t = "febrero"
            mes_n = 2
        elif mes == "ENE":
            mes_t = "enero"
            mes_n = 1
        elif mes == "MAR":
            mes_t = "marzo"
            mes_n = 3
        elif mes == "ABR":
            mes_t = "abril"
            mes_n = 4
        elif mes == "MAY":
            mes_t = "mayo"
            mes_n = 5
        elif mes == "JUN":
            mes_t = "junio"
            mes_n = 6
        elif mes == "JUL":
            mes_t = "julio"
            mes_n = 7
        elif mes == "AGO":
            mes_t = "agosto"
            mes_n = 8
        elif mes == "SEP":
            mes_t = "septiembre"
            mes_n = 9
        elif mes == "OCT":
            mes_t = "octubre"
            mes_n = 10
        elif mes == "NOV":
            mes_t = "noviembre"
            mes_n = 11
        elif mes == "DIC":
            mes_t = "diciembre"
            mes_n = 12
        else:
            pass

    #resta de años
        rst = Aactual - agno

    #condicionales de años cumplidos hasta la fecha
        if mes_n <= Mactual:
            if dia <= Dactual:
                dato = rst
            else:
                dato = rst - 1
        else:
            dato = rst - 1
        return dato
   
   
   
   
   
   
    text_fecha= re.findall(r'\d\d[A-Z]+\d\d\d\d', text_fecha, re.M)
    print(text_fecha)
    fecha = " ".join(text_fecha)
   
   
    text_dpi= re.findall(r'[0-9]+\s[0-9]+\s[0-9]+', text_dpi, re.M)
    dpi = " ".join(text_dpi)
    print(dpi)
    if(dpi != "" and nombre != "" and fecha != "" and apellido != ""):
        string = "Bienvenido " + nombre + " " + apellido+", con número de dpi: " + dpi
        print(string)
        engine.say(string)
        engine.runAndWait()
        fecha_actual = str(date.today())
        edad_actual = str(edad(fecha,fecha_actual))
        print(edad_actual)
        Nombre.append(nombre)
        Apellido.append(apellido)
        Edad.append(edad_actual)
        DPI.append(dpi)


        mic = sr.Microphone()
        with mic as source:
            print('Iniciando programa...')
            engine.say("¿Primera o segunda dosis?")
            engine.runAndWait()
            print('Grabando audio...')
            audio = r.record(source, offset=2,duration=4)
        try:
            data = r.recognize_google(audio, language='es-GT')
            print(data)


            if data == "primera":
                engine.say("Primera dosis")
                engine.say("diríjase al módulo 1")
                Dosis.append(data)
                tipo.append("No aplica")
                engine.runAndWait()
                engine.say("Puede retirar su DPI, muchas gracias")
                engine.runAndWait()
            elif data == "Apagar programa":
                engine.say("Apagando sistema de gestión...")
                engine.runAndWait()
                break
            elif data == "segunda":
                engine.say("Segunda dosis")
                engine.say("¿Que tipo de vacuna")
                engine.say("se aplicó?")
                engine.runAndWait()
                Dosis.append(data)
               
                with mic as source:
                    print('Grabando audio...')  
                    audio = r.listen(source, phrase_time_limit=2)
                try:
                    vacuna = r.recognize_google(audio, language='es-GT')
                    print(vacuna)
                    if vacuna == "sputnik":
                        engine.say("Tipo de vacuna:")
                        engine.say("spuutnik")
                        engine.say("diríjase al módulo 2")
                        tipo.append(vacuna)
                        engine.runAndWait()
                    elif vacuna == "moderna":
                        engine.say("Tipo de vacuna:")
                        engine.say("moderna")
                        engine.say("diríjase al módulo 2")
                        tipo.append(vacuna)
                        engine.runAndWait()
                    elif vacuna == "pfizer":
                        engine.say("Tipo de vacuna:")
                        engine.say("fai zer")
                        engine.say("diríjase al módulo 2")
                        tipo.append(vacuna)
                        engine.runAndWait()
                        time.sleep(4)
                    elif vacuna == "astrazeneca":
                        engine.say("Tipo de vacuna:")
                        engine.say("astrazeneca")
                        engine.say("diríjase al módulo 2")
                        tipo.append(vacuna)
                        engine.runAndWait()
                        time.sleep(4)
                    elif vacuna == "otra":
                        engine.say("diga su tipo de vacuna")
                        engine.runAndWait()
                        with mic as source:
                            print('Grabando audio...')
                            audio = r.record(source, offset=0,duration=3)
                            otra = r.recognize_google(audio, language='es-GT')
                            print(otra)
                            engine.say("Tipo de vacuna:")
                            engine.say(r.recognize_google(audio, language='es-GT'))
                            tipo.append(otra)
                            engine.say("Por favor aguarde unos minutos, alguien le vendrá a dar apoyo")
                            engine.runAndWait()
                            print(data + " dosis")
                            print(otra)
                            engine.runAndWait()
                            time.sleep(4)
                    engine.say("Puede retirar su DPI, muchas gracias")
                    engine.runAndWait()
                except sr.UnknownValueError: # error: recognizer does not understand
                    engine.say('No te puedo entender')
                    engine.runAndWait()
                    Nombre.pop()
                    Apellido.pop()
                    Edad.pop()
                    DPI.pop()
                    time.sleep(4)

             
            else:
                engine.say("Esa opción no se encuentra disponible")
                engine.runAndWait()
                Nombre.pop()
                Apellido.pop()
                Edad.pop()
                DPI.pop()
                Dosis.pop()
        except sr.UnknownValueError: # error: recognizer does not understand
                    engine.say('No te puedo entender')
                    engine.runAndWait()
                    Nombre.pop()
                    Apellido.pop()
                    Edad.pop()
                    DPI.pop()
                    Dosis.pop()
                    time.sleep(4)

        ba = {'Nombres': Nombre,
              'Apellidos': Apellido,
              'Edad': Edad,
              'DPI': DPI,
              'No. de Dosis': Dosis,
              'Tipo de Vacuna': tipo}

        df = pd.DataFrame(ba)
        escritor = pd.ExcelWriter('BasedeDatos.xlsx', engine='xlsxwriter')
        df.to_excel(escritor, sheet_name="hoja1", index=False)
        escritor.save()
    else:
        if(dpi != "" or nombre != "" or fecha != "" or apellido != ""):
            engine.say('Coloque su dpi correctamente')
            engine.runAndWait()
        else:    
            engine.say('Coloque su dpi')
            engine.runAndWait()
    time.sleep(9)