import cv2
import time#for time.sleep
import sys
import winsound#for winsound.Beep

import numpy as np

def gamma_trans(img,gamma): #gamma function, increase the brightness
    gamma_table=[np.power(x/255.0,gamma)*255.0 for x in range(256)] #build map
    gamma_table=np.round(np.array(gamma_table)).astype(np.uint8) #color is int
    return cv2.LUT(img,gamma_table) #search color map, or you can adjust by light average principle of photo

cap=cv2.VideoCapture(0)
#traning set
face_xml=cv2.CascadeClassifier('D:\\Program Files(x64)\\Phthon\\Lib\\site-packages\\cv2\\data\\haarcascade_frontalface_alt.xml')
eye_glass_xml=cv2.CascadeClassifier('D:\\Program Files(x64)\\Phthon\\Lib\\site-packages\\cv2\\data\\haarcascade_eye_tree_eyeglasses.xml')
eye_xml = cv2.CascadeClassifier('D:\\Program Files(x64)\\Phthon\\Lib\\site-packages\\cv2\\data\\haarcascade_eye.xml')
#
recover = 0
reflash_top_window_counter = 0
sleep_time_s = 4
while(cap.isOpened()):
    time.sleep(sleep_time_s)

    warning = 0
    #read camera
    ret,image=cap.read() 
    frame = cv2.flip(image, 1)
    #put frame into window
    if ret:
        #cv2.imshow('mywindow',frame)
        #check whether this is a face
        result=face_xml.detectMultiScale(frame)
        #print(result)
                
        #if is true, mark it
        if result!=(): 
            print("msg:got face",result)
            cv2.rectangle(frame,(result[0][0],result[0][1]),(result[0][0]+result[0][2],result[0][1]+result[0][3]),(255,255,0),10)
            if result[0][2] > 225:#this would need to be bigger if i become a little stronger or fatter, but it seems not possible. What a sad story, monkey boy >_<
                #too_close=too_close +1
                print("warn:face too close to screen!")                
                #winsound.Beep(600,100)
                #cv2.namedWindow('mywindow')#mywindow                
                #cv2.imshow('mywindow',frame)
                warning = 1
                recover=0
            else:
                recover = recover+1
            if recover >= 2:
                cv2.destroyAllWindows()
        else:#if face is not completely in screen, detect eyes distance
            #eye_result=eye_glass_xml.detectMultiScale(frame)# To do: affected by light(face is dark...)
            value_of_gamma = 0.4 # 0-1 :increase; 1-10 decrease
            image_gamma_correct=gamma_trans(image,value_of_gamma)   
            eye_result=eye_glass_xml.detectMultiScale(image_gamma_correct)# better after gamma correct(so you see meituxiuxiu is really useful ...)
            #print(eye_result)
            if eye_result!=():
                print("msg:only got eye(s), face is low or out of screen",eye_result)                
                if eye_result.size > 4:
                    if abs(eye_result[1][0] - eye_result[0][0]) > 347-252 - 10:
                        print("warn:got two eyes, low and too close to screen!")
                        warning = 1
                        #winsound.Beep(600,100)
                        #cv2.namedWindow('mywindow')#mywindow                                        
                        #cv2.imshow('mywindow',image_gamma_correct)
                        
        #cv2.namedWindow('mywindow')#mywindow                                
        #cv2.imshow('mywindow',frame)
        #cv2.namedWindow('mywindow2')#mywindow                                
        #cv2.imshow('mywindow2',image_gamma_correct)
    else:
        continue;
    
    if warning == 1:
        winsound.Beep(600,100)
        time.sleep(4*sleep_time_s)
        
    
#incase the user ignore and put the window backgroud, reflash to front, but it's not useful
    #reflash_top_window_counter = reflash_top_window_counter +1
    #if (reflash_top_window_counter > 2 & reflash_top_window_counter * sleep_time_s > 10):
    #    cv2.destroyAllWindows()
    #    reflash_top_window_counter=0
#q to exit
    if(cv2.waitKey(1) & 0xFF==ord('q')):
        break
    
#release
cv2.release()
cv2.destroyAllWindows()