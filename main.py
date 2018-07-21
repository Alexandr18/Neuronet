#!/usr/bin/env python 
# -*- coding: utf-8 -*-
# USAGE
# python real_time_object_detection.py --prototxt MobileNetSSD_deploy.prototxt.txt --model MobileNetSSD_deploy.caffemodel

# импортировать необходимые пакеты
from imutils.video import VideoStream
from imutils.video import FPS
import numpy as np
import argparse
import imutils
import time
import cv2
#com порт
import serial

#my_end
# построить аргумент parse и проанализировать аргументы
ap = argparse.ArgumentParser()
ap.add_argument("-p", "--prototxt", required=True,
	help="path to Caffe 'deploy' prototxt file")
ap.add_argument("-m", "--model", required=True,
	help="path to Caffe pre-trained model")
ap.add_argument("-c", "--confidence", type=float, default=0.2,
	help="minimum probability to filter weak detections")
args = vars(ap.parse_args())

# инициализировать список меток класса MobileNet SSD был обучен
# обнаружить, а затем создать набор цветов рамки для каждого класса
CLASSES = ["background", "aeroplane", "bicycle", "bird", "boat",
	"bottle", "bus", "car", "cat", "chair", "cow", "diningtable",
	"dog", "horse", "motorbike", "person", "pottedplant", "sheep",
	"sofa", "train", "tvmonitor"]
COLORS = np.random.uniform(0, 255, size=(len(CLASSES), 3))

# загрузить нашу сериализованную модель с диска
print("[INFO] loading model...")
net = cv2.dnn.readNetFromCaffe(args["prototxt"], args["model"])

# инициализировать видеопоток, позволить датчику камеры прогреться,
# и инициализация счетчика FPS
print("[INFO] starting video stream...")
vs = VideoStream(src=0).start()
time.sleep(2.0)
fps = FPS().start()

label1='0'
found="person"
# петля над кадрами из видеопотока
#устройство управления
ser = serial.Serial("/dev/ttyACM0")
ser.baudrate = 115200
#my_end
while True:
	# захватить кадр из потокового видеопотока и изменить его размер
        #, чтобы иметь максимальную ширину 400 пикселей 
	frame = vs.read()
	frame = imutils.resize(frame, width=800)

	# захватить размеры рамки и преобразовать ее
	(h, w) = frame.shape[:2]
	blob = cv2.dnn.blobFromImage(cv2.resize(frame, (300, 300)),
		0.007843, (300, 300), 127.5)

	# передать blob через сеть и получить обнаружение и
	# предсказания	
	net.setInput(blob)
	detections = net.forward()
	#print(detections)
	# цикл по обнаружению
	for i in np.arange(0, detections.shape[2]):
		# extract the confidence (i.e., probability) associated with
		# the prediction
		confidence = detections[0, 0, i, 2] 
		#print(confidence) процент опознания
		# filter out weak detections by ensuring the `confidence` is
		# greater than the minimum confidence
		if confidence > args["confidence"]:
			# extract the index of the class label from the
			# `detections`, then compute the (x, y)-coordinates of
			# the bounding box for the object
			idx = int(detections[0, 0, i, 1])
			box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
			(startX, startY, endX, endY) = box.astype("int")

			# draw the prediction on the frame
			label = "{}: {:.2f}%".format(CLASSES[idx],
				confidence * 100)
			cv2.rectangle(frame, (startX, startY), (endX, endY),
				COLORS[idx], 2)
			y = startY - 15 if startY - 15 > 15 else startY + 15
			cv2.putText(frame, label, (startX, y),
				cv2.FONT_HERSHEY_SIMPLEX, 0.5, COLORS[idx], 2)
				#my

			if label[0:6]==found:
				ser.write(b'1') 
  				#line = ser.readline()
  				#print(line[1:3])
			else:
				ser.write(b'0')	
		
			if label1!=label[0:6]:
				print(label)
				label1=label[0:6]
				#if label[0:6]==found:
				#	ser.write(b'1') 
  					#line = ser.readline()
  					#print(line[1:3])
				#else:
				#	ser.write(b'0')
#my_end
	# show the output frame
	cv2.imshow("Окно", frame)
	key = cv2.waitKey(1) & 0xFF

	# if the `q` key was pressed, break from the loop
	if key == ord("q"):
		break

	# update the FPS counter
	fps.update()

# stop the timer and display FPS information
fps.stop()
print("[INFO] elapsed time: {:.2f}".format(fps.elapsed()))
print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))

# do a bit of cleanup
cv2.destroyAllWindows()
vs.stop()
