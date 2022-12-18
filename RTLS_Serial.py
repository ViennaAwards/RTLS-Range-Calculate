import serial
import time
import turtle
import ast
import cv2
import math
import numpy as np

EPSILON = 0.000001

def Calculate_Position(a,b,c):
    A = (-2*600)+(2*670)
    B = (-2*1200)+(2*1020)
    C = (a*a) - (b*b) - (600*600) + (670*670) - (1200*1200) + (1020*1020)
    D = (-2*670) + (2*670)
    E = (-2*1020) + (2*690)
    F = (b*b) - (c*c) - (670*670) + (670*670) - (1020*1020) + (690*690)
    x = (C*E-F*B) / (E*A-B*D)
    y = (C*D-A*F) / (B*D-A*E)
    return x,y

def Calculate_Center_V2(x0,y0,r0,x1,y1,r1,x2,y2,r2):
    dx = x1-x0
    dy = y1-y0
    d = math.sqrt((dy*dy)+(dx*dx))
    if (d>(r0+r1)):
        return false
    if (d<(Math.abs(r0-r1))):
        return false
    a = ((r0*r0) - (r1*r1) + (d*d)) / (2.0 * d)
    point2_x = x0 + (dx * a/d)
    point2_y = y0 + (dy * a/d)
    h = Math.sqrt((r0*r0) - (a*a))
    rx = -dy * (h/d)
    ry = dx * (h/d)
    intersectionPoint1_x = point2_x + rx
    intersectionPoint2_x = point2_x - rx
    intersectionPoint1_y = point2_y + ry
    intersectionPoint2_y = point2_y - ry

    dx = intersectionPoint1_x - x2
    dy = intersectionPoint1_y - y2
    d1 = Math.sqrt((dy*dy) + (dx*dx))
    dx = intersectionPoint2_x - x2
    dy = intersectionPoint2_y - y2
    d2 = Math.sqrt((dy*dy) + (dx*dx))

    if(Math.abs(d1 - r2) < EPSILON):
        print(intersectionPoint1_x,intersectionPoint1_y)
    elif(Math.abs(d2 - r2) < EPSILON):
        print("Error")
    
#turtle.setup(width=600,height=600)
#t = turtle.Turtle()
#t.hideturtle()
#t.speed(0)
# 'COM9' 부분에 환경에 맞는 포트 입력
ser = serial.Serial('COM9', 115200)

anchor1_x = 0 
anchor1_y = 0 
#t.setpos(anchor1_x,anchor1_y)
#t.clear()
#t.dot(10)
img = np.zeros((1200,1200,3),np.uint8)
font=cv2.FONT_HERSHEY_SIMPLEX
radius_1st = 0
radius_2nd = 0
radius_3rd = 0
End_Time = 0
while True:
    if ser.readable():
        Line = ser.readline()
        data = Line.decode('utf-8')
        #print(data)
        try:
            img = np.zeros((1200,1200,3),np.uint8)
            Main_Range=float(data.split()[0])*100
            Range_B=float(data.split()[1])*100
            Range_C=float(data.split()[2])*100
            if(Main_Range>0 and Range_B>0 and Range_C>0):
                x,y = Calculate_Position(Main_Range,Range_B,Range_C)
                #Calculate_Center_V2(600,1200,Main_Range,670,1020,Range_B,670,690,Range_C)
                #print(x,y)
                img = cv2.circle(img,(600,1200),10,(0,0,255),-1)
                img = cv2.circle(img,(600,1200),int(Main_Range),(0,0,255),1)
                img = cv2.circle(img,(670,1020),10,(0,0,255),-1)
                img = cv2.circle(img,(670,1020),int(Range_B),(0,0,255),1)
                img = cv2.circle(img,(670,690),10,(0,0,255),-1)
                img = cv2.circle(img,(670,690),int(Range_C),(0,0,255),1)
                img = cv2.circle(img,(int(x),int(y)),5,(255,255,0),-1)
                cv2.imshow('Test',img)
                cv2.waitKey(1)
            '''if(data.find("Found") != -1 and (radius_3rd>0 and radius_1st and radius_2nd)):
                print(data)
                Start_Time = time.time()
                print("Found_Per_Second:",Start_Time-End_Time)
                img = np.zeros((1200,1200,3),np.uint8)
                for i in range(20):
                    for j in range(20):
                        img = cv2.rectangle(img,(i*100,j*100),(100+i*100,100+j*100),(255,255,255),2)
                text_1_loc = "1 Anchor Location:"+"(320,650)"
                text_1_ran = "Range:"+str(int(radius_1st))+"cm"
                text_2_loc = "2 Anchor Location:"+"(700,450)"
                text_2_ran = "Range:"+str(int(radius_2nd))+"cm"
                text_3_loc = "3 Anchor Location:"+"(700,850)"
                text_3_ran = "Range:"+str(int(radius_3rd))+"cm"
                img = cv2.circle(img,(250,620),int(radius_1st),(255,255,255),2)
                img = cv2.circle(img,(250,620),10,(0,0,255),-1)
                cv2.putText(img,text_1_loc,(250,620),font,1,(255,255,0),2)
                cv2.putText(img,text_1_ran,(250,650),font,1,(255,255,0),2)
                img = cv2.circle(img,(700,450),int(radius_2nd),(255,255,255),2)
                img = cv2.circle(img,(700,450),10,(0,0,255),-1)
                cv2.putText(img,text_2_loc,(700,450),font,1,(255,255,0),2)
                cv2.putText(img,text_2_ran,(700,480),font,1,(255,255,0),2)
                img = cv2.circle(img,(700,880),int(radius_3rd),(255,255,255),2)
                img = cv2.circle(img,(700,880),10,(0,0,255),-1)
                cv2.putText(img,text_3_loc,(700,850),font,1,(255,255,0),2)
                cv2.putText(img,text_3_ran,(700,880),font,1,(255,255,0),2)
                img = cv2.bitwise_not(img)
                End_Time = time.time()


            if(data.find("Range from: 2") != -1):
                radius_2nd = float(data.split()[4])*100
            elif(data.find("Range from: 3") != -1):
                radius_3rd = float(data.split()[4])*100
            else:
                radius_1st = float(data.split()[1])*100
            cv2.imshow('Test',img)
            cv2.waitKey(1)'''
        except Exception:
            pass
