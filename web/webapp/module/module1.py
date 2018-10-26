import pytoshop
from pytoshop.user import nested_layers as nl
import cv2
import numpy as np
import os


"""
PSD 파일의 모든 이미지 레이어를 찾는 함수
입력 : (PSD 파일의 모든 레이어, 이미지 레이어만을 저장할 리스트 변수)
레이어의 경우 계층구조(Group)를 가진 경우 존재(=pytoshop.user.nested_layers.Group)
모든 레이어를 순환하면서 이미지 레이어만을 찾아냄(재귀 호출)
출력 : (이미지 레이어만을 각 성분으로 가지는 리스트)
테스트 시간 : 0.00007초
"""
def flatten_layers(nestedLayers, flatten_layers_list):
    for layer in nestedLayers:
        if type(layer) == pytoshop.user.nested_layers.Image:
            flatten_layers_list.append(layer)
        else:
            # Group의 visible == True 인 경우만 검사 지속
            # 이유 : Group이 invisible인 경우 그 하위의 레이어들의 visible 여부와 관계없이 레이어가 OFF임 
            if layer.visible:
                flatten_layers(layer.layers, flatten_layers_list)
    return flatten_layers_list


"""
배경 레이어와 켜져있는 레어어를 찾는 함수
입력 : (이미지 레이어만을 각 성분으로 가지는 리스트, 캔버스 크기)
배경 레이어는 Visible과 관계없이, 크기와 색을 조사하여 판단
켜져있는 레이어들만 대상으로 프레임, 선화 레이어를 추정할 예정
출력 : (배경 레이어 인덱스, 켜져있는 레이어들의 인덱스를 성분으로 갖는 리스트)
테스트 시간 : 0.1초
"""
def find_backcolor_and_visible(layers, psd_shape):
    # 배경 레이어는 유일하다고 가정
    backcolor_index = None
    
    # 배경 레이어를 제외한 켜져있는 레이어를 담을 리스트
    visible_layer_list = []
    
    for layer in layers:
        height = layer.bottom - layer.top 
        width = layer.right - layer.left
        shape = (height, width)
        
        # 레이어가 켜져있을 경우 리스트에 추가
        if layer.visible == True:
            visible_layer_list.append(layers.index(layer))    
        
        # 레이어의 크기가 캔버스 크기와 같고, 흰색이면 배경 레이어라고 판단
        if shape == psd_shape:
            a_color = layer.channels[-1].image
            r_color = layer.channels[0].image
            g_color = layer.channels[1].image
            b_color = layer.channels[2].image
            white_layer = np.full(shape, 255)
            if (np.array_equal(white_layer, a_color)) and (np.array_equal(white_layer, r_color)) and (np.array_equal(white_layer, g_color)) and (np.array_equal(white_layer, b_color)):
                backcolor_index = layers.index(layer)
    
    # 배경 레이어가 리스트에 있을 경우 리스트에서 제외
    if backcolor_index in visible_layer_list:
        visible_layer_list.remove(backcolor_index)
            
    return backcolor_index, visible_layer_list 


"""
해당 레이어의 검정색과 검정/흰색을 제외한 나머지색 갯수를 비교하는 함수
입력 : (켜져있는 레이어)
레이어의 모든 픽셀에 대해 검정/흰/나머지 색의 갯수를 각각 구함
출력 : (검정색이 나머지 색보다 더 적은 경우 True
       그렇지 않은 경우 False)
테스트 시간 : 레이어당 0.55초       
"""
def has_color(layer):
        height = layer.bottom - layer.top
        width = layer.right - layer.left
        shape = (height, width)
        
        a_color = layer.channels[-1].image
        r_color = layer.channels[0].image
        g_color = layer.channels[1].image
        b_color = layer.channels[2].image
        
        # 레이어로부터 RGB를 뽑아냄
        rgba_img = np.dstack([r_color, g_color, b_color, a_color])
        rgb_img = alpha_to_color(rgba_img)
        
        # 뽑아낸 RGB로부터 검정색(0,0,0) 픽셀의 갯수를 구함
        black = np.all(rgb_img == [0,0,0], axis=-1).sum()
        # 뽑아낸 RGB로부터 검정색(0,0,0)과 흰색(255,255,255)를 제외한 픽셀의 갯수를 구함
        not_black = np.any(rgb_img != [0,0,0], axis=-1)
        not_white = np.any(rgb_img != [255,255,255], axis=-1)
        color = (not_black == not_white).sum()
        
        # 검정색과 검정/흰색 제외한 나머지색 갯수 비교
        if black < color:
            return True
        else:
            return False


