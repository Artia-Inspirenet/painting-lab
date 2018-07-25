
import cv2
import numpy as np
from lib.image_processing import colorspace, draw, transform
from sklearn.metrics.pairwise import euclidean_distances

def detect_frames(img, result_path = None):
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
	frames = []
	for i in range(len(contours)):
		cnt = contours[i]
		x, y, w, h = cv2.boundingRect(cnt)
		if w*h < area_threshold: #filter out small area, because it is likely noise.
			continue
		frames.append([x, y, w, h])
	frames = np.array(frames)
	
	filtered_frames = filter_same_frames(frames, ratio)
	print('final_frame information! : ')
	print('x, y, w, h of each frame : ')
	print(filtered_frames)

	if result_path != None:
		for i in range(len(filtered_frames)):
			x, y, w, h = filtered_frames[i]
			cv2.rectangle(result,(x,y),(x+w, y+h),(0,255,0), int(ratio)) # green

		cv2.imwrite(result_path, result)
		print(result_path+' : # of frames = %d'%len(filtered_frames))	
	return filtered_frames

def filter_same_frames(frames, ratio):
	
	center = frames[:, 0:2] + (frames[:, 2:4]/2)
	euclidean_dist_matrix = euclidean_distances(center)
	euclidean_dist_matrix = euclidean_dist_matrix < 5*ratio

	same_frames = [] # classify the same region frames
	filtered_frame_index = [] # get independent frames.

	index_list = np.array(list(range(len(frames))))
	tmp_list = index_list.copy()

	while(1):
		same_frame_boolean_index = euclidean_dist_matrix[tmp_list[0]]
		#from Euclidean distance matrix, indexes of the same frames are found as boolean type
		same_frame_index = index_list[same_frame_boolean_index]		
		# convert boolean type into integer type(the real index numbers which are the same frames)
		
		max_area = 0
		for index in same_frame_index:
			x, y, w, h = frames[index]
			if w*h>max_area: max_area_index = index
		# find the largest contour among the same region contours.

		same_frames.append(same_frame_index)
		filtered_frame_index.append(index)
		# put these into a list.

		tmp_list = np.delete(tmp_list, np.where(np.isin(tmp_list, same_frame_index)) )
		# delete these indexes from tmp_list(temporal changable list for indexes) 
		if len(tmp_list) == 0:
			break
		# break if there is no index in tmp_list, otherwise repeat it likely.
	return frames[ np.isin(index_list, filtered_frame_index)]

# def cropped_frames(img, frames):
# 	cropped_frames = []
# 	for x, y, w, h in frames:
# 		cropped = transform.crop(img, (x,y), w, h)
# 		cropped_frames.append(cropped)
# 	return cropped_frames



