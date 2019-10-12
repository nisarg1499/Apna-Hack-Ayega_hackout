import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import cv2
import os
import time as t1
import math
import random #rng
from PIL import Image #handle images
import matplotlib.pyplot as plt #plot data
from matplotlib.patches import Polygon #draw polygons on plots
import re #regex
from subprocess import check_output #run commands
import boto3

from keras.models import Sequential
from keras.models import model_from_json
from keras.layers import Input, Dropout, Flatten, Conv2D, Convolution2D, MaxPooling2D, Dense, Activation
from keras.optimizers import RMSprop
from keras.callbacks import ModelCheckpoint, Callback, EarlyStopping
from keras.utils import np_utils
from keras import backend as K

glob_len = 0;

def frameCapture(path):
	vidObj = cv2.VideoCapture(path)
	length = int(vidObj.get(cv2.CAP_PROP_FRAME_COUNT))
	print("Length : ",length)
	length1 = int(length / 11)
	print("Length1 : ",length1)
	length = int(length1)
	count = 0
	success = 1

	while success:
		success, image = vidObj.read()
		vidObj.read()
		vidObj.read()
		vidObj.read()
		vidObj.read()
		vidObj.read()
		vidObj.read()
		vidObj.read()
		vidObj.read()
		vidObj.read()
		vidObj.read()
		image = cv2.resize(image,(3680,2760))
		cv2.imwrite("/home/meet/HACKATHON/output_frames/%d.jpg" % count,image)
		count += 1
		if count == length - 1 :
			success = 0
	
class ImageData:
    def __init__(self, img_name, boxes):
        self.img_name = img_name
        self.boxes = boxes

def parse_directory(path):
    """Parse a directory containing negative images to a list of ImageData"""
    img_names = check_output(["ls", path]).decode("utf8").split("\n")
    data = []
    for img_name in img_names:
        match = re.search(r'\d+\.jpg', img_name)
        if(match):
            data.append(ImageData(match.group(), []))
    return data


class ImageColleciton:
    def __init__(self, data, path):
        self.data = data
        self.path = path
        
dataset1_path = "/home/meet/HACKATHON/"

img_collections = {
    "test": ImageColleciton( #test images have only positive data
       	parse_directory("/home/meet/HACKATHON/output_frames/"),   
        "/home/meet/HACKATHON/output_frames/"
    ),
    
}

def ImageCollection_to_full_paths(img_col):
    return [img_col.path + img.img_name for img in img_col.data]

def read_n_crop_img_from_path(path):
    image = cv2.imread(path)
    cropped_img = image[CROP_Y[0]:IMG_H - CROP_Y[1], CROP_X[0]:IMG_W - CROP_X[1]]
    return cropped_img

def imageGenerator(img_full_paths,batch_size):
    rand_indexes = []
    
    while True: 
        X_batch = np.ndarray((batch_size, cropped_img_h, cropped_img_w, CHANNELS), dtype=np.uint8)
        
        #while(len(rand_indexes) < batch_size):
        #    more_indexes = list(range(0,len(img_full_paths)))
        #    rand_indexes = more_indexes + rand_indexes
        
        for j in range(batch_size):
            #i = rand_indexes.pop()
            #print("j : ",img_full_paths[j])
            X_batch[j] = read_n_crop_img_from_path(img_full_paths[j])
             
        yield (X_batch)


def outputvideo(ph,parent_dir,path):


	vidObj = cv2.VideoCapture(path)
	fourcc = cv2.VideoWriter_fourcc(*'XVID')
	outVid = cv2.VideoWriter('output.avi',fourcc, 20.0, (848,480))

	font = cv2.FONT_HERSHEY_SIMPLEX 
	org = (1200, 2200) 
	fontScale = 10
	color = (0, 0, 255) 
	thickness = 20
	ph.sort()
	print(ph)
	
	success = True
	frame_number = 0
	ph_ID = 0
	while success :
		success, vid_image = vidObj.read()    
		if frame_number == ph_ID :

			image = cv2.putText(vid_image, 'Detected!!', org, font, 
				fontScale, color, thickness, cv2.LINE_AA) 
			vid_image = image
			outVid.write(vid_image)
			
			success, vid_image = vidObj.read()    
			image = cv2.putText(vid_image, 'Detected!!', org, font, 
				fontScale, color, thickness, cv2.LINE_AA) 
			vid_image = image
			outVid.write(vid_image)
			
			success, vid_image = vidObj.read()    
			image = cv2.putText(vid_image, 'Detected!!', org, font, 
				fontScale, color, thickness, cv2.LINE_AA) 
			vid_image = image
			outVid.write(vid_image)
			
			success, vid_image = vidObj.read()    
			image = cv2.putText(vid_image, 'Detected!!', org, font, 
				fontScale, color, thickness, cv2.LINE_AA) 
			vid_image = image
			outVid.write(vid_image)
			
			success, vid_image = vidObj.read()    
			image = cv2.putText(vid_image, 'Detected!!', org, font, 
				fontScale, color, thickness, cv2.LINE_AA) 
			vid_image = image
			outVid.write(vid_image)
			
			success, vid_image = vidObj.read()    
			image = cv2.putText(vid_image, 'Detected!!', org, font, 
				fontScale, color, thickness, cv2.LINE_AA) 
			vid_image = image
			outVid.write(vid_image)
			
			success, vid_image = vidObj.read()    
			image = cv2.putText(vid_image, 'Detected!!', org, font, 
				fontScale, color, thickness, cv2.LINE_AA) 
			vid_image = image
			outVid.write(vid_image)
			
			success, vid_image = vidObj.read()
		outVid.write(vid_image)
	outVid.write(vid_image)
	vidObj.release()
	outVid.release()


