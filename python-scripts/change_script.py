import cv2
import os
path = "./data1/"
for i in os.listdir(path):
	if i.endswith("mask.png"):
		gray = cv2.cvtColor(cv2.imread(path+i),cv2.COLOR_BGR2GRAY)
		print(i[:-8])
		cv2.imwrite("./data0/"+i[:-8]+".png",gray)