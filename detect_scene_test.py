
import cv2
from lib.image_processing import colorspace, draw, transform
from matplotlib import pyplot as plt
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
	edged = cv2.Canny(img, 30, 200)
	ret,thresh = cv2.threshold(edged,127,255,0)
	plt.imshow(thresh)
	plt.show()
	im2, contours, hierarchy = cv2.findContours(thresh,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
	print(gray.shape)
	result = img.copy()
	result = colorspace.gray2rgb(result)
	scenes = []
	for i in range(len(contours)):
		checker_img = result.copy()
		print(cv2.contourArea(contours[i]))
		if cv2.contourArea(contours[i]) < 500:
			continue
		# cnt = contours[i]
		# x, y, w, h = cv2.boundingRect(cnt)
		# cv2.rectangle(checker_img,(x,y),(x+w, y+h),(0,255,0), 3) # green
		# cv2.imwrite(str(i)+'_checker_img.png', checker_img)
		# scenes.append([x, y, w, h])
		checker_img = cv2.drawContours(checker_img, contours, i, (0, 255, 0), 3)
		plt.imshow(checker_img)
		plt.show()
	# if result_path != None:
	# 	cv2.imwrite(result_path, result)	
	return scenes

def cropped_scenes(img, scenes):
	cropped_scenes = []
	for x, y, w, h in scenes:
		cropped = transform.crop(img, (x,y), w, h)
		cropped_scenes.append(cropped)
	return cropped_scenes



