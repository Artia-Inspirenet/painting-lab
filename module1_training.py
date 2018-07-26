import os
from psd_tools import PSDImage
from PIL import Image
import cv2
from lib.image_processing import transform
import detect_frames as ds
import sys
import pickle
import numpy as np


def save_picture(psd_file, directory):
	
	psd = psd_file
	picture_img = psd.as_PIL()
	picture_img.save(directory+'/picture.png')
	print ('picture.png saved')


def save_input_picture(psd_file, line_drawing_idx, backcolor_idx, directory):
	
	psd = psd_file
	psd.layers = [psd.layers[line_drawing_idx], psd.layers[backcolor_idx]]
	input_img = psd.as_PIL_merged()
	input_picture_img = directory+'/input_picture.png'
	input_img.save(input_picture_img)
	
	return input_picture_img


def save_backcolor_frame(psd_file, frame_idx, backcolor_idx, directory):
	
	psd = psd_file
	psd.layers = [psd.layers[frame_idx], psd.layers[backcolor_idx]]
	backcolor_frame_img = psd.as_PIL_merged()
	backcolor_frame_img = backcolor_frame_img.convert('RGB')
	backcolor_frame_saved_img = directory+'/backcolor_frame.png'
	backcolor_frame_img.save(backcolor_frame_saved_img)
	print ('backcolor frame image saved')
	
	return backcolor_frame_saved_img
    

def save_picture_with_user_backcolor(backcolor_set, psd_file, backcolor_idx, line_drawing_idx, bottom_painting_idx, directory):
	
	psd = psd_file
	backcolor_img = psd.layers[backcolor_idx].as_PIL()
	psd.layers = [psd.layers[line_drawing_idx], psd.layers[bottom_painting_idx]]
	lineDrawing_bottomPainting_img = psd.as_PIL_merged()
	user_backcolor = Image.new('RGBA', backcolor_img.size, backcolor_set)
	alpha_composite = Image.alpha_composite(user_backcolor, lineDrawing_bottomPainting_img)
	RGB_alpha_composite = alpha_composite.convert('RGB')
	picture_with_user_backcolor_img = directory+'/user_backcolor.png'
	RGB_alpha_composite.save(picture_with_user_backcolor_img)
	print ('user backcolor imgae saved')
	
	return picture_with_user_backcolor_img


def layer_index_and_check_names(psd):

	backcolor_in = False
	frame_in = False
	line_drawing_in = False
	bottom_painting_in = False

	backcolor_visible = True
	frame_visible = True
	line_drawing_visible = True
	bottom_painting_visible = True

	i = 0
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
			
		if layer.name == 'bottom_painting':
			bottom_painting_idx = i
			bottom_painting_in = True
			if layer.visible == False:
				bottom_painting_visible = False
		i += 1

	if backcolor_in == False:
		print ("backcolor doesn't exist")
		backcolor_idx = 100
	if frame_in == False:
		print ("frame doesn't exist")
		frame_idx = 100
	if line_drawing_in == False:
		print ("line_drawing doesn't exist")
		line_drawing_idx = 100
	if bottom_painting_in == False:
		print ("bottom_painting doesn't exist")
		bottom_painting_idx = 100

	if backcolor_visible == False:
		print ("backcolor is not visible")
	if frame_visible == False:
		print ("frame is not visible")
	if line_drawing_visible == False:
		print ("line_drawing is not visible")
	if bottom_painting_visible == False:
		print ("bottom_painting is not visible")		

	return backcolor_idx, frame_idx, line_drawing_idx, bottom_painting_idx, backcolor_visible, frame_visible, line_drawing_visible, bottom_painting_visible			


