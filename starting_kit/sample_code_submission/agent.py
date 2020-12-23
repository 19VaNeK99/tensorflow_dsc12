# -*- coding: utf-8 -*-
"""Reinforced Learning Algorithm Template

This module contains function of player.

Example:
    >>> agent(game)

"""


from tensorflow import keras
import numpy as np
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, Flatten,Conv2D
import os
import copy

direction = ['up', 'down', 'left', 'right']


def ret_obser(env):
    observation = [[] for i in range(len(env.GetCurrentState()[0]))]
    column = 0
    a_c = -1
    a_r = -1
    c = 0
    r = 0
    for i in env.GetCurrentState()[0]:
        r = 0
        for j in i:
            if 'e' in j.ToString()[1]:
                observation[column].append(0.)
            if 'wall' in j.ToString()[1]:
                observation[column].append(-1.)
            if 'product' in j.ToString()[1]:
                observation[column].append(1.)
            if 'AGENT' in j.ToString()[1]:
                observation[column].append(5.)
                a_r = c
                a_c = r
            r += 1
        column += 1
        c += 1

    new_observation = [[] for i in range(7)]
    start_r = a_r - 3
    start_c = a_c - 3
    for i in range(7):
        start_c = a_c - 3
        for j in range(7):
            if  start_r < 0 or start_c < 0 or start_c >= len(observation[0]) or start_r >= len(observation):
                new_observation[i].append(-1)
            else:
                new_observation[i].append(observation[start_r][start_c])
            start_c += 1
        start_r += 1

    return np.array(new_observation).reshape(49)


def gather_data(env_orig):
    num_trials = 1000
    min_score = 100
    sim_steps = 1300
    mxscore = 0
    trainingX, trainingY = [], []
    env = copy.deepcopy(env_orig)
    scores = []
    env.Show()
    for _ in range(num_trials):
    #while len(trainingX) == 0:
        env = copy.deepcopy(env_orig)
        observation = ret_obser(env)
        score = 0
        training_sampleX, training_sampleY = [], []
        done = False
        while not done:
            # action corresponds to the previous observation so record before step
            #env.Show()
            #action = int(input())
            action = np.random.randint(0, 3)
            one_hot_action = np.zeros(4)
            one_hot_action[action] = 1
            training_sampleX.append(observation)
            training_sampleY.append(one_hot_action)

            fignya, reward, done = env.Move(direction[action])
            observation = ret_obser(env)
            score = reward
        #print(score)
        if score  > mxscore:
            mxscore = score
            trainingX = training_sampleX
            trainingY = training_sampleY
        print(score, mxscore)
    trainingX, trainingY = np.array(trainingX), np.array(trainingY)
    print("Average: {}".format(np.mean(scores)))
    print("Median: {}".format(np.median(scores)))
    return trainingX, trainingY


def fit_gather_data(env_orig, model):
    num_trials = 100
    mxscore = 0
    trainingX, trainingY = [], []
    env = copy.deepcopy(env_orig)
    scores = []
    #env.Show()
    for _ in range(num_trials):
        env = copy.deepcopy(env_orig)
        observation = ret_obser(env)
        score = 0
        training_sampleX, training_sampleY = [], []
        done = False
        count = 0
        while not done:
            observation = np.array(observation)

            if count == 3:
                action = np.random.randint(0, 3)
                count = 0
            else:
                action = np.argmax(model.predict(observation.reshape(1,49)))

            one_hot_action = np.zeros(4)
            one_hot_action[action] = 1
            training_sampleX.append(observation)
            training_sampleY.append(one_hot_action)

            fignya, reward, done = env.Move(direction[action])
            observation = ret_obser(env)
            score = reward
            count += 1
        # print(score)
        if score > mxscore:
            mxscore = score
            trainingX = training_sampleX
            trainingY = training_sampleY
        print(score, mxscore)

    trainingX, trainingY = np.array(trainingX), np.array(trainingY)
    print("Average: {}".format(np.mean(scores)))
    print("Median: {}".format(np.median(scores)))

    return trainingX, trainingY

def create_model():
    model = Sequential()
    model.add(Dense(64, input_shape=(49,), activation="relu"))
    model.add(Dropout(0.4))
    model.add(Dense(128, activation="relu"))
    model.add(Dropout(0.4))
    model.add(Dense(32, activation="relu"))
    model.add(Dropout(0.4))
    model.add(Dense(4, activation="softmax"))
    model.compile(
        loss="categorical_crossentropy",
        optimizer="adam",
        metrics=["accuracy"])
    print(model.summary())
    return model


def predict(g):
    env = g
    env_c = copy.deepcopy(env)
    directory = os.getcwd()
    files = os.listdir(directory)
    m = ""
    for i in files:
        if 'h5' in i:
            m = i
    model = ""
    if not m:
        model = create_model()
    else:
        try:
            model = keras.models.load_model(m)
        except:
            print("Ошибка загрузки " + m + " модели")
            exit()
    trainingX, trainingY = fit_gather_data(copy.deepcopy(env), model)
    #trainingX, trainingY = gather_data(copy.deepcopy(env))
    if len(trainingX) == 0:
        return
    model.fit(trainingX, trainingY, epochs=25)

    score = 0
    num_trials = 50
    sim_steps = 500
    for _ in range(1):
        observation = ret_obser(env_c)

        print(observation)
        score = 0
        #env_c.Show()
        for step in range(sim_steps):
            observation = np.array(observation)

            action = np.argmax(model.predict(observation.reshape(1,49)))
            print(action)
            fignya, reward, done = env_c.Move(direction[action])
            #env_c.Show()
            print(reward)
            observation = ret_obser(env_c)
            score = reward
            if done:
                break

    print(score)
    model.save('my_model.h5')



import os
def agent(g):
    d = os.path.abspath(__file__)
    print(d)
    for i in range(len(d)-1, -1, -1):
        if d[i] == '/':
            d = d[:i]
            break
    print(d)

    field, score, isGameOver = g.GetCurrentState()
    actionsList = ['up', 'down', 'left', 'right']
    model = keras.models.load_model(f'{d}/my_model.h5')
    print(len(field))

    score = 0
    count = 0
    while not isGameOver:
        observation = ret_obser(g)
        observation = np.array(observation)
        action = np.argmax(model.predict(observation.reshape(1,49)))
        g.Move(actionsList[action])
        field, score, isGameOver = g.GetCurrentState()
        g.Show()
        print(action)
        count += 1
    print(score)
