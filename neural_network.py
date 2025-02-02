import time

from keras.engine.saving import load_model
from keras.models import Sequential
from keras.layers import Dense, Dropout
from keras.layers.advanced_activations import LeakyReLU
from keras.optimizers import SGD, Adam
from keras.constraints import MaxNorm
from keras.regularizers import l2
import numpy as np
from tensorboard import summary

from globals import *
import globals

actions = {0: pygame.K_UP, 1: pygame.K_LEFT, 2: pygame.K_RIGHT}
DISCOUNT_FACTOR = 0.9
EPSILON = globals.STARTING_EPSILON
COUNT_FOR_EPSILON = 0
COUNT_FOR_TARGETNN_UPDATE = 0

PREVIOUS_NN_INPUT = []
PREVIOUS_NN_OUTPUT = []


def get_model(previous_weights):
    # model = Sequential()
    # model.add(Dense(units=720, kernel_regularizer=l2(1e-4), kernel_initializer="lecun_normal",
    #                 bias_initializer="lecun_normal"))
    # # model.add(LeakyReLU())
    # # model.add(Dropout(0.2))
    # model.add(Dense(units=200, kernel_regularizer=l2(1e-4), kernel_initializer="lecun_normal",
    #                 bias_initializer="lecun_normal"))
    # model.add(LeakyReLU())
    # model.add(Dense(units=60, kernel_regularizer=l2(1e-4), kernel_initializer="lecun_normal",
    #                 bias_initializer="lecun_normal"))
    # model.add(LeakyReLU())
    # model.add(Dense(units=3, activation='linear', kernel_regularizer=l2(1e-4), kernel_initializer="lecun_normal",
    #                 bias_initializer="lecun_normal"))
    #
    # model.compile(optimizer=Adam(lr=0.00025), loss='mean_squared_error')

    # model = Sequential()
    # model.add(Dense(units=128, activation='sigmoid', kernel_regularizer=l2(1e-2)))
    # # model.add(Dropout(0.2))
    # model.add(Dense(units=64, kernel_regularizer=l2(1e-4), kernel_initializer="lecun_normal",
    #                 bias_initializer="lecun_normal"))
    # model.add(LeakyReLU())
    # model.add(Dense(units=3, activation='linear', kernel_regularizer=l2(1e-4), kernel_initializer="lecun_normal",
    #                 bias_initializer="lecun_normal"))
    # model.compile(optimizer=SGD(lr=0.001, momentum=0.4, nesterov=True), loss='mean_squared_error')


    model = Sequential()
    model.add(Dense(units=128, activation="sigmoid", kernel_regularizer=l2(1e-4)))

    # model.add(LeakyReLU())
    model.add(Dense(units=64, kernel_regularizer=l2(1e-4), kernel_initializer="lecun_normal",
                    bias_initializer="lecun_normal"))
    model.add(LeakyReLU())
    model.add(Dense(units=3, activation='linear', kernel_regularizer=l2(1e-4), kernel_initializer="lecun_normal",
                    bias_initializer="lecun_normal"))

    model.compile(optimizer=SGD(lr=0.001, momentum=0.4, nesterov=True), loss='mean_squared_error')

    # model = Sequential()
    # model.add(Dense(units=250, kernel_constraint=MaxNorm(500), kernel_regularizer=l2(1e-4)))
    # model.add(LeakyReLU())
    # # model.add(Dropout(0.2))
    # model.add(Dense(units=25, kernel_regularizer=l2(1e-4), kernel_initializer="lecun_normal",
    #                 bias_initializer="lecun_normal"))
    # model.add(LeakyReLU())
    # model.add(Dense(units=3, activation='linear', kernel_regularizer=l2(1e-4), kernel_initializer="lecun_normal",
    #                 bias_initializer="lecun_normal"))
    #
    # model.compile(optimizer=Adam(lr=0.00025), loss='mean_squared_error')

    if previous_weights != 0:
        model.set_weights(previous_weights)

    return model


model = get_model(0)
target_model = get_model(model.get_weights())

# Pentru a continua antrenarea de la un anumit stadiu (salvat in model_trained_one_night1.h5
# care se gaseste la final in mario.py)
# model = load_model("./models/1578490617.382047_model_65_progress_01.h5")
model = load_model("./models/1578413784.776344_model_0_sare_peste_ziduri.h5")
# model = load_model("./models/1578527167.39178_model_340.h5")



print("Loaded model from disk")


def estimate_Q(current_state):
    return model.predict(np.array(current_state))


def estimate_Q_target(current_state):
    global COUNT_FOR_TARGETNN_UPDATE
    COUNT_FOR_TARGETNN_UPDATE += 1
    if COUNT_FOR_TARGETNN_UPDATE >= 5:
        print("Target NN Update")
        COUNT_FOR_TARGETNN_UPDATE = 0
        target_model.set_weights(model.get_weights())
    return target_model.predict(np.array(current_state))


def get_max_q(state, is_target=False):
    estimated_q_values = []
    if is_target:
        estimated_q_values = estimate_Q_target(state)[0]
    else:
        estimated_q_values = estimate_Q(state)[0]

    globals.Q_HISTORY += [estimated_q_values]

    max_action_index = 0
    max_q_value = 0

    if np.random.rand() < EPSILON:
        max_action_index = np.random.randint(0, 3)
        max_q_value = estimated_q_values[max_q_value]
    else:
        max_q_value = estimated_q_values[0]
        for index in range(1, 3):
            if estimated_q_values[index] > max_q_value:
                max_q_value = estimated_q_values[index]
                max_action_index = index

    #     index actiune,   actiune,      stare input,  output retea
    return max_action_index, max_q_value, state, estimated_q_values


def compute_y(reward, max_q):
    return reward + DISCOUNT_FACTOR * max_q


def compute_actual_value(next_state, reward, previous_q):
    max_index, max_q, useless_1, useless_2 = get_max_q(next_state, is_target=False)
    current_y = compute_y(reward, max_q)

    # [Q1, Q2, ... , R+y*maxQ, ... , Qn] = actual_value
    actual_value = []
    for elem_index in range(0, len(previous_q)):
        if elem_index != max_index:
            actual_value.append(previous_q[elem_index])
        else:
            actual_value.append(current_y)

    return actual_value


def train_network(next_state, reward, previous_state, previous_q):
    actual_value = compute_actual_value(next_state, reward, previous_q)
    print("=================")
    print(previous_q)
    print(actual_value)
    model.fit(np.array(previous_state), np.array([actual_value]))


def train_network_batch(batch_list):
    previous_states = []
    actual_values = []
    for batch in batch_list:
        previous_states.append(batch[2][0])
        actual_values.append(compute_actual_value(batch[0], batch[1], batch[3]))

    model.fit(np.array(previous_states), np.array(actual_values))
    print("=================")
    print(batch_list[0][3])
    print(actual_values[0])


def get_action_from_nn(current_state):
    global COUNT_FOR_EPSILON, EPSILON
    print("Current Epsilon: ", EPSILON)
    if EPSILON > 0.1:
        COUNT_FOR_EPSILON += 1
        if COUNT_FOR_EPSILON >= 400:
            COUNT_FOR_EPSILON = 0
            EPSILON -= 0.01
    # else:
    #     model.save(
    #         "./models/" + str(globals.TIME_STAMP) + "_model_" + str(globals.SAVES_COUNTER) + "_EPSILON_REACHED_0_1.h5")
    #     print("Model saved")

    action_index, q_value, previous_input, previous_output = get_max_q(current_state)
    current_action_val = actions[action_index]
    return current_action_val, previous_input, previous_output
