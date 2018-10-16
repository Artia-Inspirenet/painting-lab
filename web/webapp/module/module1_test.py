import pytoshop
from pytoshop.user import nested_layers as nl
import cv2
import numpy as np
import os

# alpha가 0(검정색)인 곳, 즉 데이터가 없는 곳은 배경색 흰색 (255,255,255)로 바꿈
# a 범위 수정 가능
def alpha_to_color(image, color=(255,255,255)):
    r, g, b, a = np.rollaxis(image, axis = -1)
    r[a < 50] = color[0]
    g[a < 50] = color[1]
    b[a < 50] = color[2]
    image = np.dstack([r, g, b])
    return image

def check_frame_layer(layer_img):
    # convert data type into unsigned 8-bit integer
    layer_img = np.uint8(layer_img)

    # Image have to be binary image
    imgray = cv2.cvtColor(layer_img, cv2.COLOR_RGB2GRAY)
    ret, thresh = cv2.threshold(imgray, 127, 255, 0)
    image, contours, hierachy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    is_frame = None
    outer_borders_idx = []
    hole_borders_idx = []
    top_list, left_list, bottom_list, right_list = [], [], [], []

    # Canvas_border : next = previous = parents = -1
    candidate = np.all(hierachy[0][:,[0,1,3]] == [-1,-1,-1], axis=1)

    # check if canvas_border is unique
    # case 1) canvas_border exists
    if sum(candidate) == 1:
        canvas_border_idx = np.where(candidate)[0][0]
        outer_borders_idx = np.where(hierachy[0][:,3] == canvas_border_idx)[0].tolist()

        # hole border is child of outer border
        for outer_idx in outer_borders_idx:
            hole_idx = hierachy[0][outer_idx][2]
            # check if each cut is composed of only one pair of hole-outer border
            # In other words, hole border doesn't have child
            if (hierachy[0][hole_idx][2] == -1):
                hole_borders_idx.append(hole_idx)

    # case 2) canvas_border does not exist
    else:
        outer_borders_idx = np.where(hierachy[0][:,3] == -1)[0].tolist()
        for outer_idx in outer_borders_idx:
            hole_idx = hierachy[0][outer_idx][2]
            if (hierachy[0][hole_idx][2] == -1):
                hole_borders_idx.append(hole_idx)

    # implement when the layer is frame layer
    if (sum(candidate) + len(outer_borders_idx) + len(hole_borders_idx)) == len(hierachy[0]):
        is_frame = True
        for idx in hole_borders_idx:
            left, top, right, bottom = cut_coordinate(contours, idx)
            left_list.append(left)
            top_list.append(top)
            right_list.append(right)
            bottom_list.append(bottom)

    #img = cv2.drawContours(layer_img, contours, -1, (0,0,255), 1)
    #cv2.imwrite('/home/dongsu/frame.png', img)

    return is_frame, left_list, top_list, right_list, bottom_list

# Take one pixel wide
def cut_coordinate(contours, hole_border_idx):
    '''x_points = contours[idx][:,0][:,0]
    y_points = contours[idx][:,0][:,1]

    # sort by x, then by y
    key = np.lexsort((y_points, x_points))
    contours[idx][key]'''

    top = np.min(contours[hole_border_idx], axis=0)[0][0]
    left = np.min(contours[hole_border_idx], axis=0)[0][1]
    bottom = np.max(contours[hole_border_idx], axis=0)[0][0]
    right = np.max(contours[hole_border_idx], axis=0)[0][1]

    return top-1, left-1, bottom+1, right+1

def layer_to_image(layers, index, shape):
    layer = layers[index]
    a_color = layer.channels[-1].image
    r_color = layer.channels[0].image
    g_color = layer.channels[1].image
    b_color = layer.channels[2].image

    # rgb --> rgba
    rgba_img = np.dstack([r_color, g_color, b_color, a_color])
    rgb_img = alpha_to_color(rgba_img)

    # make all image of layers to equal size of backcolor
    # padding with value (255,255,255)
    white_layer = np.full((shape[0], shape[1], 3), 255)
    white_layer[layer.top:layer.bottom, layer.left:layer.right, :] = rgb_img

    return white_layer

