#get the data
#view sample images and classes
#transforming the dataset to a 1d array after reshaping all the images 32*32*3
#normalize the data
#knowing the distribution of class in data
#encoding the categorical variable to numeric
#building deep neural network
#predicting
#visualize inspection of prediction

import os
import re

import keras.layers
import numpy as np
from keras import Sequential
import matplotlib.pyplot as plt
import pandas as pd
from keras.layers import Dense,Flatten,Softmax,InputLayer
import imageio.v2 as imageio
from PIL import Image
from sklearn.preprocessing import LabelEncoder
from keras.utils.np_utils import to_categorical
import tensorflow as tf
import keras_lr_finder as lr_find
from clr_callback import *

#get the data
train = pd.read_csv('../datasets/train.csv')
test = pd.read_csv('../datasets/test.csv')

#view sample images and classes
# img_name=os.path.join('datasets/Train',train['ID'][2010])
# img=imageio.imread(img_name)
# print(f'class:{train["Class"][2010]}')
# plt.imshow(img)
# plt.show()

#transform the data from 32*32*3
#transforming the dataset to a 1d array after reshaping all the images 32*32*3
temp=[]
for img_name in train['ID']:
    img_path=os.path.join('../datasets/Train', img_name)
    img=imageio.imread(img_path)
    img=np.array(Image.fromarray(img).resize((32,32))).astype('float32')
    temp.append(img)

# print(temp)

x_train=np.stack(temp)
temp=[]
# for img_name in test['ID']:
#     img_path=os.path.join('datasets/Test',img_name)
#     img=imageio.imread(img_path)
#     img=np.array(Image.fromarray(img).resize((32,32))).astype('float32')
#     temp.append(img)
# x_test=np.stack(temp)

#normalize the data
x_train=x_train/255
# x_test=x_test/255



#knowing the distribution of class in data
# print(train['Class'].value_counts(normalize=True))


#encoding the categorical variable to numeric
lb=LabelEncoder()
y_train=lb.fit_transform(train['Class'])
print(y_train)
y_train=to_categorical(y_train)
print(y_train)


#build neural network
input_layer_size=(32,32,3)
hidden_layer_size=500
output_layer_size=3
epochs=100
batch_size=128


model = Sequential([
            keras.layers.Flatten(input_shape=input_layer_size),
            keras.layers.Dense(hidden_layer_size, activation='relu'),
            keras.layers.Dense(output_layer_size, activation='softmax')
        ])
model.compile(loss='categorical_crossentropy',optimizer=tf.optimizers.Adam(),metrics=['accuracy'])
# model.fit(x_train,y_train,batch_size=batch_size,epochs=epochs,validation_split=0.2)
lr_finder=lr_find.LRFinder(model)

# Training can stop abruptly if rate is set too high. In such cases, reduce the value of end_lr.
lr_finder.find(x_train,y_train,start_lr=0.0001,end_lr=0.09,batch_size=batch_size,epochs=epochs)
#plot the loss, ignore 20 batches in the beginning and 5 in the end
lr_finder.plot_loss(n_skip_beginning=20,n_skip_end=5)
plt.show()

#pass the values of base_lr with the value of
cb_triangular=CyclicLR(base_lr=0.0001,max_lr=0.001, step_size=2000., mode='triangular2')
#witing graph will take time. Hence, keeping it False
cb_save=keras.callbacks.TensorBoard(log_dir='learning_rate', write_graph=False)

model.fit(x_train,y_train,batch_size=batch_size,epochs=epochs,validation_split=0.2,callbacks=[cb_triangular,cb_save],verbose=1)

print('model built successfully')

plt.xlabel('Training Iterations')
plt.ylabel('Learning Rate')
plt.title('CLR - triangular2 policy')
plt.plot(cb_triangular.history['iterations'],cb_triangular.history['lr'])