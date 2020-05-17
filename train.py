import math
import time
import sys
import subprocess
import random
from random import randint
import csv
import matplotlib.pyplot as plt
import numpy as np
import tensorflow as tf
from Model import CommNet
from Robots import Adversary, Ally
from Environment import Empty


def simulate(sess, actor):
    env = Empty.EmptyWorld(True)
    sess.run(tf.compat.v1.global_variables_initializer())

    state = env.reset()
    done = False
    counter = 0 
    while not done:
        counter += 1
        print(counter)
        actionDistribution = actor.predict([state])[0]
        actionForEnv = [np.argmax(x) for x in actionDistribution]

        newState, reward, done = env.step(actionForEnv)
        state = newState
    env.printToFile(True)

def train(sess, env, actor, critic):
    sess.run(tf.compat.v1.global_variables_initializer())

    actor.update_target_network()
    critic.update_target_network()

    epRewardHistoryCommNet = []
    labelsCommNet = []

    for i in range(episodes):
        percentage = (i*100.00)/episodes 
        if percentage % 10 == 0: 
            print(str(percentage) + "%")
        
        state = env.reset()

        ep_reward = 0

        done = False

        while not done:
            actionDistribution = actor.predict([state])[0]
            actionForEnv = [np.argmax(x) for x in actionDistribution]

            newState, reward, done = env.step(actionForEnv)
            reward = np.sum(reward)

            stateTrain = [state]
            actionTrain = [actionDistribution]
            rewardTrain = [reward]
            newStateTrain = [newState]

            # Update the critic network given the action, rewards and observations
            predicted_q_value, _, loss = critic.train(stateTrain, actionTrain, np.reshape(rewardTrain, (1, 1)))

            # Update the actor network (policy) using the gradient from the critic
            a_outs = actor.predict(stateTrain)
            grads = critic.action_gradients(stateTrain, a_outs)
            actor.train(stateTrain, grads[0])

            actor.update_target_network()
            critic.update_target_network()

            state = newState
            ep_reward += reward

        epRewardHistoryCommNet.append(ep_reward)
        labelsCommNet.append(i+1)

    return (labelsCommNet,epRewardHistoryCommNet)

def printTrainingCurve(labels, episodeRewards):
    avgEpRewardCommNet = []
    avgLabelsCommNet = []
    avgVal = 0
    step = 3
    for i in labels:
        if i == 1:
            continue
        avgVal += episodeRewards[i-1]
        if i % step == 0:
            avgEpRewardCommNet.append(avgVal/step)
            avgLabelsCommNet.append(i)
            avgVal = 0

    figCommNet = plt.figure(figsize=(6, 5))
    axCommNet = figCommNet.add_subplot(111)
    axCommNet.plot(avgLabelsCommNet, avgEpRewardCommNet)
    axCommNet.set_title("Learning Curve")
    axCommNet.set_ylabel("Episodic Reward")
    axCommNet.set_xlabel("Episodes")
    plt.tight_layout()
    plt.show()


episodes = 1000
learningRate = 0.4
tau = 1
gamma = 0.7

numOfAgents = 3
numOfActions = 27

labels = []
episodeRewards = []
tf.compat.v1.set_random_seed(42)
tf.compat.v1.reset_default_graph()
config = tf.compat.v1.ConfigProto()
config.gpu_options.allow_growth = True
with tf.compat.v1.Session(config=config) as sess:
    env = Empty.EmptyWorld(False)

    action_dim = (numOfAgents, numOfActions)

    actor = CommNet.ActorNetwork(sess, action_dim, learningRate, tau)

    critic = CommNet.CriticNetwork(sess, learningRate, tau, gamma, actor.get_num_trainable_vars())

    labels, episodeRewards = train(sess, env, actor, critic)

    printTrainingCurve(labels, episodeRewards)

    simulate(sess, actor)
