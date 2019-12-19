from keras.models import Sequential
from keras.layers import Dense, Dropout
from keras.optimizers import SGD
from keras.regularizers import l2
import numpy as np
from globals import *

actions = {pygame.K_UP: 1, pygame.K_LEFT: 2, pygame.K_RIGHT: 3}

# Structura NN
model = Sequential()
model.add(Dense(units=100, activation='sigmoid', kernel_regularizer=l2(1e-4), kernel_initializer="lecun_normal"))
# model.add(Dropout(0.2))
model.add(Dense(units=1, activation='softmax', kernel_regularizer=l2(1e-4), kernel_initializer="lecun_normal"))

# Algoritmi
model.compile(optimizer=SGD(lr=0.1, momentum=0.9, nesterov=True), loss='categorical_crossentropy')


# Antrenament
# model.fit(x_train, y_train, validation_data=(x_val, y_val), epochs=20, batch_size=64)


def estimate_Q(current_state, action):
    return model.predict(np.array(current_state + [action]))


def get_max_Q(current_state):
    Q_values = []
    for action in actions.items():
        current_Q = estimate_Q(current_state, action[1])
        Q_values += [(action[0], action[1], current_Q)]

    max_action = max(Q_values, key=lambda t: t[2])
    return max_action


def compute_actual_value(reward, discount_factor, max_action_q):
    return reward + discount_factor * max_action_q


def train_network(previous_state, previous_action, actual_value):
    model.fit([previous_state + [previous_action]], [actual_value], epochs=5, batch_size=64)


def get_action_from_nn(current_state, current_action):
    current_action_val = actions[current_action]

