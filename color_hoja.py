####
# Realizado por: Santiago Alejandro Trujillo Fandiño
# Fecha: 9 de julio de 2020
# Version: 1.0
# Proyecto: Implementacion de un sistema capaz de identificar el cambio de color en la hoja de gulupa
#conforme a la presencia o ausencia de nitrogeno mediante el procesamiento de imagenes RGB.
####

import numpy as np
from matplotlib import pyplot as plt
import cv2
import sys
import argparse
import glob
from math import sqrt 
#############
####
####
def kill(imagen):
  # Normalizar ventanas 
  cv2.namedWindow('imagen',cv2.WINDOW_NORMAL)
  cv2.namedWindow('imabgr',cv2.WINDOW_NORMAL)
  cv2.namedWindow('mascara',cv2.WINDOW_NORMAL)
  cv2.namedWindow('closingho',cv2.WINDOW_NORMAL)
  cv2.namedWindow('openingcua',cv2.WINDOW_NORMAL)
  cv2.namedWindow('imaseg',cv2.WINDOW_NORMAL)
  cv2.namedWindow('median',cv2.WINDOW_NORMAL)
  cv2.namedWindow('cannyseg',cv2.WINDOW_NORMAL)
  ####
  ####
  # Cambio de espacio de color de RGB a BGR
  ####
  ####
  cv2.imshow('imagen',imagen)
  imabgr=cv2.cvtColor(imagen, cv2.COLOR_RGB2BGR)
  cv2.imshow('imabgr', imabgr)
  # Propiedades de la imagen, como se sabe la imagen es una matriz compuesta por filas columnas y canales donde cada uno de estos canales
  # son sus componentes respectivamente 
  fil , col, ch= imabgr.shape
  r,g,b = cv2.split(imagen)
  ####
  #Calculo de la media de cada componente
  meanr=np.mean(r)
  meang=np.mean(g)
  meanb=np.mean(b)
  print 'el valor medio de R es: {0:.2f}'.format(meanr)
  print 'el valor medio de G es: {0:.2f}'.format(meang)
  print 'el valor medio de B es: {0:.2f}'.format(meanb)
  ####
  #Calculo de la varianza de cada componente
  varianzar=np.var(r)
  varianzag=np.var(g)
  varianzab=np.var(b)
  print 'el valor de la varianza de R es: {0:.2f}'.format(varianzar)
  print 'el valor de la varianza de G es: {0:.2f}'.format(varianzag)
  print 'el valor de la varianza de B es: {0:.2f}'.format(varianzab)
  ####
  #Calculo de la descviacion estandar
  desvestr=np.std(r)
  desvestg=np.std(g)
  desvestb=np.std(b)
  print 'el valor de la desviacion estandar de R es: {0:.2f}'.format(desvestr)
  print 'el valor de la desviacion estandar de G es: {0:.2f}'.format(desvestg)
  print 'el valor de la desviacion estandar de B es: {0:.2f}'.format(desvestb)
  ####
  # Aplicamos una segmentacion por umbralizacion directamente sobre la imagen BGR, esto con el fin 
  # de distinguir de una manera mas facil los dos objetos de interes, en este caso la hoja y el cuadrado; los vales de umbralizacion
  # utilizados se observaron mediante la herramienta editora de imagenes GIMP
  ####
  ####
  _,mascara=cv2.threshold(imabgr,170,255,cv2.THRESH_BINARY)
  cv2.imshow('mascara',mascara)
  ####
  ####
  # Luego de aplicar la umbralizacion y observar que los objetos de interes pueden seperarse individualmente, se realiza una segmentacion
  # sobre la imagen resultante y se separan los objetos de interes  
  ####
  ####
  #Segmentacion solo de la hoja
  imasegho=np.ones([fil,col],np.uint8)
  for i in range(fil):
   for j in range (col):
    if mascara[i ,j,0]==0 and mascara[i ,j,1]==0 and mascara[i ,j,2]==0:
     imasegho[i,j]=255;
    else:
     imasegho[i,j]=0;
  ####
  ####
  # se realiza la trasformacion de Caracteristicas morfologicas como erode-open y closin, herramientas que se 
  # uilizan con el fin de mejorar la calidad de la imagen y limpiarla del ruido que quede luego de la segmentacion
  ####
  ####
  #EROSION hoja 
  kernel = np.ones((3,3),np.uint8)
  erosionho = cv2.erode(imasegho,kernel,iterations = 1)
  ####
  #OPENING hoja quita puntos blancos fuera de lo segmentado 
  openingho = cv2.morphologyEx(erosionho, cv2.MORPH_OPEN, kernel)
  ####
  #Closing hoja quita puntos negros dentro de lo segmentado 
  kernelclos= np.ones((3,3),np.uint8)
  kernelcloss= np.ones((7,7),np.uint8)
  closingho = cv2.morphologyEx(openingho, cv2.MORPH_CLOSE, kernelclos)
  closingho = cv2.morphologyEx(openingho, cv2.MORPH_CLOSE, kernelcloss)
  cv2.imshow('closingho',closingho)
  ####
  ####
  # Pixeles Blancos en la hoja: esto se realiza con el fin de saber la cantidad de pixeles blancos que contiene la segmentacion de la hoja
  # para mas adelante utilizar este valor con el fin de encontrar el area afectada de la hoja
  blancosho=0;
  for i in range(fil):
    for j in range (col):
      if closingho[i ,j]==255:
      	blancosho=blancosho+1;
  print'la cantidad de pixeles blancos de la hoja son:' + str(int(blancosho))
  ####
  ####
  #Seleccion de borde hoja: Esta funcion permite dibujar el contorno exterior de la hoja segmentada anteriormente
  cannyho = cv2.Canny(closingho, 100, 150,)
  cv2.imshow("cannyclo", cannyho)
  ####
  #Encontrar Contornos hojas: contoursho realiza una busqueda de figuras que se encuentren en la imagen segmentada, donde cuyo proposito 
  # es hallar el area de cada una estas. 
  (contoursho,_) = cv2.findContours(cannyho.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
  #numero de formas
  #print'numero de formas: {0:.2f}'.format(len(contoursho))
  ####
  ####
  areaho = []
  perimeterho = []
    #Dibujar Contornos: Parte fundamental del codigo donde el condicional for se encarga de asignar a la 
  # variable cntho los valores dados por contoursho; en el caso de que contoursho encuentre mas de una forma,
  # cntho almacena y agrupa cada valor en dos listas(array) una es el area y otra el perimetro, cntho organizar los valores de areas y perimetros 
  # dados por contoursho para luego hallar el valor maximo dentro de estas listas, ese valor maximo sera el area y perimetro de la hoja
  # 
  ####
  for cntho in contoursho:
      perimeterho.append(cv2.arcLength(cntho,True))
      perimetromaxi = max(perimeterho)
      areaho.append(cv2.contourArea(cntho))
      areamaxima = max(areaho)
  areareal=round(areamaxima)
  perimeterreal=round(perimetromaxi)
  print 'el area de la hoja en pixeles es:  {0:.2f}'.format(areareal)
  print 'el perimetro de la hoja en pixeles es:  {0:.2f}'.format(perimeterreal)
  ####
  # Puntos Extremos
  ####
  #superior
  i = 0
  j = 0
  superiorho = []
  romper = 0
  for i in range(fil):
    for j in range (col):
      if closingho[i ,j]==255:
      	superiorho=[i,j]
        romper = 1
        break
    if romper==1:
     break
  #print'la posicion superior es :', superiorho 
  ####
  #inferior
  i = fil
  j = col
  romper = 0
  inferiorho = []
  for i in range(fil-1,0,-1):
    for j in range (col-1,0,-1):
      if closingho[i,j]==255:
      	inferiorho = [i,j]
        romper = 1
        break
    if romper==1:
     break
  #print'la posicion inferior es :', inferiorho
  ####
  #izquierda
  romper = 0
  izquierdoho = []
  for j in range(col):
    for i in range (fil):
      if closingho[i,j]==255:
      	izquierdoho = [i,j]
        romper = 1
        break
    if romper==1:
     break
  #print 'la posicion izquierda es :', izquierdoho
  ####
  #derecho
  i = fil
  j = col
  romper = 0
  derechoho = []
  for j in range(col-1,0,-1):
    for i in range (fil-1,0,-1):
      if closingho[i,j]==255:
      	derechoho = [i,j]
        romper = 1
        break
    if romper==1:
     break
  #print'la posicion derecha es :', derechoho 
  ####
  ####
  # Puntos extremos: al ser la hoja una forma irregular se busca hallar los puntos extremos de la hoja
  # de la izquierda la derecha, arriba y abajo, para luego mediante la ecuacion de la distancia entre dos puntos hallar el largo y
  # ancho de la hoja
  ####
  #largo de la hoja
  largoho=sqrt(((inferiorho[0]-superiorho[0])**2)+((inferiorho[1]-superiorho[1])**2))
  largoho=round(largoho)
  #if largoho < 10:
   # largoho = largoho + 550
  print 'el largo de la hoja en pixeles es: ', largoho
  ####
  # Ancho de la hoja en pixeles
  anchoho=sqrt(((izquierdoho[0]-derechoho[0])**2)+((izquierdoho[1]-derechoho[1])**2))
  anchoho=round(anchoho)
  #if anchoho < 10:
   # anchoho = anchoho + 490
  print 'el ancho de la hoja en pixeles es: ', anchoho
  ####
  ####
  #segmentacion imagen para visualizar el estado de nitrogeno en la hoja: segmentacion de la imagen en bgr donde se busca 
  #mediante condicionales de las componentes de la imagen segmentar el area que muestre la decoloracion esta area se resalta de color blanco
  imaseg=np.ones([fil,col],np.uint8)
  for i in range(fil):
    for j in range (col):
        if imabgr[i,j,0]>=90 and imabgr[i,j,0]<=190 and imabgr[i,j,2]>=30 and imabgr[i,j,2]<=80 : #90,190  ima[i,j]>=85 and r[i,j]<=190
           imaseg[i,j]=255
        else:
            imaseg[i,j]=0; 
  cv2.imshow('imaseg',imaseg)
  ####
  ####
  # Conteo de pixeles blancos: En esta seccion se realiza el conteo de pixeles blancos dentro de la imagen segmentada ya que estos
  # son los que identifican la zona de decoloracion en la hoja, la varibale blancoshoseg se utiliza mas adelante con el proposito 
  # de hallar el area afectada de la hoja en cm
  blancoshoseg=0;
  for i in range(fil):	
    for j in range (col):
      if imaseg[i,j]==255:
       blancoshoseg=blancoshoseg+1;
  print'la cantidad de pixeles blancos de la hoja seg son:' + str(int(blancoshoseg))
  ####
  ####
  # Se realiza una umbralizacion a la imagen segmentada con el fin de resaltar y diferenciar mas los pixeles blancos con los negros
  _,mask=cv2.threshold(imaseg,120,240,cv2.THRESH_BINARY)
  ####
  ####
  #Filtros: El filtro de media permite mejorar la calidad de la imagen 
  ####
  median=cv2.medianBlur(mask,3)
  cv2.imshow('median',median)
  ####
  ####
  #Bordes Se usa de nuevo canny para poder dibujar el contorno externo de la hoja y el contorno interno que serian las areas 
  #que presenten alguna afectacion en la  hoja 
  cannyseg = cv2.Canny(median, 50, 150,) #50,150
  cv2.imshow("cannyseg", cannyseg)
  ####
  ####
  #Segmentacion solo del cuadrado: Se separa el cuadrado de la imagen debido a que este funciona como referencia en cm de un area, largo
  #y perimetro conocido
  imasegcua=np.ones([fil,col],np.uint8)
  for i in range(fil):
    for j in range (col):
      if mascara[i ,j ,0]==0 and mascara[i ,j,1]==0 and mascara[i ,j,2]>=253:
       imasegcua[i,j]=255;
      else:
       imasegcua[i,j]=0;
  ####
  ####
  #Caracteristicas morfologicas erode-open
  #EROSION cuadrado
  kernelcua = np.ones((7,7),np.uint8)
  erosioncua = cv2.erode(imasegcua,kernelcua,iterations = 1)
  ####
  #OPENING cuadrado
  openingcua = cv2.morphologyEx(erosioncua, cv2.MORPH_OPEN, kernel)
  cv2.imshow('openingcua',openingcua)
  ####
  ####
  #Pixeles blancos en el cuadrado
  blancoscua=0;
  for i in range(fil):
    for j in range (col):
      if imasegcua[i ,j]==255:
       blancoscua=blancoscua+1;
  #print'la cantidad de pixeles blancos del cuadrado son:' + str(int(blancoscua))
  ####
  ####
  #Seleccion borde del cuadrado
  cannycua = cv2.Canny(openingcua, 50, 150,)
  ####
  ####
  #Encontrar Contornos cuadrado
  (contourscua,_) = cv2.findContours(cannycua.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
  ####
  #numero de formas
  #print'numero de formas: {0:.2f}'.format(len(contourscua))
  ####
  ####
  areacua = []
  perimetercua = []
  superioor = []
  inferioor = []
  derechoo = []
  izquierdoo = []
  #
  #Dibujar Contornos
  for cntcua in contourscua:
    perimetercua.append(cv2.arcLength(cntcua,True))
    perimaxcua = max(perimetercua)
    areacua.append(cv2.contourArea(cntcua))
    areamaximacua = max(areacua)
  areacua=round(areamaximacua)
  perimetercua=round(perimaxcua)
  ####
  ####
  print 'el area del cuadro en pixeles es:  {0:.2f}'.format(areacua)
  print 'el perimetro del cuadro en pixeles es:  {0:.2f}'.format(perimetercua)
  ####
   # Puntos Extremos
  ####
  #superior
  i = 0
  j = 0
  superiorcua = []
  romper = 0
  for i in range(fil):
    for j in range (col):
      if openingcua[i ,j]==255:
      	superiorcua=[i,j]
        romper = 1
        break
    if romper==1:
     break
  #print'la posicion superior es :', superiorcua 
  ####
  #inferior
  i = fil
  j = col
  romper = 0
  inferiorcua = []
  for i in range(fil-1,0,-1):
    for j in range (col-1,0,-1):
      if openingcua[i,j]==255:
      	inferiorcua = [i,j]
        romper = 1
        break
    if romper==1:
     break
  #print'la posicion inferior es :', inferiorcua
  ####
  #izquierda
  romper = 0
  izquierdocua = []
  for j in range(col):
    for i in range (fil):
      if openingcua[i,j]==255:
      	izquierdocua = [i,j]
        romper = 1
        break
    if romper==1:
     break
  #print 'la posicion izquierda es :', izquierdocua
  ####
  #derecho
  i = fil
  j = col
  romper = 0
  derechocua = []
  for j in range(col-1,0,-1):
   for i in range (fil-1,0,-1):
     if openingcua[i,j]==255:
       derechocua = [i,j]
       romper = 1
       break
   if romper==1:
    break
  #print'la posicion derecha es :', derechocua 
  
  ####
  #Largo del cuadrado en pixeles
  largocua=sqrt(((superiorcua[0]-inferiorcua[0])**2)+((superiorcua[1]-inferiorcua[1])**2))
  largocua=round(largocua)
  print 'el largo del cuadrado en pixeles es:', largocua
  ####
  # Ancho del cuadrado en pixeles
  anchocua=sqrt(((derechocua[0]-izquierdocua[0])**2)+((derechocua[1]-izquierdocua[1])**2))
  anchocua=round(anchocua)
  print 'el ancho del cuadrado en pixeles es: ', anchocua
  ####
  ####
  #Area del cuadrado en cm
  areacuadrado= 25
  #print 'el area del cuadrado en centimetros cuadrados es:', areacuadrado
  ####
  #Perimetro del cuadrado en cm
  perimetrocuadrado= 20
  #print 'el perimetro del cuadrado en centimetros es:', perimetrocuadrado
  ####
  #ancho del cuadrado
  anchocuadrado=5
  #print 'el ancho del cuadrado en cm es:', anchocuadrado
  ####
  #largo del cuadrado
  largocuadrado=5
  #print 'el largo del cuadrado en cm es:', largocuadrado
  ####
  ####
  #Calculo del area de la hoja en cmsuperiorho:  (400, 669)
  centimetrosho=areareal*areacuadrado
  centimetrosho=round(centimetrosho/areacua)
  #if centimetrosho>1000:
  #  centimetrosho=centimetrosho/10000
  print 'el area de la hoja en centimetros cuadrados es: {0:.0f}'.format(centimetrosho)
  ####
  #Calculo del perimetro de la hoja cm
  perimetroho=perimeterreal*perimetrocuadrado
  perimetroho= round( perimetroho/perimetercua)
  print 'el perimetro de la hoja en centimetros es: {0:.2f}'.format(perimetroho)
  ####
  #Ancho de la hoja en cm
  ancmho=anchoho*anchocuadrado
  ancmho=round(ancmho/anchocua)
  #if ancmho>100:
  # ancmho=ancmho/10
  print 'el ancho de la hoja en cm es:', ancmho
  ####
  #largo de la hoja en cm
  lacmho=largoho*largocuadrado
  lacmho=round(lacmho/largocua)
  #if lacmho>100:
  # lacmho=lacmho/10
  print 'el largo de la hoja en cm es:', lacmho
  ####
  #Area afectada de la hoja
  areainfectada=(blancoshoseg*centimetrosho)
  areainfectada=round(areainfectada/blancosho)
  #if areainfectada>1000:
  #  areainfectada=areainfectada/10000
  print 'El area afectada de la hoja en cm cuadrados es: {0:.0f}'.format(areainfectada)
  ####
  # Porcentaje de area afectada en la hoja
  porcentajem=areainfectada*100
  porcentajem=round(porcentajem/centimetrosho)
  print 'El porcentaje de la hoja que presenta deficiencia de N es el : {0:.0f}'.format(porcentajem)
  ####
  ####
####
def main (argv):
#Cargar Imagen
  iimagen=cv2.imread(sys.argv[1])
  width, height = 1080, 720
  iimagen=cv2.resize(iimagen,(width,height), interpolation=cv2.INTER_LINEAR)
  kill(iimagen)
main(sys.argv[1]) 
####
####
cv2.waitKey(0)
cv2.destroyAllWindows()
