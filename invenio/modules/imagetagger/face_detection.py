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

"""Face detection"""
import sys
import cv2
import cv2.cv as cv
import numpy as np
import math

def detect(image,cascade):
	size = int(0.06*len(image))
	result = cascade.detectMultiScale(image, scaleFactor = 1.1, minNeighbors = 2, minSize = (10,10), flags = cv.CV_HAAR_SCALE_IMAGE)
	return result

def draw(image, results):
	for x, y, width, height in results:
		cv2.rectangle(image, (x,y), (x+width, y+height), (0, 255, 0), 2)

def faces(image,path_to_cascade):
	cascade = cv2.CascadeClassifier(path_to_cascade)
	return detect(image, cascade)

def group_faces(faces):
	result, weights = cv2.groupRectangles(np.array(faces).tolist(), 0)
	return result

def format_result(result, image_width, fixed_width):
	factor = float(fixed_width)/float(image_width)
	#factor = 1
	tags = []
	ind = 0
	for face in result:
		tags.append([str(ind),'', int(face[0]*factor), int(face[1]*factor), int(face[2]*factor), int(face[3]*factor), int(face[3]*factor)+5])
		ind += 1
	return tags

def find_faces(path_to_image, width, path_to_cascade = '/home/cern/Downloads/opencv-2.4.6.1/data/haarcascades/haarcascade_frontalface_alt2.xml', already_tagged=[]):
	image = cv2.imread(path_to_image)
	print path_to_image
	h, w = image.shape[:2]
	th = 500
	if h > th or w > th:
		image = cv2.pyrDown(image)
	h, w = image.shape[:2]
	kernel = (3,3)
	sigma = 1.5
	image = cv2.GaussianBlur(image, kernel, sigma)
	gray = cv2.cvtColor(image, cv.CV_BGR2GRAY)
	gray = cv2.equalizeHist(gray)
	if len(already_tagged) > 0:
		factor = float(width)/float(w)
		for tag in already_tagged:
			cv2.rectangle(gray, (int(int(tag[2])*factor),int(int(tag[3])*factor)), (int(int(tag[2])*factor+int(tag[4])*factor),int(int(tag[3])*factor+int(tag[5])*factor)), (0,0,0), -1)
	result = faces(gray, path_to_cascade)
	#result = group_faces([result])[0]
	return format_result(result, w, width)