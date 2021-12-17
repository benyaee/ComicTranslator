import math
import numpy as np
import cv2
import re

#Based on Carlo Borella’s implementation
#See here https://towardsdatascience.com/remove-text-from-images-using-cv2-and-keras-ocr-24e7612ae4f4

def midpoint(x1, y1, x2, y2):
    x_mid = int((x1 + x2)/2)
    y_mid = int((y1 + y2)/2)
    return (x_mid, y_mid)

def boundRect(vert):
    out= []
    for x in vert:
        x = x.replace("("," ")
        x = x.replace(")"," ")
        chunks = x.split(',')
        out.append(chunks)
    return out

def inpaint(filename,vert):
    img = cv2.imread(filename)
    x0=int(vert[0][0])
    x1=int(vert[1][0])
    x2=int(vert[2][0])
    x3=int(vert[3][0])
    y0=int(vert[0][1])
    y1=int(vert[1][1])
    y2=int(vert[2][1])
    y3=int(vert[3][1])

    x_mid0, y_mid0 = midpoint(x1, y1, x2, y2)
    x_mid1, y_mi1 = midpoint(x0,y0,x3,y3)
    thickness = int(math.sqrt( (x2 - x1)**2 + (y2 - y1)**2 ))
    mask = np.zeros(img.shape[:2], dtype="uint8")
    cv2.line(mask, (x_mid0, y_mid0), (x_mid1, y_mi1), 255, thickness)
    masked = cv2.bitwise_and(img, img, mask=mask)
    #cv2.imwrite("masked.png",masked)
    img_inpainted = cv2.inpaint(img, mask, 7, cv2.INPAINT_NS)
    cv2.imwrite("temp.png",img_inpainted)
    return "temp.png"
