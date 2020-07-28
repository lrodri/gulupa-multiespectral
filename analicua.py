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

#cv2.namedWindow('rezima1',cv2.WINDOW_NORMAL)
#cv2.namedWindow('rezima2',cv2.WINDOW_NORMAL)
#cv2.namedWindow('filtrado figuras',cv2.WINDOW_NORMAL)
##cv2.namedWindow('imainv',cv2.WINDOW_NORMAL)
cv2.namedWindow('imaseg',cv2.WINDOW_NORMAL)


def cuadro(frimagenf):
    """ Filtra la imagen almacenada en la funcion segmf(), la cual, entrega una imagen segmentada, con algunos puntos de ruido"""
    filC , colC, ch= frimagenf.shape
    
    _,th=cv2.threshold(frimagenf, 41,255,cv2.THRESH_BINARY)
 
    kernel=np.ones((2,2),np.uint8)
    imainv=cv2.bitwise_not(th)
    closing = cv2.morphologyEx(imainv, cv2.MORPH_CLOSE, kernel)
    median = cv2.medianBlur(imainv,7)
    cuared=np.ones([filC,colC],np.uint8)
    for i in range(filC):
        for j in range (colC):
            if median[i ,j,0]==255 and median[i ,j,1]==255 and median[i ,j,2]==255:
                cuared[i,j]=255;
            else:
                cuared[i,j]=0;
    cv2.imshow('cuared',cuared)
    kernelocua  =  np.ones((9,9), np.uint8 )
    opencua = cv2.morphologyEx(cuared, cv2.MORPH_OPEN, kernelocua)
    kernelccua  =  np.ones((5,5),np.uint8)
    closingcua = cv2.morphologyEx(opencua,cv2.MORPH_CLOSE, kernelccua)
    cannycua = cv2.Canny(closingcua, 20, 200)
    (contor,_)= cv2.findContours(cannycua.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    areacu1=[]
    for contcua in contor:
        areacu1.append(cv2.contourArea(contcua))
        
    return areacu1[0]

    
def main(argv1):
    
    imagen1=cv2.imread(sys.argv[1])
    Mcuadro1=cuadro(imagen1)
    print('El area del cuadrado en pixeles es:',int(Mcuadro1))

main(sys.argv[1])



cv2.waitKey(0)
