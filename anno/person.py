keypoints = [
    'nose', 
    'left_eye', 
    'right_eye', 
    'left_ear', 
    'right_ear', 
    'left_shoulder', 
    'right_shoulder', 
    'left_elbow', 
    'right_elbow', 
    'left_wrist', 
    'right_wrist', 
    'left_hip', 
    'right_hip', 
    'left_knee', 
    'right_knee', 
    'left_ankle', 
    'right_ankle'
]

keypoints_style = [
    "#e6194b",
    "#3cb44b",
    "#ffe119",
    "#0082c8",
    "#f58231",
    "#911eb4",
    "#46f0f0",
    "#f032e6",
    "#d2f53c",
    "#fabebe",
    "#008080",
    "#e6beff",
    "#aa6e28",
    "#fffac8",
    "#800000",
    "#aaffc3",
    "#808000",
]

skeleton = [
    [16, 14],
    [14, 12],
    [17, 15],
    [15, 13],
    [12, 13],
    [6, 12],
    [7, 13],
    [6, 7],
    [6, 8],
    [7, 9],
    [8, 10],
    [9, 11],
    [2, 3],
    [1, 2],
    [1, 3],
    [2, 4],
    [3, 5],
    [4, 6],
    [5, 7]
]

categories = [{
    "id" : "1",
    "name" : "person",
    "supercategory" : "person",
    "keypoints" : keypoints,
    "keypoints_style" : keypoints_style,
    "skeleton" : skeleton
}]

import glob
import os
import cv2
import sys

home_path = os.environ['HOME']

img_path = os.path.join(home_path, 'images')

if not os.path.exists(img_path):
	print ("images directory doesn't exist")
	sys.exit()

image_dir_regx = img_path + '/*.png'
images = []
for image_path in glob.glob(image_dir_regx):
    image_file_name = os.path.basename(image_path)
    image_id = os.path.splitext(image_file_name)[0]
    image_url = "http://localhost:6008/" + image_file_name
    image = cv2.imread(image_path)
    width = image.shape[1]
    height = image.shape[0]
    images.append({
        "id" : image_id,
        "file_name" : image_file_name,
        "url" : image_url,
        "height" : height,
        "width" : width
    })

import json

dataset = {
    "categories" : categories,
    "images" : images,
    "annotations" : [],
    "licenses" : []
}

dataset_file_path = home_path + "/input.json"
with open(dataset_file_path, 'w') as f:
    json.dump(dataset, f)    