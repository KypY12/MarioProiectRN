from keras.models import Sequential
from keras.layers import Dense, Dropout
from keras.optimizers import SGD
from keras.regularizers import l2
import numpy as np

# Structura NN
model = Sequential()
model.add(Dense(units=100, activation='sigmoid', kernel_regularizer=l2(1e-4), kernel_initializer="lecun_normal"))
# model.add(Dropout(0.2))
model.add(Dense(units=10, activation='softmax', kernel_regularizer=l2(1e-4), kernel_initializer="lecun_normal"))

# Algoritmi
model.compile(optimizer=SGD(lr=0.1, momentum=0.9, nesterov=True), loss='categorical_crossentropy')

# Antrenament
# model.fit(x_train, y_train, validation_data=(x_val, y_val), epochs=20, batch_size=64)




