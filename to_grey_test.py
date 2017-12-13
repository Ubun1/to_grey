import unittest
import to_grey
import numpy

class TestToGrey(unittest.TestCase):

    def test_perform_picture_modification(self):
        self.assertTrue(type(to_grey.perform_picture_modification(numpy.array([[0],[0]]))) is numpy.ndarray)

    def test_read_img_from_fs(self):
        self.assertTrue(type(to_grey.read_img_from_fs("./tests/data", "img.jpg")) is numpy.ndarray)

if __name__ == '__main__':
    unittest.main()