def cropped_scenes(backcolor_set, image1, image2, scenes, directory):

	threshold_for_backcolor = 10
	i = 0
	img1 = cv2.imread(image1)
	img2 = cv2.imread(image2)

	seq_array = np.lexsort((scenes[:,0], scenes[:,1]))
	seq_list = seq_array.tolist()
	scenes_list = scenes.tolist()
	sorted_scenes_list = []

	for idx in seq_list:
		sorted_scenes_list.append(scenes_list[idx])

	xy_coordinate_list = []	

	for x, y, w, h in sorted_scenes_list:
		center_x = x + int(w/2)
		center_y = y + int(h/2)
		cropped1 = transform.crop(img1, (center_x,center_y), w, h)
		cropped2 = transform.crop(img2, (center_x,center_y), w, h)
		xy_coordinate = (x, y)
		is_backcolor = (cropped1 == backcolor_set[::-1]).all(2)
		r, c = np.where(is_backcolor == False)

		if len(c) > threshold_for_backcolor:
			i += 1
			cv2.imwrite(directory+'/output_cropped_img'+str(i)+'.png', cropped1)
			cv2.imwrite(directory+'/input_cropped_img'+str(i)+'.png', cropped2)
			xy_coordinate_list.append(xy_coordinate)
			print ('cropping each cuts...')

	return xy_coordinate_list		

def load_psd():

    backcolor_set = (13,254,17)
    work_path = os.getcwd()
    name_error_list = []
    visible_not_activated_list = []

    for file in os.listdir(work_path):
        if file.endswith('PSD'):
            new_dir = work_path+'/'+file
            for psds in os.listdir(new_dir):
            	if psds.endswith('.psd'):
            		print ('-------------------------------------------------------------')
            		print (new_dir+'/'+psds+' is processing')
            		result_dir = new_dir+'/'+psds[0:3]
            		os.mkdir(result_dir)
            		psd = PSDImage.load(new_dir+'/'+psds)

            		backcolor_idx, frame_idx, line_drawing_idx, bottom_painting_idx, backcolor_visible, frame_visible, line_drawing_visible, bottom_painting_visible = layer_index_and_check_names(psd)

            		if (backcolor_idx == 100) or (frame_idx == 100) or (line_drawing_idx == 100) or (bottom_painting_idx == 100) :
            			name_error_list.append(new_dir+'/'+psds)
            			continue
            		if (backcolor_visible == False) or (frame_visible == False) or (line_drawing_visible == False) or (bottom_painting_visible == False) :
            			visible_not_activated_list.append(new_dir+'/'+psds)
            			continue	

            		backcolor_frame_saved_img = save_backcolor_frame(psd, frame_idx, backcolor_idx, result_dir)
            		del psd

            		img = cv2.imread(backcolor_frame_saved_img)[:,:,::-1]
            		detected_backcolor_frame = result_dir + '/detected_backcolor_frame.png'
            		cut_point_list = ds.detect_frames(img, detected_backcolor_frame)

            		

            		psd = PSDImage.load(new_dir+'/'+psds)
            		save_picture(psd, result_dir)
            		picture_with_user_backcolor_img = save_picture_with_user_backcolor(backcolor_set, psd, backcolor_idx, line_drawing_idx, bottom_painting_idx, result_dir)
            		del psd

            		psd = PSDImage.load(new_dir+'/'+psds)
            		input_picture_img = save_input_picture(psd, line_drawing_idx, backcolor_idx, result_dir)
            		xy_coordinate_list = cropped_scenes(backcolor_set, picture_with_user_backcolor_img, input_picture_img, cut_point_list, result_dir)
            		with open(result_dir+'/xy_coordinate.txt', 'wb') as f:
            			pickle.dump(xy_coordinate_list, f)
            		print (new_dir+'/'+psds+' is over')
            		del psd

            print ('one psd file is done')

    with open(work_path+'/name_error_psd.txt','wb') as f :
    	pickle.dump(name_error_list, f)
    with open(work_path+'/invisible_psd.txt','wb') as f :
    	pickle.dump(visible_not_activated_list, f)	

    print ('---------------------------- name error list ---------------------------------')
    print (name_error_list)
    print ('------------------------visible is not activated list ------------------------')
    print (visible_not_activated_list)

load_psd()		