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

import sys
import numpy as np
import cv2
#import scipy as sp
import cv2.cv as cv
import math
import time

def calc_histogram(model, is_hsv=False):
	if is_hsv:
		hsv = model
	else:
		hsv = cv2.cvtColor(model, cv2.COLOR_BGR2HSV)
   	mask = cv2.inRange(hsv, np.array((0., 60., 32.)), np.array((180., 255., 255.)))
	hist = cv2.calcHist( [hsv], [0], mask, [16], [0, 180] )
	return hist

def build_model(tagged_face, image, torso_mask, reference_area=4000, is_tupple=False, isJson=False):
	h_mask, w_mask = torso_mask.shape[:2]
	if is_tupple:
		area = float(tagged_face[1][0]*tagged_face[1][1]*math.pi)/4.
		center = (tagged_face[0][0],tagged_face[0][1])
		chin = max(tagged_face[1][0]/2., tagged_face[1][1]/2.)
	else:
		if isJson:
			area = tagged_face[4]*tagged_face[5]
			center = (tagged_face[2]+tagged_face[4]/2,tagged_face[3]+tagged_face[5]/2)
			chin = max(tagged_face[4]/2., tagged_face[5]/2.)
		else:
			area = tagged_face[2]*tagged_face[3]
			center = (tagged_face[0]+tagged_face[2]/2,tagged_face[1]+tagged_face[3]/2)
			chin = max(tagged_face[2]/2., tagged_face[3]/2.)
	if area == 0:
		return []
	chin = 0
	factor = math.sqrt(float(area)/float(reference_area))
	image_height, image_width = image.shape[:2]
	roi = image[max(0,center[1]+chin):min(image_height,center[1]+h_mask*factor+chin),max(0,center[0]-(w_mask/2)*factor):min(image_width,center[0]+(w_mask/2)*factor)]
	print center[1]+chin, center[1]+h_mask*factor+chin, center[0]-(w_mask/2)*factor, center[0]+(w_mask/2)*factor
	h, w = roi.shape[:2]
	
	#cv2.rectangle(image, (int(center[0]-(w_mask/2)*factor),int(center[1]+chin)), (int(center[0]+(w_mask/2)*factor),int(center[1]+h_mask*factor+chin)), (255,0,0), 2)
	temp_mask = cv2.resize(torso_mask, (w,h))
	return cv2.calcHist([roi], [0], temp_mask, [8], [0, 180])

def frontal_faces_detection(image):
	cascade = cv2.CascadeClassifier('/home/cern/Downloads/opencv-2.4.6.1/data/haarcascades/haarcascade_frontalface_alt2.xml')
	kernel = (3,3)
	sigma = 1.5
	image2 = cv2.GaussianBlur(image, kernel, sigma)
	gray = cv2.cvtColor(image2, cv.CV_BGR2GRAY)
	gray = cv2.equalizeHist(gray)
	return cascade.detectMultiScale(gray, scaleFactor = 1.1, minNeighbors = 2, minSize = (10,10), flags = cv.CV_HAAR_SCALE_IMAGE)

