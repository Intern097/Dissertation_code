# -*- coding: utf-8 -*-
"""
Created on Thu Mar 12 23:06:42 2020
@author: Ioannis Theocharides 957865
"""
import tensorflow as tf
import keras
import keras.backend as k
from tensorflow.keras.layers import Conv2D, MaxPooling2D
from keras.layers import Flatten, Dense, Dropout
from keras.models import Sequential
from tensorflow.keras.losses import sparse_categorical_crossentropy
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.initializers import RandomNormal
import math


class Model:

    def __init__(self, data):

        (self.x_train, self.y_train), (self.x_test, self.y_test) = data
        self.x_train, self.x_test = (self.x_train/255.0).reshape((-1, 28, 28, 1)), \
                                    (self.x_test/255.0).reshape((-1, 28, 28, 1))
        self.y_train = k.cast(self.y_train, 'float32')
        self.y_test = k.cast(self.y_test, 'float32')
        self.batch_size = 128
        self.epochs = 20
        self.weight_init = RandomNormal()
        # Model
        self.model = self.build_model()
        self.opt = Adam(lr=0.001)
        # Print a model summary
        self.model.summary()
        self.training_loop()
        self.compile_model()
        # self.fit_model()
        # self.step(self.x_train, self.y_train)

    def build_model(self):
        model = Sequential()
        model.add(Conv2D(32, kernel_size=(3, 3), activation='relu',
                         kernel_initializer=self.weight_init, input_shape=(28, 28, 1)))
        model.add(Conv2D(64, (3, 3), activation='relu', kernel_initializer=self.weight_init))
        model.add(MaxPooling2D(pool_size=(2, 2)))
        model.add(Dropout(0.25))
        input_layer = Flatten()
        model.add(input_layer)
        hidden_layer_1 = Dense(128, activation='relu', kernel_initializer=self.weight_init)
        model.add(hidden_layer_1)
        hidden_layer_2 = Dropout(0.3)
        model.add(hidden_layer_2)
        outer_layer = Dense(10, activation='softmax', kernel_initializer=self.weight_init)
        model.add(outer_layer)
        return model

    def step(self, x_true, y_true):
        with tf.GradientTape() as tape:
            pred = self.model(x_true)
            loss = sparse_categorical_crossentropy(y_true, pred)

        grads = tape.gradient(loss, self.model.trainable_variables)
        self.opt.apply_gradients(zip(grads, self.model.trainable_variables))

    # def create_loss(self, y_true, y_pred):
    #     loss = k.sum(k.log(y_true) - k.log(y_pred))
    #     return loss

    def training_loop(self):
        bat_per_epoch = math.floor(len(self.x_train) / self.batch_size)
        for epoch in range(self.epochs):
            print('=', end='')
            for i in range(bat_per_epoch):
                n = i * self.batch_size
                self.step(self.x_train[n:(n + self.batch_size)], self.y_train[n:n + self.batch_size])

    def compile_model(self):
        self.model.compile(loss=Loss_function.loss, optimizer=self.opt, metrics=['accuracy'])

    # def fit_model(self):
    #     self.model.fit(self.x_train, self.y_train, epochs=self.epochs)

    def return_score(self):
        score = self.model.evaluate(self.x_test, self.y_test)
        print('accuracy', score[1])


class Loss_function:

    @staticmethod
    def loss(y_true, y_pred):
        loss = k.sum(k.log(y_true) - k.log(y_pred))
        return loss


mnist = keras.datasets.mnist
x = Model(mnist.load_data())
x.return_score()
