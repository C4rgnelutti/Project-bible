#Project_bible_Version_1.1.4

import cv2
import os
import numpy as np

#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

def loadimages (path):
    return[os.path.join(path , f) for f in os.listdir(path) if f.endswith(".jpg")]

#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

Input = str(input("Set the directory from the images you want to effect:"))
Output = str(input("Set the directory for the new images:"))

#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

num = 0
filenames = (loadimages(Input))
for file in filenames:

    print("Loading Image...")
    Main_Image = cv2.imread(file , cv2.IMREAD_UNCHANGED)
    Grey_Image = cv2.imread(file , 0)

    #Center pixel:
    y = int((Main_Image.shape[0])/2)
    x = int((Main_Image.shape[1])/2)

    #Defining Verification amplitudes:
    Ay = int((Grey_Image.shape[0])*0.4)
    Ax = int((Grey_Image.shape[0])*0.2)

    #Auxiliar variables:
    Aprox_Line_Distance = int(((Grey_Image.shape[0])*0.7)/30) #30 is the amount of lines in the page
    Maximum_Intensity = 150

    #Auxiliar Lists:
    List1 = []
    List2 = []

    #Real shit:
    print("processing Image")
    for dy in range (y-Ay,y+Ay):
        if Grey_Image.item(dy,x)<=Maximum_Intensity:
            for a in range (Aprox_Line_Distance-10,Aprox_Line_Distance+10):
                if Grey_Image.item(dy-a,x)<=Maximum_Intensity and Grey_Image.item(dy+a,x)<=Maximum_Intensity:
                    for b in range (0,a+1):
                        c = a - b
                        if Grey_Image.item(dy-b,x+Ax)<= Maximum_Intensity and Grey_Image.item(dy+c,x+Ax)<= Maximum_Intensity:
                            if c << b:
                                List = []
                                List.append(dy-b)
                                List.append(x+Ax)
                                List.append(dy+b)
                                List.append(x-Ax)
                                List1.append(List)
                            if c >> b:
                                List = []
                                List.append(dy-c)
                                List.append(x-Ax)
                                List.append(dy+c)
                                List.append(x+Ax)
                                List1.append(List)


    
    for g in List1:
        
        cv2.line(Main_Image,(g[1],g[0]),(g[3],g[2]),0,3)
        
        op = (g[2]-g[0])/2 #Defining Oposite leg
        ad = (g[3]-g[1])/2 #Defining Adjacent leg
        tan = op/ad
        angle = np.arctan(tan)
        List2.append(angle)
    
    Average_Angle = 0
    for k in List2:
        Average_Angle = Average_Angle + k
    Average_Angle = (Average_Angle/len(List2))*50 #Seriously, i have no idea why, but if multiply by 50 it works better....maybe is something about the arctan and the relative radious of rotation, but, who knows?...

    #C
    def rotateImage(image, angle):
      image_center = tuple(np.array(image.shape[1::-1]) / 2)
      rot_mat = cv2.getRotationMatrix2D(image_center, angle, 1.0)
      result = cv2.warpAffine(image, rot_mat, image.shape[1::-1], flags=cv2.INTER_LINEAR)
      return result
    #The rotate function was copied from "Alex Rodrigues - https://stackoverflow.com/questions/9041681/opencv-python-rotate-image-by-x-degrees-around-specific-point"
    

    print("Saving Image")
    cv2.imwrite((str(Output))+(str(num))+".png" , rotateImage(Main_Image,Average_Angle))
    num = num+1
    