def prep_imgs_for_plt(imgs):
    return [np.flip(img, 2) for img in imgs]

def avg_img(img_list):
    return np.array(img_list).mean(axis=0, dtype=np.uint32)

def show_img(img, text="", prep=True):
    if(prep):
        img = prep_imgs_for_plt([img])[0]
    fig, ax = plt.subplots(1, figsize=(25,25))
    ax.set_title(text)
    ax.imshow(img)

def apply_threshold(threshold, data):
    return [0 if item < threshold else 1 for item in data]
    
def display_prediction(X,index):
    image = X[index]
    label = 'idk'
    pred = loaded_model.predict(np.expand_dims(image, axis=0))
    show_img(image, "label: {}, prediction: {}".format(label, pred))


if __name__ == '__main__':
	frameCapture("/home/meet/HACKATHON/input_videos/9_2.mp4")
	json_file = open('/home/meet/HACKATHON/model.json', 'r')
	loaded_model_json = json_file.read()
	json_file.close()
	loaded_model = model_from_json(loaded_model_json)
	loaded_model.load_weights("/home/meet/HACKATHON/model.h5")
	print("Loaded model from disk")

t1.sleep(2)
IMG_W = 3680
IMG_H = 2760
CHANNELS = 3
CROP_X = (0,0) #take CROP_X[0] from the left and CROP_X[1] from the right
CROP_Y = (1000,800) #take CROP_Y[0] from the top and CROP_Y[1] from the bottom

lat = ["23.187590", "23.187566", "23.187541", "23.187521", "23.187507", "23.187699"]
lon = ["72.628997", "72.629007", "72.629008", "72.629018", "72.629012", "72.629010"]
flag = 1

vidObj = cv2.VideoCapture("/home/meet/HACKATHON/input_videos/9_2.mp4")
length = int(vidObj.get(cv2.CAP_PROP_FRAME_COUNT)/11)
print("length : ", length)

cropped_img_w = IMG_W - CROP_X[0] - CROP_X[1]
cropped_img_h = IMG_H - CROP_Y[0] - CROP_Y[1]
test_col = img_collections["test"]
img_full_paths = ImageCollection_to_full_paths(test_col)
test_generator = imageGenerator(img_full_paths,length - 8)
X_test = next(test_generator)
poth_count = -1

ph = []
full_path = []
it = 0

ACCESS_KEY=''

SECRET_KEY=''
parent_dir = '/home/meet/HACKATHON/output_frames/'

for i in range(length) :
	if apply_threshold(0.5, loaded_model.predict(X_test[i:i+1], verbose=1)) == [1] :
		name = img_full_paths[i].split('/')
		id = name[-1].split('.')
		time = int((int(id[0])*11 + 1)/60)
		time_ms = int(time/60)
		time_ss = time - (time_ms*60)
		print("Current Count", poth_count)

		if poth_count < 5 :
			poth_count=poth_count+1
			s = lat[poth_count]+","+lon[poth_count]+" "+str(flag)+ "\n"
			print("In")
			print(s)
			file = open("/home/meet/HACKATHON/co.txt", "a")
			file.write(s)
			t1.sleep(1)
			file.close();
			s3 = boto3.client('s3', aws_access_key_id=ACCESS_KEY, aws_secret_access_key=SECRET_KEY)
			s3.upload_file("/home/meet/HACKATHON/co.txt", "hackoutpothole", "/home/meet/HACKATHON/co.txt")
			print("Uploaded to S3")
		
		ph.append(int(id[0])*11)
		print(ph[it])
		it = it + 1

		#print("Detected!! Frame Number :- % d" % (int(id[0])*11))
		#print("Time min : %d \t sec : %d" %(time_ms,time_ss))


outputvideo(ph, parent_dir, "/home/meet/HACKATHON/input_videos/9.mp4")
display_prediction(X_test,0)
display_prediction(X_test,1)
	
