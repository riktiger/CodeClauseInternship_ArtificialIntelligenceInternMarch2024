#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 13 01:40:13 2024

@author: aritra
"""
# CodeClause Internship, March, 2024

# DOMAIN : Artificial Intelligence Intern

# PROBLEM STATEMENT : Gesture Recognition System (#CC3602)

#Use deep learning techniques to train a model capable of recognizing a variety of hand gestures, potentially for controlling devices or interacting with virtual environments.

# SOLUTION

# AUTHOR : ARITRA BAG

#Importing Libraries
import cv2
import mediapipe as mp
from datetime import datetime
import pyautogui

pyautogui.FAILSAFE = False

#Initializing
print(datetime.now(),"Air Mouse v 1.0")
print(datetime.now(),"Starting.................")


#Getting the screen height and width
screen_width, screen_height = pyautogui.size()

#Getting the finger tip points
tip = [8,12,16,20]
finger_tips = [8,12,16,20]
finger = []
fingers = []

#Importing webcam feed
cap = cv2.VideoCapture(0)
hand_detector = mp.solutions.hands.Hands(static_image_mode=False, max_num_hands=1, min_detection_confidence=0.8)
drawing_utils = mp.solutions.drawing_utils
while True:
    ret,frame = cap.read()
    #flipping the frame and scaling with respect to the frame
    #frame = cv2.flip(frame,1)
    frame_height, frame_width, channels = frame.shape
    
    if ret == True:

        #Coverting to RGB Frames
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        #Detection of Hand Landmarks
        detection = hand_detector.process(rgb_frame)
        hands = detection.multi_hand_landmarks
        #Drawing hand landmarks
        if hands:
            for hand in hands:
                thumbIsOpen = 0;
                indexIsOpen = 0;
                middleIsOpen = 0;
                ringIsOpen = 0;
                littleIsOpen = 0;
                drawing_utils.draw_landmarks(frame, hand)
                #Getting the ID of indvidual landmarks
                landmarks = hand.landmark
                index_y = 0
                for id,landmark in enumerate (landmarks):
                    x = int(landmark.x * frame_width)
                    y = int(landmark.y * frame_height)
                    #Detecting index finger tip
                    if id == 8:
                        cv2.circle(img=frame, center = (x,y), radius = 10, color = (0,255,0))
                        index_x = screen_width / frame_width * x
                        index_y = screen_height / frame_height * y
                        #Moving the cursor
                        pyautogui.moveTo(index_x,index_y)
                        #Creating a reference Point
                        reference = landmarks[2].y;
                        #Seeing if thumb is open
                        if landmarks[3].y < reference and landmarks[4].y < reference:
                            thumbIsOpen = 1
                        #Seeing if index finger is open
                        if landmarks[7].y < reference and landmarks[8].y < reference:
                            indexIsOpen = 1
                        #Seeing if middle finger is open
                        if landmarks[11].y  < reference and landmarks[12].y < reference:
                            middleIsOpen = 1
                        #Seeing if ring finger is open
                        if landmarks[15].y < reference and landmarks[16].y < reference:
                            ringIsOpen = 1
                        #Seeing if little finger is open
                        if landmarks[19].y < reference and landmarks[20].y < reference:
                            littleIsOpen = 1
                        #Detecting Hand Open Gesture   
                        if thumbIsOpen == 1 and indexIsOpen == 1 and middleIsOpen == 1 and ringIsOpen == 1 and littleIsOpen == 1:
                            cv2.putText(frame, "HAND IS OPEN", (25,400), cv2.FONT_HERSHEY_COMPLEX, 1.0,(0,255,0))
                            #Detecting Hand Closed Gesture 
                        if thumbIsOpen == 0 and indexIsOpen == 0 and middleIsOpen == 0 and ringIsOpen == 0 and littleIsOpen == 0:
                            cv2.putText(frame, "HAND IS CLOSED", (25,400), cv2.FONT_HERSHEY_COMPLEX, 1.0,(0,0,255))
                         #Detecting Thumbs Up Gesture 
                        if thumbIsOpen == 1 and indexIsOpen == 0 and middleIsOpen == 0 and ringIsOpen == 0 and littleIsOpen == 0:
                            cv2.putText(frame, "THUMBS UP", (25,400), cv2.FONT_HERSHEY_COMPLEX, 1.0,(255,0,0))
                         #Detecting Peace Gesture 
                        if thumbIsOpen == 0 and indexIsOpen == 1 and middleIsOpen == 1 and ringIsOpen == 0 and littleIsOpen == 0:
                            cv2.putText(frame, "PEACE", (25,400), cv2.FONT_HERSHEY_COMPLEX, 1.0,(255,255,255))

  
        #Displaying Output
        cv2.imshow('VIEWFINDER', frame)
        
        #Breaking the feed Loop
        if cv2.waitKey(1) == 27:
            break

#Closing all Windows
print(datetime.now(),"Esc was Pressed")
print(datetime.now(),"Exiting................")