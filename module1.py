import cv2
import os
from psd_tools import PSDImage
from PIL import Image
import cv2
from lib.image_processing import transform
import detect_frames as ds
import sys
import pickle
import numpy as np

# function for getting layer indices and checking wrong name and invisibility of layer
def layer_index_and_check_names(psd):
# initialization
	backcolor_in = False
	frame_in = False
	line_drawing_in = False

	backcolor_visible = True
	frame_visible = True
	line_drawing_visible = True

	i = 0 # for layer index
	for layer in psd.layers:
		if layer.name == 'backcolor':
			backcolor_idx = i
			backcolor_in = True
			if layer.visible == False:
				backcolor_visible = False

		if layer.name == 'frame':
			frame_idx = i
			frame_in = True
			if layer.visible == False:
				frame_visible = False

		if layer.name == 'line_drawing':
			line_drawing_idx = i
			line_drawing_in = True
			if layer.visible == False:
				line_drawing_visible = False

		i += 1

	if backcolor_in == False:
		print ("backcolor doesn't exist")
		backcolor_idx = 100 # 100 is arbitrary number
	if frame_in == False:
		print ("frame doesn't exist")
		frame_idx = 100
	if line_drawing_in == False:
		print ("line_drawing doesn't exist")
		line_drawing_idx = 100

	if backcolor_visible == False:
		print ("backcolor is not visible")
	if frame_visible == False:
		print ("frame is not visible")
	if line_drawing_visible == False:
		print ("line_drawing is not visible")

	return backcolor_idx, frame_idx, line_drawing_idx, backcolor_visible, frame_visible, line_drawing_visible



# function for saving image of psd file which has only frame and backcolor layers
def save_backcolor_frame(psd_file, frame_idx, backcolor_idx, directory):

	psd = psd_file
	psd.layers = [psd.layers[frame_idx], psd.layers[backcolor_idx]] # order is important!!
	backcolor_frame_img = psd.as_PIL_merged() # type(backcolor_frame_img) = RGBA
	backcolor_frame_img = backcolor_frame_img.convert('RGB')
	backcolor_frame_saved_img = directory+'backcolor_frame.png'
	backcolor_frame_img.save(backcolor_frame_saved_img)
	print ('backcolor frame image saved')

	return backcolor_frame_saved_img



# function for saving whole psd_file into image_file
def save_picture(psd_file, directory):

	psd = psd_file
	picture_img = psd.as_PIL()
	picture_img.save(directory+'picture.png')
	print ('picture.png saved')



# function for saving input_image
def save_input_picture(psd_file, line_drawing_idx, backcolor_idx, directory):

	psd = psd_file
	psd.layers = [psd.layers[line_drawing_idx], psd.layers[backcolor_idx]]
	input_img = psd.as_PIL_merged()
	input_picture_img = directory+'input_picture.png'
	input_img.save(input_picture_img)

	return input_picture_img



# function for cropping images
def cropped_scenes(image, scenes, directory):

	backcolor_set = (255,255,255) # backcolor = white
	threshold_for_backcolor = 10 # for checking if frame is empty
	i = 0
	img = cv2.imread(image)

	# sort frame sequence
	seq_array = np.lexsort((scenes[:,0], scenes[:,1]))
	seq_list = seq_array.tolist()
	scenes_list = scenes.tolist()
	sorted_scenes_list = []

	for idx in seq_list:
		sorted_scenes_list.append(scenes_list[idx])

	xy_coordinate_list = []	# frame coordinate

	for x, y, w, h in sorted_scenes_list:
		center_x = x + int(w/2)
		center_y = y + int(h/2)
		cropped = transform.crop(img, (center_x,center_y), w, h)
		xy_coordinate = (x, y)
		is_backcolor = (cropped == backcolor_set[::-1]).all(2)
		r, c = np.where(is_backcolor == False)

		if len(c) > threshold_for_backcolor: # crop frames only for non-empty ones
			i += 1
			cv2.imwrite(directory+'input_cropped_img'+str(i)+'.png', cropped)
			xy_coordinate_list.append(xy_coordinate)
			print ('cropping each cuts...')

	return xy_coordinate_list



# main function
def load_psd():

    home_path = os.environ['HOME'] + '/'
    # set load_path
    work_path = 'test_psd' # set work_path
    title = 't1' # set title
    episode = 'e2' # set episode
    load_path = home_path + work_path + '/' + title + '/' + episode + '/'

    name_error_list = [] # list of mis-spelled layers
    visible_not_activated_list = [] # list of non-visible layers

    for file in os.listdir(load_path):
        if file.endswith('.psd'):
        	print ('-------------------------------------------------------------')
        	print (load_path+file+' is processing')
        	result_dir = load_path+'/'+file[0:3]+'/'
        	os.mkdir(result_dir)

        	psd = PSDImage.load(load_path+file)
        	backcolor_idx, frame_idx, line_drawing_idx, backcolor_visible, frame_visible, line_drawing_visible = layer_index_and_check_names(psd)

        	if (backcolor_idx == 100) or (frame_idx == 100) or (line_drawing_idx == 100) :
        		name_error_list.append(load_path+file)
        		continue

        	if (backcolor_visible == False) or (frame_visible == False) or (line_drawing_visible == False):
        		visible_not_activated_list.append(load_path+file)
        		continue

        	backcolor_frame_saved_img = save_backcolor_frame(psd, frame_idx, backcolor_idx, result_dir)
        	del psd # delete changed psd_file

        	img = cv2.imread(backcolor_frame_saved_img)[:,:,::-1]
        	detected_backcolor_frame = result_dir + 'detected_backcolor_frame.png'
        	cut_point_list = ds.detect_frames(img, detected_backcolor_frame)

        	psd = PSDImage.load(load_path+file) # re-load original psd_file
        	save_picture(psd, result_dir)
        	input_picture_img = save_input_picture(psd, line_drawing_idx, backcolor_idx, result_dir)
        	xy_coordinate_list = cropped_scenes(input_picture_img, cut_point_list, result_dir)
        	with open(result_dir+'xy_coordinate.txt', 'wb') as f:
        		pickle.dump(xy_coordinate_list, f)
        	print (load_path+file+' is over')

    print ('everything is done')
    with open(load_path+'name_error_psd.txt','wb') as f :
    	pickle.dump(name_error_list, f )
    with open(load_path+'invisible_psd.txt','wb') as f:
    	pickle.dump(visible_not_activated_list, f)

    print ('---------------------------- name error list ---------------------------------')
    print (name_error_list)
    print ('------------------------visible is not activated list ------------------------')
    print (visible_not_activated_list)

load_psd()
