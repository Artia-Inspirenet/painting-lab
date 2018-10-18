from django.shortcuts import render
from django.conf import settings
from django.contrib.auth.models import User, Group
from django.core.files import File
from rest_framework.decorators import api_view
from rest_framework.viewsets import ModelViewSet
from rest_framework.parsers import FormParser, MultiPartParser, JSONParser
from rest_framework.response import Response

import pytoshop, os, random
from pytoshop.user import nested_layers as nl
from pytoshop.enums import *
import numpy as np
from PIL import Image

from .module import module1_test as m1
import cv2

from .models import PSDFile, Work, Episode, Author, Cut
from .serializers import PSDFileUploadSerializer, WorkSerializer, EpisodeSerializer, AuthorSerializer


@api_view(['GET', 'POST'])
def psdfile_handler(request):

    if request.method == 'GET':
        # Author, Work, Episode Dropdown menu
        # Not working yet
        psdfile_list = PSDFile.objects.all()
        serializer = PSDFileUploadSerializer(psdfile_list, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        psdfiles = request.FILES.getlist('psdfile')
        #
        #
        #
        #

        file_path = settings.MEDIA_ROOT + '/m1_test'
        for fd in psdfiles:
            psd = pytoshop.read(fd)
            # shape : (height, width)
            shape = psd.shape
            # extract layers from psd file
            # return : list of layers
            nestedLayers = nl.psd_to_nested_layers(psd)

            backcolor_index, visible_layer_list = m1.find_backcolor_and_visible(nestedLayers, shape)

            frame_index = []
            line_drawing_index = []
            left, right, top, bottom = [], [], [], []
            final_img = None

            # iterate all visible layers
            for visible_idx in visible_layer_list:
                layer_img = m1.layer_to_image(nestedLayers, visible_idx, shape)

                # left, right, top, bottom would be empty if the layer is not frame one
                is_frame, temp_left, temp_top, temp_right, temp_bottom = m1.check_frame_layer(layer_img)
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
                layer_img = m1.layer_to_image(nestedLayers, ld_idx, shape)
                # return boolean
                is_not_white = np.any(layer_img != [255,255,255], axis=-1)
                # get indices which indicates non-white pixels
                not_white_idx = np.argwhere(is_not_white)
                final_img[not_white_idx[:,0], not_white_idx[:,1]] = layer_img[not_white_idx[:,0], not_white_idx[:,1]]

            # crop image with frame corner points
            for i in range(len(left)):
                result = final_img[top[i]:bottom[i]+1, left[i]:right[i]+1, :]
                cv2.imwrite(file_path + '/{0}.png'.format(i), result[:,:,::-1])

        #
        #
        #
        for psdfile in psdfiles:
            serializer = PSDFileUploadSerializer(data=request.data)
            if serializer.is_valid() :
                serializer.save(user=request.user,
                                datafile=psdfile,
                                author=request.data['author'],
                                work=request.data['work'],
                                episode=request.data['episode'])
        return Response({'status':'success'})




# Just for example, this view function makes cut again and agian when request income.
@api_view(['GET', 'POST'])
def keypoint_finder(request):
    if request.method == 'GET':

        with open(settings.MEDIA_ROOT+'/sample/humanlogo.png', 'rb') as fd:
            init = { 'img_file':File(fd),
                     'x':0,
                     'y':0,
                     'w':300,
                     'h':335 }

            cutimg = Cut.objects.create(**init)

        cut_url = os.path.join(settings.MEDIA_URL, cutimg.img_file.name[len(settings.MEDIA_ROOT)+1:])
        keypoints = [{ 'x': x*random.random(), 'y': x*random.random() } for x  in range(100,900,10)]
        keypoints.append({ 'x': 145,
                           'y': 245 })
        data = dict({ 'cutimg_url': cut_url,
                      'keypoints': keypoints })
        return Response(data=data)
