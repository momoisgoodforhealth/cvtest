#!/usr/bin/env python

from __future__ import division
import cv2
import numpy as np
import socket
import struct

from collections import Counter
from module import findnameoflandmark,findpostion#,speak
import math


tip=[8,12,16,20]
tipname=[8,12,16,20]
fingers=[]
finger=[]
font = cv2.FONT_HERSHEY_SIMPLEX

MAX_DGRAM = 2**16

def dump_buffer(s):
    """ Emptying buffer frame """
    while True:
        seg, addr = s.recvfrom(MAX_DGRAM)
        print(seg[0])
        if struct.unpack("B", seg[0:1])[0] == 1:
            print("finish emptying buffer")
            break

def main():
    """ Getting image udp frame &
    concate before decode and output image """
    
    # Set up socket
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind(('10.115.133.220', 12345))
    dat = b''
    dump_buffer(s)

    while True:
        seg, addr = s.recvfrom(MAX_DGRAM)
        if struct.unpack("B", seg[0:1])[0] > 1:
            dat += seg[1:]
        else:
            dat += seg[1:]
            img = cv2.imdecode(np.fromstring(dat, dtype=np.uint8), 1)
            a=findpostion(img)
            b=findnameoflandmark(img)

            if len(b and a)!=0:
                global finger
                finger=[]
                if a[0][1:] < a[4][1:]: 
                    finger.append(1)
                    print (b[4])
                
                else:
                    finger.append(0)   
                
                global fingers
                fingers=[] 
                for id in range(0,4):
                    if a[tip[id]][2:] < a[tip[id]-2][2:]:
                        print(b[tipname[id]])

                        fingers.append(1)
            
                    else:
                        fingers.append(0)
            #Below will print to the terminal the number of fingers that are up or down          
            x=fingers + finger
            c=Counter(x)
            up=c[1]
            down=c[0]
            print('This many fingers are up - ', up)
            print('This many fingers are down - ', down)
            upp=str(up)
            cv2.putText(img, upp, (7, 70), font, 3, (100, 255, 0), 3, cv2.LINE_AA) 
            cv2.imshow('frame', img)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            dat = b''

    # cap.release()
    cv2.destroyAllWindows()
    s.close()

if __name__ == "__main__":
    main()