"""
RGBA 이미지를 RGB 이미지로 변경하기 위한 함수
입력 : (RGBA 이미지, 배경색=흰색)
R : 빨강색
G : 초록색
B : 파랑색
A : 불투명도를 나타냄. 0에 가까울 수록 투명함. 
    띠라서 값이 0인 해당 픽셀은 나중에 배경색으로 채워짐
    실제 이미지에서 데이터가 존재하는 부분 255(흰색)으로부터 멀어질수록 0(검정색)에 가까워짐
A(Alpha) 값을 조정함으로써 R,G,B 값을 얼마나 반영할 지 결정
A의 범위가 커질 수록 배경색(흰색)으로 바꿔질 부분이 확장됨(선이 얇아짐) 
출력 : (RGB 이미지)      
"""
def alpha_to_color(image, color=(255,255,255)):
    # RGBA 4개의 채널을 가진 이미지를 각각의 R,G,B,A 1개 채널 데이터로 쪼갬
    r, g, b, a = np.rollaxis(image, axis = -1)
    
    r[a < 50] = color[0] # a범위에 따라 해당 R 값을 255(배경색)으로 변경
    g[a < 50] = color[1] # a범위에 따라 해당 G 값을 255(배경색)으로 변경
    b[a < 50] = color[2] # a범위에 따라 해당 B 값을 255(배경색)으로 변경
    
    # R,G,B 각 채널을 하나로 쌓음(RGB 채널의 이미지)
    image = np.dstack([r, g, b])
    return image


"""
해당 레이어로부터 이미지를 생성해주는 함수
입력 : (모든 레이어, 해당 레이어 인덱스, 캔버스 크기)
캔버스 크기와 동일한 흰색 이미지를 생성 후 그 위에 레이어 이미지를 덮어씀
레이어의 좌표가 캔버스 밖에 존재하는 경우 존재 --> 캔버스 크기 안의 데이터만 신경씀
ex) 캔버스는 left=top=0 을 기준
    특정 레이어 left, top < 0 또는 right, bottom 좌표가 캔버스보다 큰 경우 존재
출력 : (캔버스 크기와 동일한 사이즈로 흰색 배경을 가진 해당 레이어의 이미지)
테스트 시간 : 레이어당 0.2초
"""
def layer_to_image(layers, index, psd_shape):
    # 인덱스를 통해 해당 레이어만을 선택
    layer = layers[index]
    
    # 해당 레이어의 크기를 알기 위해 상,하,좌,우 좌표를 구함
    left = layer.left
    right = layer.right
    top = layer.top
    bottom = layer.bottom
    
    # 해당 레이어에서 각 채널의 데이터를 얻음(R,G,B,A)
    a_color = layer.channels[-1].image
    r_color = layer.channels[0].image
    g_color = layer.channels[1].image
    b_color = layer.channels[2].image
    
    # 해당 레이어의 RBGA 이미지를 RGB 이미지로 변경
    rgba_img = np.dstack([r_color, g_color, b_color, a_color])
    rgb_img = alpha_to_color(rgba_img)
    
    # 캔버스 크기와 동일한 흰색 배경 이미지 생성
    white_layer = np.full((psd_shape[0], psd_shape[1], 3), 255)
    
    # 이미지 데이터 좌표의 기준을 캔버스로 맞춤
    if layer.left < 0:
        left = 0
    if layer.top < 0:
        top = 0
    if layer.right > psd_shape[1]:
        right = psd_shape[1]
    if layer.bottom > psd_shape[0]:
        bottom = psd_shape[0]

    # 흰색 배경 이미지 위에 레이어 데이터 덮어씀 
    white_layer[top:bottom, left:right, :] = rgb_img
    
    return white_layer


"""
프레임의 윤곽선에서 컷 별로 자를 네 모서리 좌표점 구하는 함수
입력 : (프레임 레이어의 윤곽선 좌표들, 안쪽 윤곽선 인덱스)
안쪽 윤곽선의 (x,y) 좌표들 중 가장 크거나 작은 좌표점들을 대표점으로 선택
(단, 1 픽셀 씩 넓게 잡음)
출력 : (컷 별로 자를 네 모서리 좌표점)
"""
def cut_coordinate(contours, hole_border_idx):
    
    top = np.min(contours[hole_border_idx], axis=0)[0][0] # 행의 최솟값
    left = np.min(contours[hole_border_idx], axis=0)[0][1] # 열의 최솟값
    bottom = np.max(contours[hole_border_idx], axis=0)[0][0] # 행의 최댓값
    right = np.max(contours[hole_border_idx], axis=0)[0][1] # 열의 최솟값

    return top-1, left-1, bottom+1, right+1


