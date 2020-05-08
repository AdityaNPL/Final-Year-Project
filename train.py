from Environment import Empty
import matplotlib.pyplot as plt
from Model import CommNet
import numpy as np
import tensorflow as tf
import random

def train(sess, env, actor, critic):
    sess.run(tf.compat.v1.global_variables_initializer())

    actor.update_target_network()
    critic.update_target_network()

    epRewardHistoryCommNet = []
    labelsCommNet = []

    for i in range(episodes):
        print(str(i+1) + " / " + str(episodes) )
        state = env.reset()

        ep_reward = 0

        done = [False for _ in range(env.n_agents)]

        while not all(done):
            actionDistribution = actor.predict([state])[0]
            actionForEnv = [np.argmax(x) for x in actionDistribution]

            newState, reward, done, info = env.step(actionForEnv)
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



episodes = 200
hiddenValueLengths = 10
numOfAgents = 3
observationLength = 6
numOfActions = 27

learningRate = 0.001
tau = 0.2
gamma = 0.8

labels = []
episodeRewards = []
tf.compat.v1.set_random_seed(42)
tf.compat.v1.reset_default_graph()
config = tf.compat.v1.ConfigProto()
config.gpu_options.allow_growth = True
with tf.compat.v1.Session(config=config) as sess:
    env = Empty.EmptyWorld()

    action_dim = (numOfAgents, numOfActions)

    actor = CommNet.ActorNetwork(sess, action_dim, learningRate, tau)

    critic = CommNet.CriticNetwork(sess, learningRate, tau, gamma, actor.get_num_trainable_vars())

    labels, episodeRewards = train(sess, env, actor, critic)

"""#### Plot the Learning Curve"""

# print(labels)
# print(episodeRewards)
avgEpRewardCommNet = []
avgLabelsCommNet = []
avgVal = 0
step = 10
for i in labels:
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
