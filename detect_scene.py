
import cv2
import numpy as np
from lib.image_processing import colorspace, draw, transform
from sklearn.metrics.pairwise import euclidean_distances

def detect_scenes(img, result_path = None):
	if len(img.shape)<3:
		print('gray')
	elif len(img.shape)==3:
		print('color image')
		img = colorspace.rgb2gray(img)
	else:
		print('input is not image!')
		return
	#resize the image with fixed width
	#resized = transform.resize(img, 400)
	ratio = img.shape[1] / 400
	area_threshold = 500*ratio*ratio # I think area of 500 pixels is a good threshold to determine which one is noise or real contour.

	gray = cv2.bilateralFilter(img, 11, 17, 17)
	edged = cv2.Canny(gray, 30, 200)
	ret,thresh = cv2.threshold(edged,127,255,0)
	im2, contours, hierarchy = cv2.findContours(thresh,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
	result = img.copy()
	result = colorspace.gray2rgb(result)
	scenes = []
	for i in range(len(contours)):
		cnt = contours[i]
		x, y, w, h = cv2.boundingRect(cnt)
		if w*h < area_threshold: #filter out small area, because it is likely noise.
			continue
		scenes.append([x, y, w, h])
	scenes = np.array(scenes)
	
	filtered_scenes = filter_same_scenes(scenes, ratio)
	print('final_scene information! : ')
	print('x, y, w, h of each scene : ')
	print(filtered_scenes)

	if result_path != None:
		for i in range(len(filtered_scenes)):
			x, y, w, h = filtered_scenes[i]
			cv2.rectangle(result,(x,y),(x+w, y+h),(0,255,0), int(ratio)) # green

		cv2.imwrite(result_path, result)
		print(result_path+' : # of scenes = %d'%len(filtered_scenes))	
	return filtered_scenes

def filter_same_scenes(scenes, ratio):
	
	center = scenes[:, 0:2] + (scenes[:, 2:4]/2)
	euclidean_dist_matrix = euclidean_distances(center)
	euclidean_dist_matrix = euclidean_dist_matrix < 5*ratio

	same_scenes = [] # classify the same region scenes
	filtered_scene_index = [] # get independent scenes.

	index_list = np.array(list(range(len(scenes))))
	tmp_list = index_list.copy()

	while(1):
		same_scene_boolean_index = euclidean_dist_matrix[tmp_list[0]]
		#from Euclidean distance matrix, indexes of the same scenes are found as boolean type
		same_scene_index = index_list[same_scene_boolean_index]		
		# convert boolean type into integer type(the real index numbers which are the same scenes)
		
		max_area = 0
		for index in same_scene_index:
			x, y, w, h = scenes[index]
			if w*h>max_area: max_area_index = index
		# find the largest contour among the same region contours.

		same_scenes.append(same_scene_index)
		filtered_scene_index.append(index)
		# put these into a list.

		tmp_list = np.delete(tmp_list, np.where(np.isin(tmp_list, same_scene_index)) )
		# delete these indexes from tmp_list(temporal changable list for indexes) 
		if len(tmp_list) == 0:
			break
		# break if there is no index in tmp_list, otherwise repeat it likely.
	return scenes[ np.isin(index_list, filtered_scene_index)]

# def cropped_scenes(img, scenes):
# 	cropped_scenes = []
# 	for x, y, w, h in scenes:
# 		cropped = transform.crop(img, (x,y), w, h)
# 		cropped_scenes.append(cropped)
# 	return cropped_scenes



