import cv2
from matplotlib import pyplot as plt
from lib.image_processing import draw
import detect_scene as ds


#module 1 example: get scenes from layer png file
img1 = cv2.imread('layer.png')[:,:,::-1]


ds.detect_scenes(img1)