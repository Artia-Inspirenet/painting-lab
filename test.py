import cv2
import detect_scene as ds

img1 = cv2.imread('square_shapes.png')[:,:,::-1]
img2 = cv2.imread('squres.png')[:,:,::-1]

ds.detect_scenes(img1, 'result1.png')
ds.detect_scenes(img2, 'result2.png')

