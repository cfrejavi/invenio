# -*- coding: utf-8 -*-
##
## This file is part of Invenio.
## Copyright (C) 2013 CERN.
##
## Invenio is free software; you can redistribute it and/or
## modify it under the terms of the GNU General Public License as
## published by the Free Software Foundation; either version 2 of the
## License, or (at your option) any later version.
##
## Invenio is distributed in the hope that it will be useful, but
## WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
## General Public License for more details.
##
## You should have received a copy of the GNU General Public License
## along with Invenio; if not, write to the Free Software Foundation, Inc.,
## 59 Temple Place, Suite 330, Boston, MA 02111-1307, USA.

import numpy as np
import cv2
import cv2.cv as cv
import os

def get_image_info(image_path):
	json = ''
	return json

def json_to_opencv_notation(json):
	#nb_faces x1 y1 w1 h1 ...
	tags = '0'
	return tags

def add_for_training(training_file_path, image_paths):
	training_file = open(training_file_path, 'a')
	for image_path in image_paths:
		training_file.write("\n"+image_path+" "+json_to_opencv_notation(get_image_info(image_path)))
	training_file.close()

def run_face_detection_training(positives_samples_file_path, negative_samples_file_path, vec_file_path, cascade_file_path, total_images_pos, total_images_neg, sample_width=20, sample_height=20, nb_stages=20, min_hit_rate=0.995):
	os.system("opencv_createsamples -info "+positives_samples_file_path+" -w "+sample_width+" -h "+sample_height+" -vec "+vec_file_path+" -num "+total_images_pos)
	nb_positives_training = float(total_images_pos)/float(1+(nb_stages-1)*(1-min_hit_rate))-0.15*total_images_pos
	os.system("opencv_traincascade -data "+cascade_file_path+" -vec "+vec_file_path+" -numPos "+int(nb_positives_training)+" -bg "+negative_samples_file_path+" -numNeg "+total_images_neg+" -numStages "+nb_stages+" -w "+sample_width+" -h "+sample_height+" -minHitRate "+min_hit_rate)
	return os.path.join(cascade_file_path, "cascade.xml")

def two_real_eyes(result):
	if len(result) < 2:
		return False
	else:
		if len(result) == 2:
			center1 = ((result[0][0]+result[0][2])/2., (result[0][1]+result[0][3])/2.)
			center2 = ((result[1][0]+result[1][2])/2., (result[1][1]+result[1][3])/2.)
			mean_size = (result[0][2] + result[1][2]) / 2.
			return (abs(center1[1]-center2[1]) < mean_size)
		else:
			result2 = []
			return False

def read_images_for_recognition(csv_path, size=(70,70), cropped=True):
	if not cropped:
		eye_cascade = cv2.CascadeClassifier("/home/cern/Downloads/opencv-2.4.6.1/data/haarcascades/haarcascade_eye.xml")
	images = []
	labels = []
	csv_file = open(csv_path, 'r')
	lines = csv_file.readlines()
	for line in lines:
		parts = line.split(';')
		im = cv2.imread(parts[0])
		gray = cv2.cvtColor(im, cv.CV_BGR2GRAY)
		if not cropped:
			result = eye_cascade.detectMultiScale(gray, scaleFactor = 1.2, minNeighbors = 2, minSize = (1,1), flags = cv.CV_HAAR_SCALE_IMAGE)
			im2 =Image.open(parts[0])
			if two_real_eyes(result):
				if result[0][0] < result[1][0]:
					new_im = align_and_crop_face.CropFace(im2, (result[0][0]+result[0][2]/2., result[0][1]+result[0][3]/2.), (result[1][0]+result[1][2]/2., result[1][1]+result[1][3]/2.), dest_sz=size)
				else:
					new_im = align_and_crop_face.CropFace(im2, (result[1][0]+result[1][2]/2., result[1][1]+result[1][3]/2.), (result[0][0]+result[0][2]/2., result[0][1]+result[0][3]/2.), dest_sz=size)
				#cv2.imwrite(parts[0][:-5]+"cropped"+parts[0][-5:], new_im)
				new_im.save(parts[0][:-4]+"cropped"+parts[0][-4:])
				new_im = cv2.imread(parts[0][:-4]+"cropped"+parts[0][-4:], 0)
				images.append(np.asarray(new_im, dtype=np.uint8))
				labels.append(parts[1])
		else:
			images.append(np.asarray(im, dtype=np.uint8))
			labels.append(parts[1])
		# for res in result:
		# 	cv2.rectangle(im, (int(res[0]), int(res[1])), (int(res[0]+res[2]), int(res[1]+res[3])), (255,0,0))
		# cv2.imshow("res", im)
		# cv.WaitKey()
		#images.append(np.asarray(im, dtype=np.uint8))
	return images, labels

def train_face_recognizer(algorithm, data_information_file, result_path, cropped=True):
	if algorithm == "eigen":
		model = cv2.createEigenFaceRecognizer()
	elif algorithm == "fisher":
		model = cv2.createFisherFaceRecognizer()
	elif model_type == "lbph":
		model = cv2.createLBPHFaceRecognizer()
	images, labels = read_images_for_recognition(data_information_file, cropped=cropped)
	model.train(np.asarray(images), np.asarray(labels, dtype=np.int32))
	model.save(result_path)