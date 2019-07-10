from PIL import Image
import numpy as np
import os


def two_to_one_vec_array(img_array, normalize=True):
    one_vec_arr = np.zeros(img_array.size)
    for i in range(0, 28):
        for j in range(0, 28):
            one_vec_arr[i * 28 + j] = img_array[i][j]
            if normalize:
                one_vec_arr[i * 28 + j] = one_vec_arr[i * 28 + j] / 255.0
    return one_vec_arr


def _change_one_hot_label(X):
    T = np.zeros((len(X), 10))
    for idx, row in enumerate(T):
        row[ord(X[idx]) - 65] = 1

    return T.astype(np.int)


def not_change_one_hot_label(X):
    T = np.zeros(len(X))
    for idx in range(0, len(X)):
        T[idx] = ord(X[idx]) - 65

    return T.astype(np.int)


def load_one_pict(path):
    T = np.zeros((1, 784))
    img = Image.open(path)
    grey = img.convert('L')
    resize1 = grey.resize((28, 28))
    # resize1.show()
    T[0] = two_to_one_vec_array(np.array(resize1))
    T = T.reshape(-1, 1, 28, 28)
    return T


def load_nist():
    # data_type = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']
    data_type = ['A']
    train_data = np.zeros((6000, 784))
    train_label = []
    test_data = np.zeros((1000, 784))
    test_label = []

    data_dict = {}

    print('init...')

    for data_key in data_type:
        image_data_arr = []
        for root, dirs, files in os.walk('LetterDataSet/' + data_key):
            for file in files:
                image_path = os.path.join(root, file)
                img = Image.open(image_path)
                grey = img.convert('L')
                resize1 = grey.resize((28, 28))
                image_arr = two_to_one_vec_array(np.array(resize1))
                image_data_arr.append(image_arr)
        data_dict[data_key] = image_data_arr
    # int(data_step / len(data_type)

    # sort data
    for data_step in range(0, 7000):

        data_label = data_type[data_step % len(data_type)]

        if data_step < 6000:
            train_label.append(data_label)
            idx = int(data_step / len(data_type))
            print(str(idx)+"|"+data_label)
            train_data[data_step] = data_dict[data_label][idx]
        else:
            test_label.append(data_label)
            test_data[data_step - 6000] = data_dict[data_label][int(data_step / len(data_type))]

    train_data = train_data.reshape(-1, 1, 28, 28)
    test_data = test_data.reshape(-1, 1, 28, 28)

    return (train_data, not_change_one_hot_label(train_label)), (test_data, not_change_one_hot_label(test_label))
