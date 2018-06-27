import cv2
from matplotlib import pyplot as plt
from lib.image_processing import draw
import detect_scene as ds

#module 1 example: get scenes from layer png file
img1 = cv2.imread('test_images/square_shapes.png')[:,:,::-1]
img2 = cv2.imread('test_images/squres.png')[:,:,::-1]

ds.detect_scenes(img1, 'test_images/result1.png')
ds.detect_scenes(img2, 'test_images/result2.png')

# test in layer.png which was not well done before
img3 = cv2.imread('test_images/layer.png')[:,:,::-1]
ds.detect_scenes(img3, 'test_images/result_layer.png.png')


#module 3 example: color filling in the boundary with a starting point

img = cv2.imread('test_images/square_shapes.png')[:,:,::-1]
sample = img.copy()
center = (50, 50)
new_color = (255, 0, 0)
new = draw.color_filling(sample, center, new_color) 
#get the image of square shapes and fill red color on the image with starting point (50, 50)
cv2.imwrite('test_images/color_filling_result.png', new[:,:,::-1])
