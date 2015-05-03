#!/usr/bin/env python
# encoding: utf-8


# from scipy.ndimage import imread
# import scipy.ndimage as ndimage
from skimage.data import imread
import math

def which_interval(v, h):
    val = math.atan2(v, h) * (180 / math.pi)
    return int(val / 30)


def process():
    data = {
            0: 0,
            1: 0,
            2: 0,
            3: 0,
            4: 0,
            5: 0,
            6: 0,
            7: 0,
            8: 0,
            }
    sobel_v_image = imread('sobel_v2.jpg')
    sobel_h_image = imread('sobel_h2.jpg')
    canny_image = imread('canny2.jpg')
    row, col = canny_image.shape
    for r in xrange(row):
        for c in xrange(col):
            if sobel_v_image[r][c] < 0 or sobel_h_image[r][c] < 0:
                print sobel_v_image[r][c], sobel_h_image[r][c]
            if canny_image[r][c] != 255:
                continue
            interval = which_interval(sobel_v_image[r][c], sobel_h_image[r][c])
            data[interval] += 1

    print data

if __name__ == '__main__':
    process()