"""
레이어가 프레임 레이어인지 검사하고, 프레임(사각형)의 네 모서리 좌표점도 함께 반환하는 함수
입력 : (흰/검 레이어의 이미지)
hierachy 구성 : [next, previous, child, parents]
    next : 동일 레벨의 이전 윤곽선
    previous : 동일 레벨의 다음 윤곽선
    child : 자식 레벨의 첫번째 윤곽선 (다른 윤곽선을 포함함)
    parents : 부모 레벨의 윤곽선 (다른 윤곽선에 포함됨)
출력 : (프레임 레이어 확인, 레이어의 컷 갯수 만큼의 네 모서리 좌표점)
테스트 시간 : 레이어당 0.05초    
"""
def check_frame_layer(layer_img):
    # unsigned 8-bit 정수로 데이터 타입 변환
    layer_img = np.uint8(layer_img)
    
    # OpenCV의 윤곽선 검출 함수 활용
    imgray = cv2.cvtColor(layer_img, cv2.COLOR_RGB2GRAY)
    ret, thresh = cv2.threshold(imgray, 127, 255, 0)
    # contours : 윤곽선을 구성하는 좌표들
    # hierachy : 윤곽선들간의 계층구조 나타냄
    image, contours, hierachy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    
    is_frame = None
    outer_borders_idx = [] # 바깥쪽 윤곽선들 인덱스 저장할 리스트 
    hole_borders_idx = [] # 안쪽 윤곽선들 인덱스 저장할 리스트
    top_list, left_list, bottom_list, right_list = [], [], [], []
    
    # 최외각 윤곽선(next=previous=parents=-1)의 갯수
    candidate = np.all(hierachy[0][:,[0,1,3]] == [-1,-1,-1], axis=1)
    
    # 경우 1) 최외각 윤곽선이 하나인 경우(=일반적인 경우)
    #        최외각 윤곽선 = 캔버스 윤곽선
    if sum(candidate) == 1:
        # 바깥쪽 윤곽선 : 최외각 윤곽선을 부모로 가짐
        canvas_border_idx = np.where(candidate)[0][0]
        outer_borders_idx = np.where(hierachy[0][:,3] == canvas_border_idx)[0].tolist()
        
        # 안쪽 윤곽선 : 바깥쪽 윤곽선의 자식
        for outer_idx in outer_borders_idx:
            hole_idx = hierachy[0][outer_idx][2]
            # 각 컷은 하나의 (바깥쪽 외곽선, 안쪽 외곽선) 하나의 쌍으로 구성
            # 안쪽 외곽선은 내부에 더 이상 외곽선을 가지지 않음. 즉, 자식 존재하지 않음
            if (hierachy[0][hole_idx][2] == -1):
                hole_borders_idx.append(hole_idx)
    
    # 경우 2) 최외각 윤곽선이 존재하지 않는 경우
    #        나머지는 경우 1과 동일            
    else:
        outer_borders_idx = np.where(hierachy[0][:,3] == -1)[0].tolist()
        for outer_idx in outer_borders_idx:
            hole_idx = hierachy[0][outer_idx][2]
            if (hierachy[0][hole_idx][2] == -1):
                hole_borders_idx.append(hole_idx)
    
    # 프레임 레이어가 맞는 경우에 실행
    # 총 윤곽선 갯수 = 최외각 윤곽선 + 바깥쪽 윤곽선 갯수 + 안쪽 윤곽선 갯수
    if (sum(candidate) + len(outer_borders_idx) + len(hole_borders_idx)) == len(hierachy[0]):
        is_frame = True

        # 모든 안쪽 윤곽선에 대해
        for idx in hole_borders_idx:
            left, top, right, bottom = cut_coordinate(contours, idx)
            left_list.append(left)
            top_list.append(top)
            right_list.append(right)
            bottom_list.append(bottom)

    return is_frame, left_list, top_list, right_list, bottom_list    

