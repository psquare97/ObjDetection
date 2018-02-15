from __future__ import division, print_function, absolute_import
import numpy as np
import tflearn
from tflearn.data_utils import shuffle, to_categorical
from tflearn.layers.core import input_data, dropout, fully_connected
from tflearn.layers.conv import conv_2d, max_pool_2d
from tflearn.layers.estimator import regression
from tflearn.data_preprocessing import ImagePreprocessing
from tflearn.data_augmentation import ImageAugmentation
import pickle

# Data loading and preprocessing
train_data = pickle.load(open('main_data.p','rb'))
test_data = pickle.load(open('test_data.p','rb'))

X, Y  = train_data[:,0:2500],train_data[:,2500:]
X_test, Y_test = test_data[:,0:2500],test_data[:,2500:]
X = X.reshape([-1,50,50,1])
X_test = X_test.reshape([-1,50,50,1])

cnn_network = input_data(shape=[None, 50, 50, 1])

cnn_network = conv_2d(cnn_network, 30, 3, activation='relu')
cnn_network = max_pool_2d(cnn_network, 2)

cnn_network = conv_2d(cnn_network, 30, 3, activation='relu')
cnn_network = max_pool_2d(cnn_network, 2)

cnn_network = conv_2d(cnn_network, 40, 3, activation='relu')
cnn_network = max_pool_2d(cnn_network, 2)

cnn_network = conv_2d(cnn_network, 40, 3, activation='relu')
cnn_network = max_pool_2d(cnn_network, 2)

cnn_network = conv_2d(cnn_network, 40, 3, activation='relu')
cnn_network = max_pool_2d(cnn_network, 2)

cnn_network = conv_2d(cnn_network, 30, 3, activation='relu')
cnn_network = max_pool_2d(cnn_network, 2)

cnn_network = fully_connected(cnn_network, 100, activation='relu')
cnn_network = dropout(cnn_network, 0.5)

cnn_network = fully_connected(cnn_network, 50, activation='relu')

cnn_network = fully_connected(cnn_network, 2, activation='softmax')


# Train using classifier
cnn_network = regression(cnn_network, optimizer='adam',
                     loss='categorical_crossentropy',
                     learning_rate=0.001)

model = tflearn.DNN(cnn_network, tensorboard_verbose=0)
model.fit(X, Y, n_epoch=5, shuffle=True, validation_set=(X_test, Y_test),
          show_metric=True, batch_size=96, run_id='my_cnn')

model.save('my_cnn.tflearn')
