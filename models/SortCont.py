import cv2
import pandas as pd


def sortContours(cnts):
    boundingBoxes = [cv2.boundingRect(c) for c in cnts]
    # print(boundingBoxes)
    df = pd.DataFrame(boundingBoxes, columns=['x','y','w','h'])
    # print(df)
    df.sort_values(by=['y','x'], inplace= True)
    boundingBoxes = df.values.tolist()
    # print(boundingBoxes)
    return boundingBoxes










    # contours_poly = [None]*len(contours)    
    # boundRect = [None]*len(contours)
    # for i, c in enumerate(contours):
    #     contours_poly[i] = contours[i]
    #     boundRect[i] = cv2.boundingRect(contours_poly[i])
    
    # for i in range(len(contours)):
    #     # color = (rng.randint(0,256), rng.randint(0,256), rng.randint(0,256))
    #     color = (0,0 ,255 )
    #     cv2.rectangle(resized, (int(boundRect[i][0]), int(boundRect[i][1])), \
    #       (int(boundRect[i][0]+boundRect[i][2]), int(boundRect[i][1]+boundRect[i][3])), color, 2)
    
    # cv2.imwrite('boxes.png', resized)    
    # # cv2.imshow('Contours', resized)
    # # cv2.waitKey(0)
    # # cv2.destroyAllWindows()      
    