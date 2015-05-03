#!/usr/bin/env python
# encoding: utf-8


from skimage.data import imread
from skimage.filters import canny, sobel_v, sobel_h
from PIL import Image
from sklearn.decomposition import PCA
from scipy.spatial import distance

import skimage
import random
import numpy as np
import math

opts = {
        'earing': {
            'path': 'image/earing/*.jpg',
            'hogs': [],
            },
        'necklace': {
            'path': 'image/necklace/*.jpg',
            'hogs': [],
            },
        }


def which_interval(v, h):
    val = math.atan2(v, h) * (180 / math.pi) + 90
    return abs(int(val / 30))


def imgread(path):
    image = imread(path, True)
    return image * 255


def prow(image):
    for row in image:
        print row


def save_img(image, fname):
    im = Image.fromarray(np.uint8( image ))
    im.save(fname)


def eoh(image):
    data = { 0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0 }
    canny_image = canny(image, low_threshold=40)
    row, col = canny_image.shape

    sobel_v_image = sobel_v(image)
    sobel_h_image = sobel_h(image)

    for r in xrange(row):
        for c in xrange(col):
            if not canny_image[r][c]:
                continue
            interval = which_interval(sobel_v_image[r][c], sobel_h_image[r][c])
            if data.has_key(interval):
                data[interval] += 1

    return data


def get_eohs(path):
    images = skimage.io.ImageCollection(path)
    datas = []

    for image in images:
        image = skimage.color.rgb2gray(image) * 255
        data = eoh(image)
        datas.append(data.values())

    return datas


def cal_distance(matrix, arr):
    results = []
    for pc in matrix:
        results.append(distance.euclidean(pc, arr))
    return min(results)


def get_eohs_by_opts(opts):
    results = {}

    for key, val in opts.iteritems():
        datas = get_eohs(val['path'])
        results[key] = datas

    return results


def get_pcas(datas):
    results = {}

    for key, vals in datas.iteritems():
        results[key] = {}

        datas = np.matrix(random.sample(vals, 9))

        pca = PCA()
        matrix = pca.fit_transform(datas)

        results[key]['matrix'] = matrix
        results[key]['pca'] = pca

    return results


def pca_tester(train_set, arr):
    results = {}

    for key, pca_result in train_set.iteritems():
        transform = pca_result['pca'].transform(arr)
        results[key] = cal_distance(pca_result['matrix'], transform)

    return results


def process():
    print opts

    results = get_eohs_by_opts(opts)
    pca_results = get_pcas(results)

    for key, vals in results.iteritems():
        print key
        for val in vals:
            print "*"*100
            test_result = pca_tester(pca_results, val)
            print test_result

if __name__ == '__main__':
    process()
