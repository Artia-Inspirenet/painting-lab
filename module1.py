import os
import save
import cv2
from lib.image_processing import transform
import detect_scene as ds
import pickle


def cropped_scenes(image, scenes, point, path):
	i = 0
	xywh_list = []
	img = cv2.imread(image)[:,:,::-1]
	
	for x, y, w, h in scenes:
		i += 1
		center_x = x + point[0] + int(w/2)
		center_y = y + point[1] + int(h/2)
		cropped = transform.crop(img, (center_x,center_y), w, h)
		cv2.imwrite(path+'/part'+str(i)+'.png', cropped)
		print (path+'/part'+str(i)+'.png is created')
		xywh_list.append([x,y,w,h])
	
	with open(path+'/xywh_point.txt','wb') as f:
		pickle.dump(xywh_list, f)


def save_cropped_scene():
	
	task_path = save.load_psd()

	if task_path != 0:
		for directory in os.listdir(task_path):
			if directory.startswith('PSD'):
				img = cv2.imread(task_path+'/'+directory+'/layer.png')[:,:,::-1]
				with open(task_path+'/'+directory+'/layer_start_point.txt','rb') as f:
					point = pickle.load(f)

				detected_contour = ds.detect_scenes(img, task_path+'/'+directory+'/detection.png')
				cropped_scenes(task_path+'/'+directory+'/picture.png', detected_contour, point, task_path+'/'+directory+'/part')

    		

save_cropped_scene()