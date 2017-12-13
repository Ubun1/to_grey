import unittest
import to_grey
import numpy

class TestToGrey(unittest.TestCase):

    def test_read_img_from_fs(self):
        self.assertTrue(type(to_grey.read_img_from_fs("./test/data", "img.jpg")) is ndarray)

    def tes_perform_picture_modification(self):
        self.assertTrue(type(to_grey.perform_picture_modification(numpy.empty([1,1]))) is ndarray)

if __name__ == '__main__':
    unittest.main()