# find backcolor layer index and visible layer indices
def find_backcolor_and_visible(layers, psd_shape):
    # Assume that backolor layer is unique
    backcolor_index = None

    # Exclude backolor_layer in the list
    visible_layer_list = []

    for layer in layers:
        height = layer.bottom - layer.top
        width = layer.right - layer.left
        shape = (height, width)
        # psd.shape = backcolor.shape
        if shape == psd_shape:
            # check whether backcolor is all white
            a_color = layer.channels[-1].image
            r_color = layer.channels[0].image
            g_color = layer.channels[1].image
            b_color = layer.channels[2].image
            white_layer = np.full(shape, 255)
            if (np.array_equal(white_layer, a_color)) and (np.array_equal(white_layer, r_color)) and (np.array_equal(white_layer, g_color)) and (np.array_equal(white_layer, b_color)):
                backcolor_index = layers.index(layer)

        elif layer.visible == True:
            visible_layer_list.append(layers.index(layer))

    return backcolor_index, visible_layer_list

if __name__ == '__main__':

    file_path = ''
    psd_name = ''
    save_path = file_path + ''
    os.mkdir(save_path)
    
    with open(file_path + psd_name, 'rb') as fd:
        # read binary file
        psd = pytoshop.read(fd)
        # shape : (height, width)
        shape = psd.shape
        # extract layers from psd file
        # return : list of layers
        nestedLayers = nl.psd_to_nested_layers(psd)
    
        backcolor_index, visible_layer_list = find_backcolor_and_visible(nestedLayers, shape)
    
        frame_index = []
        line_drawing_index = []
        left, right, top, bottom = [], [], [], []
        final_img = None
    
        # iterate all visible layers
        for visible_idx in visible_layer_list:
            layer_img = layer_to_image(nestedLayers, visible_idx, shape)
    
            # left, right, top, bottom would be empty if the layer is not frame one
            is_frame, temp_left, temp_top, temp_right, temp_bottom = check_frame_layer(layer_img)
            left.extend(temp_left)
            right.extend(temp_right)
            top.extend(temp_top)
            bottom.extend(temp_bottom)
    
            if is_frame:
                frame_index.append(visible_idx)
    
            else:
                # the number of black pixels
                black = np.all(layer_img == [0,0,0], axis=-1).sum()
                # not black neither white pixels
                not_black = np.any(layer_img != [0,0,0], axis=-1)
                not_white = np.any(layer_img != [255,255,255], axis=-1)
                # in short, the number of colorful pixels
                color = (not_black == not_white).sum()
    
                # Assume that line_drawing layer consists of white&black pixels
                if black > color:
                    line_drawing_index.append(visible_idx)
    
        # create white layer
        if len(line_drawing_index) != 0:
            final_img = np.full((shape[0], shape[1], 3), 255)
    
        # prepare each line_drawing_layer
        # if a pixel in each layer image is not white, which is drawing, overwrite the pixel on previous overlapped layer image
        for ld_idx in line_drawing_index:
            # make each layer to image
            layer_img = layer_to_image(nestedLayers, ld_idx, shape)
            # return boolean
            is_not_white = np.any(layer_img != [255,255,255], axis=-1)
            # get indices which indicates non-white pixels
            not_white_idx = np.argwhere(is_not_white)
            final_img[not_white_idx[:,0], not_white_idx[:,1]] = layer_img[not_white_idx[:,0], not_white_idx[:,1]]
    
        # crop image with frame corner points
        for i in range(len(left)):
            result = final_img[top[i]:bottom[i]+1, left[i]:right[i]+1, :]
            cv2.imwrite(save_path + '/{0}.png'.format(i), result[:,:,::-1])