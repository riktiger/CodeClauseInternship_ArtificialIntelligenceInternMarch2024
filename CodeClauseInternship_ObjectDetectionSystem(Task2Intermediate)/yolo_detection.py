# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
# CodeClause Internship, March, 2024

# DOMAIN : Artificial Intelligence Intern

# PROBLEM STATEMENT : Object Detection System (#CC3600)

#Create an object detection model capable of identifying and locating multiple objects within an image or video. 
#Utilize a pre-trained model such as YOLO (You Only Look Once) or Faster R-CNN, and customize it to detect specific objects of interest.

# SOLUTION

# AUTHOR : ARITRA BAG

#Importing Libraries
import ultralytics
import supervision as sv
import gradio as gr
import cv2

# Create an array of COCO labels
coco_labels = ["person", "bicycle", "car", "motorcycle", "airplane", "bus", "train", "truck", "boat", "traffic light", "fire hydrant", "stop sign", "parking meter", "bench", "bird", "cat", "dog", "horse", "sheep", "cow", "elephant", "bear", "zebra", "giraffe", "backpack", "umbrella", "handbag", "tie", "suitcase", "frisbee", "skis", "snowboard", "sports ball", "kite", "baseball bat", "baseball glove", "skateboard", "surfboard", "tennis racket", "bottle", "wine glass", "cup", "fork", "knife", "spoon", "bowl", "banana", "apple", "sandwich", "orange", "broccoli", "carrot", "hot dog", "pizza", "donut", "cake", "chair", "couch", "potted plant", "bed", "dining table", "toilet", "tv", "laptop", "mouse", "remote", "keyboard", "cell phone", "microwave", "oven", "toaster", "sink", "refrigerator", "book", "clock", "vase", "scissors", "teddy bear", "hair drier", "toothbrush"]

#Importing the YOLO Model
from ultralytics import YOLO
model = YOLO('yolov9c.pt')


#Creating a function to detect specified objects
def detect_object(input_img,lookup):
    if str(lookup) in coco_labels:
        class_no = int(coco_labels.index(lookup))
             
        results = model.predict(input_img)[0]
        detections = sv.Detections.from_ultralytics(results)
        detections = detections[detections.class_id == class_no]
        
        numbers = len(detections)
        print(numbers)
        
        labels = [f"{results.names[class_id]} : {confidence:.2f}"
            for class_id, confidence in zip(detections.class_id, detections.confidence) ]
        print(labels)
        
        box_annotators = sv.BoxAnnotator(thickness = 4, text_thickness = 2, color = sv.Color.from_hex("#39FF14"))
        output_img = box_annotators.annotate(scene = input_img, detections = detections, labels = labels)
        
        return output_img, str(numbers)        
        

    else:
        
        return input_img, "Object not in trained model"
    
#Building the gradio UI
input_img = gr.Image(height = 400, width = 640, label = "Input Image")
input_obj = gr.Textbox(label = "Enter Object to be Detected" )
output_img = gr.Image(height = 400, width = 640, label = "Output Image")
output_counts = gr.Textbox(label = "Number of Specified Objects" )
object_detector = gr.Interface(fn = detect_object, inputs = [input_img, input_obj], outputs = [output_img,output_counts])

#Launching the UI
object_detector.launch(debug = True)