def n_possibilities(hist_face, image, hsv, height_face, width_face, n, torso_hist, torso_mask):
	scales = (0.2, 0.5, 1, 1.5, 2)
	height2, width2 = image.shape[:2]
	step = width2 * 0.05
	best_dists = []
	best_dist = -1
	last_max = 0
	best_pos = []
	threshold = 0.5
	for s in scales:
		for y in range(0, int(height2 - height_face * s), int(step * s)):
			for x in range(0, int(width2 - width_face * s), int(step * s)):
				roi = hsv[y:y+int(height_face*s),x:x+int(width_face*s)]
				hist2 = calc_histogram(roi)
				dist = cv2.compareHist(hist_face, hist2, cv.CV_COMP_CHISQR)
				if len(best_dists) < n:
					best_dists.append(dist)
					best_pos.append((x,y,s))
					if best_dist < dist:
						best_dist = dist
						last_max = len(best_dists)-1
				else:
					if best_dist > dist:
						best_dists[last_max] = dist
						best_pos[last_max] = (x,y,s)
						for ind in range(n):
							if best_dists[last_max] < best_dists[ind]:
								last_max = ind
						best_dist = best_dists[last_max]
				
	# faces = frontal_faces_detection(image)
	# for face in faces:
	# 	x = face[0]
	# 	y = face[1]
	# 	w = face[2]
	# 	h = face[3]
	# 	s = float(width_face)/float(w)
	# 	roi = hsv[y:y+h,x:x+w]
	# 	hist2 = calc_histogram(roi)
	# 	dist = cv2.compareHist(hist_face, hist2, cv.CV_COMP_CHISQR)
	# 	cv2.rectangle(image, (x, y), (x+int(width_face*s), y+int(height_face*s)), (0, 255, 0), 2)
	# 	if len(best_dists) < n:
	# 		best_dists.append(dist)
	# 		best_pos.append((x,y,s))
	# 		if best_dist < dist:
	# 			best_dist = dist
	# 			last_max = len(best_dists)-1
	# 	else:
	# 		if best_dist > dist:
	# 			best_dists[last_max] = dist
	# 			best_pos[last_max] = (x,y,s)
	# 			for ind in range(n):
	# 				if best_dists[last_max] < best_dists[ind]:
	# 					last_max = ind
	# 			best_dist = best_dists[last_max]
	best_dist = -1
	result = []
	for ind in range(n):
		pos = best_pos[ind]
		#cv2.rectangle(image, (pos[0], pos[1]), (pos[0]+int(width_face*pos[2]), pos[1]+int(height_face*pos[2])), (0, 255, 0), 2)
		#cv2.putText(image, str(pos[2]), (pos[0], pos[1]-5), 0, 0.8, (255,0,0))
		mask = cv2.inRange(hsv, np.array((0., 60., 32.)), np.array((180., 255., 255.)))
		prob = cv2.calcBackProject([hsv], [0], hist_face, [0, 180], 1)
		prob &= mask
		term_crit = ( cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 1 )
		track_window = (pos[0], pos[1], int(width_face*pos[2]), int(height_face*pos[2]))
		track_box, track_window = cv2.CamShift(prob, track_window, term_crit)
		#cv2.ellipse(hsv, track_box, (0, 0, 255), 2)
		image_hist = build_model(track_box, hsv, torso_mask, is_tupple=True)
		if len(image_hist) < 1:
			continue
		dist = cv2.compareHist(torso_hist, image_hist, cv.CV_COMP_CHISQR)
		dist *= best_dists[ind]
		if best_dist == -1 or best_dist > dist:
			best_dist = dist
			result = track_box
	#if len(result) > 0:
		#cv2.ellipse(hsv, result, (0,255,0), 2)
	# 	cv2.putText(image, str(best_dist), (int(result[0][0]), int(result[0][1])-5), 0, 0.8, (255,0,0), 2)

	return result, best_dist

def find_face_in_collection(current_image, current_tag, collection, torso_path, resize):
	mask = cv2.imread(torso_path, 0)
	cv2.rectangle(current_image, (current_tag[2], current_tag[3]), (current_tag[2]+current_tag[4],current_tag[3]+current_tag[5]), (0,0,255), 2)
	print current_tag
	face = current_image[current_tag[3]:current_tag[3]+current_tag[5],current_tag[2]:current_tag[2]+current_tag[4]]
	cv2.imwrite('/home/cern/.virtualenvs/invenionext/src/invenio/invenio/modules/imagetagger/static/face.jpg', current_image)
	height_face, width_face = face.shape[:2]
	face_hist = calc_histogram(face, True)
	torso_hist = build_model(current_tag, current_image, mask, isJson=True)
	result = {}
	for image in collection:
		color = cv2.imread(image)
		hsv = cv2.cvtColor(color, cv2.COLOR_BGR2HSV)
		best_solution, dist = n_possibilities(face_hist, color, hsv, height_face, width_face, 10, torso_hist, mask)
		result[image] = to_tab_format(current_tag[1], best_solution, width_face, height_face, resize)
		print dist, current_tag[1]
		#cv2.imwrite(image[0:-4]+'result.jpg', color)
		#color = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
		#cv2.imwrite(image, color)
	return result

def to_tab_format(title, tag, w, h, resize):
	if len(tag) == 0:
		return tag
	tmp = cv2.ellipse2Poly((int(tag[0][0]),int(tag[0][1])), (int(tag[1][0]/2.),int(tag[1][1]/2.)), int(tag[2]), 0, 360, 60)
	rect = cv2.boundingRect(np.array([[pt] for pt in tmp]))
	return [0,title,rect[0]*resize,rect[1]*resize,rect[2]*resize,rect[3]*resize,rect[3]*resize+5]

def find_faces_in_collection(current_image, current_tags, collection, torso_path, final_width):
	now = time.time()
	tags = {}
	first = True
	hsv_model = cv2.cvtColor(cv2.imread(current_image), cv2.COLOR_BGR2HSV)
	resize = float(final_width)/float(hsv_model.shape[1])
	for tag in current_tags:
		result = find_face_in_collection(hsv_model, tag, collection, torso_path, resize)
		for img in result.keys():
			if first:
				tags[img] = [result[img]]
			else:
				tags[img].append(result[img])
		first = False
	print "-----------------time-----------", time.time()-now

	return tags