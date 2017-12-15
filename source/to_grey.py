from skimage import data, io, filters, exposure
from skimage.util import img_as_ubyte
from skimage.morphology import disk
from skimage.color import rgb2gray
import logging
import boto3
import os

def main_loop(read_f, action_f, save_f, path):
    for file_name in os.listdir(path):
        img = read_f(file_name)
        res_img = action_f(img)
        save_f(file_name, res_img)

def args_logger(arr):
    logging.debug('args: {0}'.format(", ".join(arr)))

def read_img_from_fs(dir_path, file_name):
    args_logger([dir_path, file_name])
    try:   
        picture = io.imread(dir_path +'/' + file_name, True)
        return picture
    except Exception as e:
        logging.exception(e)
        raise
        
def perform_picture_modification(picture):
    try:
        args_logger([len(picture)])
        img = img_as_ubyte(picture)
        adj = exposure.adjust_log(img)
        eq = exposure.equalize_hist(adj)
        res = filters.rank.equalize(eq, selem=disk(30))
        return res
    except Exception as e:
        logging.exception(e) 
        raise

def upload_to_s3(file_name, image, path, bucket_name, file_suff):
    try:
        args_logger([file_name, len(image), path, bucket_name, file_suff])
        edited_file = file_name.split('.')[0] + file_suff + ".jpg"
        io.imsave(path+edited_file, image)
        s3 = boto3.resource('s3')
        s3.Bucket(bucket_name).upload_file(edited_file, edited_file)
    except Exception as e:
        logging.exception(e)
        raise 

if __name__ == '__main__':
    #config logger
    logging.basicConfig(format='%(levelname)s:%(funcName)s:%(message)s', level=logging.DEBUG, handlers=[logging.StreamHandler])

    #config vars
    bucket_name = os.environ['BUCKET']
    path = os.environ['WDIR']
    file_suff = os.environ['F_SUFF']

    read_f = lambda file_name: read_img_from_fs(path, file_name)
    save_f = lambda file_name, image: upload_to_s3(file_name, image, path, bucket_name, file_suff)
    action_f = lambda picture: perform_picture_modification(picture)

    main_loop(read_f, action_f, save_f, path)