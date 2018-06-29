import os
from psd_tools import PSDImage
from PIL import Image
import pickle

def save_picture(psd_file, directory):
    picture_img = psd_file.as_PIL()
    picture_img.save(directory+'/picture.png')

def save_layer(layer, directory):
    layer_img = layer.as_PIL()
    background = Image.new('RGBA', layer_img.size, (255,255,255))
    alpha_composite = Image.alpha_composite(background, layer_img)
    alpha_composite.save(directory+'/layer.png')                        

def load_psd():

    home_path = os.environ['HOME']
    task_path = home_path + '/Painting_task'
    work_path = os.getcwd()

    if not os.path.exists(task_path):
        os.mkdir(task_path)
        print ('Painting_task created in your home directory')
    
    i = 0
    for file in os.listdir(work_path+'/test_psd'):
        if file.endswith('.psd'):
            i += 1
            new_dir = task_path+'/PSD'+str(i)
            if os.path.exists(new_dir):
                print (new_dir+' exists already')
                
                return 0
            else:
                os.mkdir(new_dir)
                print (new_dir + ' is created')
                psd = PSDImage.load(work_path+'/test_psd/'+file)
                save_picture(psd, new_dir)
                print ('picture.png is saved in '+ new_dir)
                for layer in psd.layers:
                    if layer.name == '칸':
                        print ('칸 layer exists in psd')

                        point = (layer.bbox.x1, layer.bbox.y1)

                        with open(new_dir+'/layer_start_point.txt','wb') as f :
                            pickle.dump(point, f)
                            save_layer(layer, new_dir)
                            print ('layer.png is saved in '+ new_dir)

                            os.mkdir(new_dir+'/part')
                            print (new_dir+'/part is created')

                    	
                           
    return task_path