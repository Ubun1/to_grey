from skimage import data, io, filters, exposure
from skimage.util import img_as_ubyte
from skimage.morphology import disk
from skimage.color import rgb2gray
import os

path = './images/'
for fl in os.listdir(path):
    picture = None
    picture = io.imread(path + fl, True)
    img = img_as_ubyte(picture)
    adj = exposure.adjust_log(img)
    eq = exposure.equalize_hist(adj)
    res = filters.rank.equalize(eq, selem=disk(30))
    io.imsave(path+'res/'+fl.split('.')[0]+'_{0}.jpg'.format(os.environ['F_SUFF']), res, quality=10)