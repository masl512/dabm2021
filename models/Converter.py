import os
import cv2
import csv
import numpy as np
import easygui
import pytesseract
import difflib

from models import Contours
from models.Contours import sort_contours
from models.Extract import extract, readHV, createHeaders

def convert():
    file = easygui.fileopenbox()
    # files = filedialog.askopenfilenames()
    directory = os.path.dirname(__file__)
    # directory = r'C:\Users\USUARIO\Documents\UNIVERSIDAD\DABM\Proyecto\data'
    texto = box_extraction(file,directory)
    # disp = Equipo(name,code,rs,brand,model,tipo,series,numAct)
    # disp.create()    
    return texto

def box_extraction(img_for_box_extraction_path, cropped_dir_path):   
    img = cv2.imread(img_for_box_extraction_path, 0)  # Read the image
    scale_percent = 80 # percent of original size
    width = int(img.shape[1] * scale_percent / 100)
    height = int(img.shape[0] * scale_percent / 100)
    dim = (width, height)  
    # resize image
    resized = cv2.resize(img, dim, interpolation = cv2.INTER_AREA)
    # resized = cv2.resize(img, (960,540))

    (thresh, img_bin) = cv2.threshold(resized, 150, 255, 
    cv2.THRESH_BINARY | cv2.THRESH_OTSU)  # Thresholding the image
    img_bin = 255-img_bin  # Invert the image
    cv2.imwrite("Image_bin.jpg",img_bin)

    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1,2)) # Operador morfol+ogico de apertura
    img_bin = cv2.morphologyEx(img_bin, cv2.MORPH_OPEN, kernel,iterations=1)

    # Defining a kernel length
    kernel_length = np.array(resized).shape[1]//120
    # A verticle kernel of (1 X kernel_length), which will detect all the verticle lines from the image.
    verticle_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, round(kernel_length*0.89)))
    # A horizontal kernel of (kernel_length X 1), which will help to detect all the horizontal line 
    # from the image.
    hori_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (kernel_length, 1))
    # A kernel of (3 X 3) ones.
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    # Morphological operation to detect verticle lines from an image
    img_temp1 = cv2.erode(img_bin, verticle_kernel, iterations=3)
    verticle_lines_img = cv2.dilate(img_temp1, verticle_kernel, iterations=3)
    cv2.imwrite("verticle_lines.jpg",verticle_lines_img)
    # Morphological operation to detect horizontal lines from an image
    img_temp2 = cv2.erode(img_bin, hori_kernel, iterations=3)
    horizontal_lines_img = cv2.dilate(img_temp2, hori_kernel, iterations=3)
    cv2.imwrite("horizontal_lines.jpg",horizontal_lines_img)
    # Weighting parameters, this will decide the quantity of an image to be added to make a new image.
    alpha = 0.5
    beta = 1.0 - alpha
    # This function helps to add two image with specific weight parameter to get a third image as summation of two image.
    img_final_bin = cv2.addWeighted(verticle_lines_img, alpha, horizontal_lines_img, beta, 0.0)
    img_final_bin = cv2.erode(~img_final_bin, kernel, iterations=2)
    (thresh, img_final_bin) = cv2.threshold(img_final_bin, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    # For Debugging
    # Enable this line to see verticle and horizontal lines in the image which is used to find boxes
    cv2.imwrite("img_final_bin.jpg",img_final_bin)
    # Find contours for image, which will detect all the boxes
    contours, hierarchy = cv2.findContours(img_final_bin, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    # cv2.drawContours(img_final_bin,contours,-1,(0,255,0),3)
    # cv2.imshow('image',img_final_bin)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    
    # print(contours)
    # Sort all the contours by top to bottom.
    (contours, boundingBoxes) = sort_contours(contours, method="top-to-bottom")
    idx = 0

    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
    text = []
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1,2))
    for c in contours:
    # Returns the location and width,height for every contour
        x, y, w, h = cv2.boundingRect(c)
        # If the box height is greater then 20, widht is >80, then only save it as a box in "cropped/" folder.
        if (w > 20 and h > 10) and w > 4*h:
            idx += 1

            new_img = resized[y-3:y+h+3, x-2:x+w]
            # cv2.imshow('image',new_img)
            # cv2.waitKey(0)
            # cv2.destroyAllWindows()            
            # # gray = cv2.cvtColor(new_img, cv2.COLOR_BGR2GRAY)
            
            blur = cv2.GaussianBlur(new_img,(3,3),0)
            # cv2.imshow('image',blur)
            # cv2.waitKey(0)
            # cv2.destroyAllWindows()            
            
            tresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
            # cv2.imshow('image',tresh)
            # cv2.waitKey(0)
            # cv2.destroyAllWindows()

            kernel = np.ones((1,1),np.uint8)
            dilation = cv2.dilate(tresh,kernel,iterations = 1)   
            # cv2.imshow('image',dilation)
            # cv2.waitKey(0)
            # cv2.destroyAllWindows()            
            
            kernel = np.ones((1,2),np.uint8)
            erosion = cv2.erode(dilation,kernel,iterations = 1)
            # cv2.imshow('image',erosion)
            # cv2.waitKey(0)
            # cv2.destroyAllWindows()            
            
            invert = 255 - erosion
            # cv2.imshow('image',invert)
            # cv2.waitKey(0)
            # cv2.destroyAllWindows()            

            custom_config = r'--oem 3 --psm 6'
            txt = pytesseract.image_to_string(invert,config= custom_config)
            print(txt)

            text.append(txt)
            # cv2.imwrite(cropped_dir_path+str(idx) + '.png', invert)
    matx = []
    for e in text:
        mod1 = e.replace('\n','')
        # print(mod1)
        mod2 = mod1.replace('\x0c','')
        # print(mod2)
        matx.append(mod2)
    
    return matx
            

    # # box_extraction("41.jpg", "./Cropped/")

def get_matches(matrix,refTitle):
    match = difflib.get_close_matches(refTitle,matrix)
    match = match[0]
    return match

def getData(refMatrix):
    # hdv = readHV('HV_BENEHEART_D6.csv')
    headers,values = extract(refMatrix)
    createHeaders(headers,values)

        
    

    #Extraer fecha de operación
    #Extraer vida util
    #Extraer fecha de vencimiento de garantía
    #Extraer periodicidad de mantenimiento
    #Extraer ultimo mantenimiento
    #Extraer los que tienen x
    #Extraer riesgo