# -*- coding: utf-8 -*-
"""Mobilenet_v2 batch aug 0.001.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1VUJJh46T0__ytzndgLWBLXj2u7Wcxrc7
"""

import tensorflow as tf
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.layers import Dense, GlobalAveragePooling2D, BatchNormalization
from tensorflow.keras.regularizers import l2
from tensorflow.keras.datasets import cifar100
from tensorflow.keras.utils import to_categorical
import matplotlib.pyplot as plt

(x_train, y_train), (x_test, y_test) = cifar100.load_data(label_mode='fine')
# print(len(x_train),len(x_test))

x_train = x_train.astype('float32') / 255
x_test = x_test.astype('float32') / 255

num_classes = 100
y_train = to_categorical(y_train, num_classes)
y_test = to_categorical(y_test, num_classes)
print(x_test.shape)

print(x_test[0].shape)

import matplotlib.pyplot as plt
import numpy as np

image = x_train[0]
# Transpose the image
# image = image.transpose(2,3,1)
# Display the image
plt.imshow(image)

from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Dense, GlobalAveragePooling2D

l2_reg = 0.001

base_model = MobileNetV2(weights='imagenet', include_top=False, input_shape=(32, 32, 3))

x = base_model.output
x = GlobalAveragePooling2D()(x)
x = Dense(256, activation='relu', kernel_regularizer=l2(l2_reg))(x)
x = BatchNormalization()(x)
predictions = Dense(100, activation='softmax')(x)

# Create the model
model = tf.keras.models.Model(inputs=base_model.input, outputs=predictions)

for layer in base_model.layers:
        layer.trainable = False

# model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])



# datagen = ImageDataGenerator(width_shift_range=0.1, height_shift_range=0.1, horizontal_flip=True)

import tensorflow as tf
import matplotlib.pyplot as plt

learning_rates = [0.001]
num_epochs = 50
lr=0.001
model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=lr),
                  loss='categorical_crossentropy',
                  metrics=['accuracy'])

datagen = ImageDataGenerator(width_shift_range=0.1, height_shift_range=0.1, horizontal_flip=True)
datagen.fit(x_train)

history = model.fit(datagen.flow(x_train, y_train, batch_size=500),
                        steps_per_epoch=len(x_train) // 500,
                        epochs=num_epochs,
                        validation_data=(x_test, y_test))

plt.plot(range(1, num_epochs+1), history.history['loss'], label='lr={}'.format(lr))

plt.title('Loss vs. Number of Epochs')
plt.xlabel('Epoch')
plt.ylabel('Loss')
plt.legend(loc='upper right')
plt.show()

import matplotlib.pyplot as plt
plt.plot(history.history['loss'])
plt.plot(history.history['val_loss'])
plt.title('Model Loss')
plt.xlabel('Epoch')
plt.ylabel('Loss')
plt.legend(['Train', 'Validation'], loc='upper right')
plt.show()