"""
메인 함수로서 실제로 call 되어 실행될 함수
입력 : (PSD 파일이 있는 경로)
출력 : 컷 좌표 리스트
"""
def run(file_path, psd_name):
        
    with open(os.path.join(file_path, psd_name), 'rb') as fd:
       
        # 바이너리 형태의 PSD 파일을 읽음
        psd = pytoshop.read(fd)

        # PSD의 shape : (height, width) = (높이, 너비)
        shape = psd.shape

        # PSD 파일로부터 레이어를 뽑아내어 리스트 형태로 반환
        nestedLayers = nl.psd_to_nested_layers(psd)
        
        # 이미지 레이어만을 저장할 리스트 변수(=pytoshop.user.nested_layers.Image)
        flatten_layers_list = []
        flatten_layers(nestedLayers, flatten_layers_list)
        
        backcolor_index, visible_layer_list = find_backcolor_and_visible(flatten_layers_list, shape)
        
        # 필요 변수들 선언 및 초기화
        black_white_layer_list = [] # 검/흰을 제외한 나머지 색이 거의 없는 레이어의 인덱스 저장할 리스트
                                    # 프레임 레이어 혹은 선화 레이어로 분류 예정
        frame_index = [] # 프레임 레이어의 인덱스 저장할 리스트(다수일 가능성)
        line_drawing_index = [] # 선화 레이어의 인덱스 저장할 리스트(다수일 가능성)
        left, right, top, bottom = [], [], [], [] # 프레임 레이어에서 각 코너 좌표점(사각형의 네 모서리)을 저장할 리스트
        final_img = None # 선화 레이어가 존재한다면 사용할 예정
        
        # 켜져 있는 레이어 중 색이 많이 들어가 있는 레이어 제거
        for visible_idx in visible_layer_list:
            if not has_color(flatten_layers_list[visible_idx]):
                black_white_layer_list.append(visible_idx)
        
        # 검정/흰색이 대부분을 차지하는 레이어들을 대상으로        
        for black_white_idx in black_white_layer_list:
            
            # 레이어로부터 이미지 생성
            layer_img = layer_to_image(flatten_layers_list, black_white_idx, shape)
            
            # 레이어가 프레임 레이어인지 검사
            # 만약 레이어가 프레임 레이어가 아니라면, [left, right, top, bottom]은 빈 리스트를 반환
            is_frame, temp_left, temp_top, temp_right, temp_bottom = check_frame_layer(layer_img)
            left.extend(temp_left)
            right.extend(temp_right)
            top.extend(temp_top)
            bottom.extend(temp_bottom)
            
            # 프레임 레이어가 맞다면, 프레임 레이어 리스트에 추가
            if is_frame:
                frame_index.append(black_white_idx)

            # 프레임 레이어가 아니라면, 선화 레이어 리스트에 추가    
            else:
                line_drawing_index.append(black_white_idx)
        
        # 컷을 순서대로 자르기 위함 (순서 : 위 -> 아래, 좌 -> 우)
        top_left = [] # 좌측 상단 좌표만 고려 (행,열)
        num_cut = len(left) # 컷의 갯수
        for c in range(num_cut): 
            top_left.append((top[c], left[c]))
        
        # 컷의 좌측 상단 좌표들 오름 차순 정렬 (행 먼저 고려, 그 다음 열 고려)
        sorted_cut_order = sorted(top_left, key=lambda x: (x[0],x[1]))
        
        # 데이터베이스에 저장할 컷 이미지 정보
        img_info = list()

        # 만약 선화 레이어가 존재한다면 실행(다수일 가능성)
        if len(line_drawing_index) != 0:
            
            # 캔버스 크기와 동일한 크기의 흰색 이미지 준비(초기 이미지)
            final_img = np.full((shape[0], shape[1], 3), 255)
            
            # 모든 선화 레이어에 대해서
            '''
            모든 선화 레이어 합치기
            테스트 시간 : 레이어당 0.2초 내외 
            '''
            for ld_idx in line_drawing_index:
                
                # 각 선화 레이어 이미지 생성
                layer_img = layer_to_image(flatten_layers_list, ld_idx, shape)
                
                # 선화 레이어에서 흰색이 아닌 픽셀(그림이 있는 픽셀)의 위치를 모두 구함
                is_not_white = np.any(layer_img != [255,255,255], axis=-1)
                not_white_idx = np.argwhere(is_not_white)
                
                # 기본 이미지(혹은 이전 이미지)에 새로운 이미지를 덮어씀 
                final_img[not_white_idx[:,0], not_white_idx[:,1]] = layer_img[not_white_idx[:,0], not_white_idx[:,1]]
            
            # 정렬된 컷의 좌측 상단 좌표들을 이용하여 컷의 인덱스를 구함 
            cut_index = []
            for c in range(len(sorted_cut_order)):
                idx = top_left.index(sorted_cut_order[c])
                cut_index.append(idx)
            
            # 정렬된 컷 순서대로 네 모서리 좌표점을 이용하여 선화 이미지로부터 해당 부분 이미지 저장 
            '''
            컷 레이어 저장
            테스트 시간 : 한 레이어(3컷 기준) 0.17초
            '''
            for i in range(len(cut_index)):
                result = final_img[top[cut_index[i]]:bottom[cut_index[i]]+1, left[cut_index[i]]:right[cut_index[i]]+1, :]
                psd_num = psd_name.split('.')[0]
                cv2.imwrite(file_path + '/{0}_{1}.png'.format(psd_num, i), result[:,:,::-1])
                img_name = '{0}_{1}.png'.format(psd_num, i)
                x = left[cut_index[i]] # 열
                y = top[cut_index[i]] # 행
                img_info.append({'name':img_name, 'x':x, 'y':y})

        # 만약 선화 레이어가 존재하지 않는다면 실행        
        else:
            print ('Line Drawing Layer Does Not Exist')
    return img_info        