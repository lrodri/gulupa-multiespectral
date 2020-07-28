"""
Realizado por: Faryd Alejandro Peñuela González
Fecha: 24 de julio del 2020
Versión: 1.0.0.
Proyecto: IMPLEMENTACION DE UN SISTEMA CAPAZ DE CALCULAR EL AREA FOLIAR DE UNA PLANTA DE GULUPA, A PARTIR DE IMAGENES QUE REPRESENTEN DOS DIMENSIONES DE LA PLANTA, MEDIANTE TECNICAS DE PROCESAMIENTO DE IMAGENES

Nota: No agregar tildes

"""

import numpy as np
from PIL import Image
from matplotlib import pyplot as plt
import cv2
import sys
import math

cv2.namedWindow('rezima1',cv2.WINDOW_NORMAL)
cv2.namedWindow('rezima2',cv2.WINDOW_NORMAL)
#cv2.namedWindow('filtrado figuras',cv2.WINDOW_NORMAL)
cv2.namedWindow('segcua',cv2.WINDOW_NORMAL)
cv2.namedWindow('imaseg',cv2.WINDOW_NORMAL)

def resize(rimagen1, rimagen2):
    """ Funcion para redimensionar la imágen a 1080X720 pixeles"""
    width = 1080
    height = 720
    dim = (width, height)
    resized1 = cv2.resize(rimagen1, dim)
    cv2.imshow('rezima1',resized1)
    resized2 = cv2.resize(rimagen2, dim)
    cv2.imshow('rezima2',resized2)
    cv2.imwrite('resize.jpg',resized1)
    cv2.imwrite('resize.jpg',resized2)
    
    return (resized1, resized2)


def Igrisf(fimagen1, fimagen2):
   """ funcion para convertir las imagenes redimensionadas en escala de grises"""
    imagris1=cv2.cvtColor(fimagen1, cv2.COLOR_RGB2GRAY)
    imagris2=cv2.cvtColor(fimagen2, cv2.COLOR_RGB2GRAY)
    cv2.imwrite('imagris.jpg',imagris1)
    return (imagris1, imagris2)

def segmf(ffimagen):

    """ Llama el valor almacenado en la funcion Igris, calcula la cantidad de pixeles con las que cuenta la imagen. Posteriormente, segmenta la imagen, utilizando la umbralizacion como camino; cambia pixel por pixel de la imagen en gris asignandole 0 o 255 dependiendo el umbral propuesto. """
    fils , cols= ffimagen.shape
    countB=0;
    countN=0;
    
    imaseg=np.ones([fils,cols],np.uint8)

    for i in range(fils):
        for j in range (cols):
            if ffimagen[i,j]<=41:
                imaseg[i,j]=0;
            else:
                if ffimagen[i,j]>=140 and ffimagen[i,j]<=255:
                    imaseg[i,j]=0;
                    countN=countN+1;
                else:0
                    imaseg[i,j]=255;
                    countB=countB+1;
    cv2.imwrite('imaseg.jpg',imaseg)
    cv2.imshow('imaseg',imaseg)
    print('El area foliar de la planta en pixeles es', countB)
    return (imaseg, countB)
    

def cuadro(frimagenf):
    """ Filtra la imagen almacenada en la funcion segmf(), la cual, entrega una imagen segmentada, con algunos puntos de ruido
    Distinge el cuadrado de contraste de la imagen y calcula el area correspondiente a dicha figura
    
    """
    filC , colC, ch= frimagenf.shape
    
    _,th=cv2.threshold(frimagenf, 41,255,cv2.THRESH_BINARY)
    cv2.imwrite('threshold.jpg',th)
    kernel=np.ones((2,2),np.uint8)
    imainv=cv2.bitwise_not(th)
    cv2.imwrite('imainv.jpg',imainv)
    closing = cv2.morphologyEx(imainv, cv2.MORPH_CLOSE, kernel)
    cv2.imwrite('closing1.jpg',closing)
    median = cv2.medianBlur(imainv,7)
    cv2.imwrite('median.jpg',median)
    cuared=np.ones([filC,colC],np.uint8)
    for i in range(filC):
        for j in range (colC):
            if median[i ,j,0]==255 and median[i ,j,1]==255 and median[i ,j,2]==255:
                cuared[i,j]=255;
            else:
                cuared[i,j]=0;
    cv2.imwrite('cuared.jpg',cuared)
    kernelocua  =  np .ones((9,9), np . uint8 )
    opencua = cv2.morphologyEx(cuared, cv2.MORPH_OPEN, kernelocua)
    kernelccua  =  np.ones((5,5),np.uint8)
    closingcua = cv2.morphologyEx(opencua,cv2.MORPH_CLOSE, kernelccua)
    cv2.imwrite('closingcua.jpg',closingcua)
    cannycua = cv2.Canny(closingcua, 20, 200)
    (contor,_)= cv2.findContours(cannycua.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    areacu1=[]
    for contcua in contor:
        areacu1.append(cv2.contourArea(contcua))
    maxarea1 = max(areacu1) 
    cv2.imshow('segcua',closingcua)
    print('area del cuadro en pixeles es:', int(maxarea1))
    return (int(maxarea1), closingcua)
    
def calc(acu, apla):
    """ Calcula el area foliar de la planta en metros cuadrados utilizando la resolucion de la imagen y la escalabilidad a la que se encuentra el cuadrado"""
    Raiz_cuad_px=math.sqrt(acu)     
    lado_px2cm=Raiz_cuad_px/28.346
    ladoxlado=lado_px2cm**2
    cuadro_veces=400/ladoxlado
        
    Area_planta_cm=((apla*400.0)/acu)/cuadro_veces
    Area_planta_m=Area_planta_cm/100
    return Area_planta_m
    
def main(argv1, argv2):
    """ Funcion principal; ejecuta las funciones internas con propositos unicos"""
    imagen1=cv2.imread(sys.argv[1])
    imagen2=cv2.imread(sys.argv[2])
    
    Mresize1, Mresize2=resize(imagen1, imagen2)
    Mgris1, Mgris2=Igrisf(Mresize1, Mresize2)
    
    Mcuadro1, imacua1=cuadro(Mresize1)
    #cv2.waitKey(0)
    Mcuadro2, imacua2=cuadro(Mresize2)
    cv2.imwrite('cuasegF.jpg',imacua1)
    cv2.imwrite('cuasegV.jpg',imacua2)
    
    Imaretf1 , Arpla1 = segmf(Mgris1)
    Imaretf2 , Arpla2 = segmf(Mgris2)
    
    cv2.imwrite('plasegF.jpg',Imaretf1)
    cv2.imwrite('plasegV.jpg',Imaretf2)
    
    Ac1= calc(Mcuadro1, Arpla1)
    Ac2= calc(Mcuadro2, Arpla2)
    
    return Ac1, Ac2
    
A, B = main(sys.argv[1], sys.argv[2])

print('El area real de la planta frontal es de {0:.2f} metros cuadrados'.format(A))
print('El area real de la planta lateral es de {0:.2f} metros cuadrados'.format(B))
#print (Igrisf._ cv2.imshow('imaseg',imaseg) cv2.imshow('imaseg',imaseg)_doc__)
#print (segmf.__doc__)
#print (filf.__doc__)

cv2.waitKey(0)
