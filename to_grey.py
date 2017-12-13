from skimage import data, io, filters, exposure
from skimage.util import img_as_ubyte
from skimage.morphology import disk
from skimage.color import rgb2gray
import boto3
import os

def main_loop(read_f, action_f, save_f, path):
    for file_name in os.listdir(path):
        img = read_f(file_name)
        res_img = action_f(img)
        save_f(res_img)
    
def read_img_from_fs(dir_path, file_name):
    picture = io.imread(dir_path + file_name, True)
    return picture

def perform_picture_modification(picture):
    img = img_as_ubyte(picture)
    adj = exposure.adjust_log(img)
    eq = exposure.equalize_hist(adj)
    res = filters.rank.equalize(eq, selem=disk(30))
    return res

def upload_to_s3(bucket_name, file_name):
    s3 = boto3.resource('s3')
    s3.Bucket(bucket_name).download_file(file_name, file_name)

read_f = lambda file_name: read_img_from_fs(os.environ['WDIR'], file_name)
save_f = lambda file_name: upload_to_s3(os.environ['BUCKET'], file_name)
action_f = lambda picture: perform_picture_modification(picture)

if __name__ == '__main__':
    main_loop(read_f, action_f, save_f, os.environ['WDIR'])