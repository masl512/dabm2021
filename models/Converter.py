import os
import cv2
import numpy as np
import pytesseract
import difflib

from models import Contours
from models.Contours import sort_contours
from models.Extract import extract, readHV, createHeaders
from models.SortCont import sortContours

def convert(filename):
    directory = r'instance/htmlfi'
    file = os.path.join(directory,filename)
    texto = box_extraction(file,directory)  
    return texto

def box_extraction(img_for_box_extraction_path, cropped_dir_path):   
    img = cv2.imread(img_for_box_extraction_path, 0)  # Read the image
    scale_percent = 70 # percent of original size
    width = int(img.shape[1] * scale_percent / 100)
    height = int(img.shape[0] * scale_percent / 100)
    dim = (width, height)  
    # resize image
    resized = cv2.resize(img, dim, interpolation = cv2.INTER_AREA)
    # DETECTAR Y EXTRAER LÍNEAS DE LA IMAGEN
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
    # Sort all the contours by top to bottom.
    sortedBoxes = sortContours(contours)
    idx = 0
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
    text = []
    groups = []
    cont = 0
    coords = [0,0,0,0]
    for b in sortedBoxes:
    # Returns the location and width,height for every contour
        x = b[0]
        y = b[1]
        w = b[2]
        h = b[3]
    # If the box height is greater than 20, widht is >80, then only save it as a box in "cropped/" folder.
        if (w > 20 and h > 10 and h < 40) and w > 3*h:
            ncoords = b
            idx += 1        
            group = getCellGroup(coords,ncoords,resized)
            if group != None:
                groups.append(group)
            coords = b
    matx = [g for g in groups]
    return matx
            

def get_matches(refTitle,matrix):
    print(refTitle)
    match = difflib.get_close_matches(refTitle,matrix)
    print(match)
    match = match[0]
    return match

def getData(refMatrix):
    headers,values = extract(refMatrix)
    createHeaders(headers,values)
    return headers, values

def getCellGroup(coords,ncoords,resized):
    A = (coords[0],coords[1]) # Esquina superior izquierda de la celda anterior
    B = (coords[0]+coords[2],coords[1]) # Esquina superior derecha de la celda anterior
    C = (coords[0],coords[1]+coords[3]) # Esquina inferior izquierda de la celda anterior
    D = (coords[0]+coords[2],coords[1]+coords[3]) # Esquina inferior derecha de la celda anterior

    nA = (ncoords[0],ncoords[1]) # Esquina superior izquierda de la celda actual
    nB = (ncoords[0]+ncoords[2],ncoords[1]) # Esquina superior derecha de la celda actual
    nC = (ncoords[0],ncoords[1]+ncoords[3]) # Esquina inferior izquierda de la celda actual
    nD = (ncoords[0]+ncoords[2],ncoords[1]+ncoords[3]) # Esquina inferior derecha de la celda actual
    
    if (B <= nA and D <= nC) and (A[1] >= nA[1]-25 and  A[1] <= nA[1]+25):
        group = [coords,ncoords]
        x1 = group[0][0] 
        y1 = group[0][1] 
        w1 = group[0][2] 
        h1 = group[0][3] 
        testimg1 = resized[y1-3:y1+h1+3, x1-2:x1+w1]
        tit = getText(testimg1) 
        x2 = group[1][0] 
        y2 = group[1][1] 
        w2 = group[1][2] 
        h2 = group[1][3] 
        testimg2 = resized[y2-3:y2+h2+3, x2-2:x2+w2]  
        val = getText(testimg2) 
        g = (tit,val)
        return g
        #agrupo coords del titulo y coords del valor        

def getText(new_img):
    blur = cv2.GaussianBlur(new_img,(3,3),0)

    tresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1,2)) # Operador morfol+ogico de apertura
    openmorf = cv2.morphologyEx(tresh, cv2.MORPH_OPEN, kernel,iterations=1)

    kernel = np.ones((1,1),np.uint8)
    dilation = cv2.dilate(openmorf,kernel,iterations = 1)   

    kernel = np.ones((1,2),np.uint8)
    erosion = cv2.erode(dilation,kernel,iterations = 1)

    median = cv2.medianBlur(erosion,1)      

    invert = 255 - median

    custom_config = r'--oem 3 --psm 6'
    txt = pytesseract.image_to_string(invert,config= custom_config)
    mod1 = txt.replace('\n','')
    txt = mod1.replace('\x0c','')
    return txt  