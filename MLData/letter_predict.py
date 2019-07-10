# coding: utf-8
import sys, os

sys.path.append(os.pardir)
from common.functions import softmax
from train.simple_convnet import SimpleConvNet
from image_to_eminst import img_standardization

max_epochs = 20

network = SimpleConvNet(input_dim=(1, 28, 28),
                        conv_param={'filter_num': 30, 'filter_size': 5, 'pad': 0, 'stride': 1},
                        hidden_size=100, output_size=26, weight_init_std=0.01)


def letter_predict(img):
    # load参数
    network.load_params("train/self_params_letter.pkl")
    # x = load_one_pict('/UnityProject/letter_CNN/Assets/rec_letter.png')
    x = img_standardization(img)
    # x = load_one_pict('tmpm4pb835w.png')
    result = network.predict(x)

    pred = softmax(result) * 100
    return pred
    # for idx in range(0, 26):
    #     print(chr(65 + idx) + '的预测概率为' + str('%.2f' % pred[0][idx]) + '%')


letter_predict("test.png")
