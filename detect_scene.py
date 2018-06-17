
import cv2
from lib.image_processing import colorspace, draw, transform

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
	#ratio = img.shape[0] / float(resized.shape[0])

	gray = cv2.bilateralFilter(img, 11, 17, 17)
	edged = cv2.Canny(gray, 30, 200)
	ret,thresh = cv2.threshold(edged,127,255,0)
	im2, contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

	result = img.copy()
	result = colorspace.gray2rgb(result)
	scenes = []
	for i in range(len(contours)):
		cnt = contours[i]
		x, y, w, h = cv2.boundingRect(cnt)
		cv2.rectangle(result,(x,y),(x+w, y+h),(0,255,0), 3) # green
		scenes.append([x, y, w, h])
	if result_path != None:
		cv2.imwrite(result_path, result)	
	return scenes

def cropped_scenes(img, scenes):
	cropped_scenes = []
	for x, y, w, h in scenes:
		cropped = transform.crop(img, (x,y), w, h)
		cropped_scenes.append(cropped)
	return cropped_scenes



