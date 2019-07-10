import cv2
import numpy as np
from load_letter_data import two_to_one_vec_array
import os


def corp_margin(img):
    img2 = img.sum(axis=2)
    (row, col) = img2.shape
    row_top = 0
    row_down = 0
    col_top = 0
    col_down = 0
    for r in range(0, row):
        if img2.sum(axis=1)[r] < 765 * col:
            row_top = r
            break

    for r in range(row - 1, 0, -1):
        if img2.sum(axis=1)[r] < 765 * col:
            row_down = r
            break

    for c in range(0, col):
        if img2.sum(axis=0)[c] < 765 * row:
            col_top = c
            break

    for c in range(col - 1, 0, -1):
        if img2.sum(axis=0)[c] < 765 * row:
            col_down = c
            break

    r = row_down - row_top
    c = col_down - col_top
    if r > c:
        half = (r - c) // 2
        col_down += half
        col_top -= r - c - half
    else:
        half = (c - r) // 2
        row_down += half
        row_top -= c - r - half

    new_img = img[row_top:row_down + 1, col_top:col_down + 1, 0:3]
    return new_img


# for root, dirs, files in os.walk('/Users/squarepanda/Downloads/JPG-PNG-to-MNIST-NN-Format-master/test-images'):
#     for file in files:
#         image_path = os.path.join(root, file)
#         if 'Store' not in image_path:
#             source_img = cv2.imread(image_path)
#             blur_img = cv2.GaussianBlur(source_img, (3, 3), 1)
#             # c v2.imshow('src', blur_img)
#             corp_img = corp_margin(blur_img)
#             # cv2.imshow('corp', corp_img)
#             r_down_img = cv2.resize(corp_img, dsize=(28, 28))
#             # cv2.imshow('resize', r_down_img)
#             gray_img = cv2.cvtColor(r_down_img, cv2.COLOR_BGR2GRAY)
#             dst = np.zeros((28, 28, 1), np.uint8)
#             for i in range(0, 28):
#                 for j in range(0, 28):
#                     grayPixel = gray_img[i, j]
#                     dst[i, j] = 255 - grayPixel
#             cv2.imwrite(image_path, dst)
#             print("finish" + image_path)

def img_standardization(img):
    T = np.zeros((1, 784))
    source_img = cv2.imread(img)
    blur_img = cv2.GaussianBlur(source_img, (3, 3), 1)
    # c v2.imshow('src', blur_img)
    corp_img = corp_margin(blur_img)
    # cv2.imshow('corp', corp_img)
    r_down_img = cv2.resize(corp_img, dsize=(28, 28))
    # cv2.imshow('resize', r_down_img)
    gray_img = cv2.cvtColor(r_down_img, cv2.COLOR_BGR2GRAY)
    dst = np.zeros((28, 28, 1), np.uint8)
    for i in range(0, 28):
        for j in range(0, 28):
            grayPixel = gray_img[i, j]
            dst[i, j] = 255 - grayPixel
    T[0] = two_to_one_vec_array(dst)
    T = T.reshape(-1, 1, 28, 28)
    return T
