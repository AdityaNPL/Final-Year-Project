import math
import time
import sys
import subprocess
import random
import csv
import matplotlib.pyplot as plt
import numpy as np
import tensorflow as tf

class Adversary():

    def __init__(self, id, realSim):
        self.id = id
        self.step = 0
        self.maxSpeed = 5
        self.pos = [0,0,0]
        self.history = {}
        self.allies = []
        self.newPos = [0,0,0]
        self.realSim = realSim
        self.timer_start = time.time()
        self.timer_end = time.time()
        self.no_of_move_calls = 0
        # self.grid_distribution = [[0 for i in range(self.grid_ui_obj.grid_width/100+1)] for j in range(self.grid_ui_obj.grid_height/100+1)]
        self.avgDistFromCenter = 0
        self.dataToAnalyse = []

    def setAllies(self, allies):
        self.allies = allies

    def calcStatus(self):
        if self.realSim:
            self.pos = gs.roboStat(self.id)
        self.history[self.step] = self.pos


    def printHistory(self, write):
        self.calcStatus()
        # print("########################################")
        # print("Robo:" + str(self.id))

        posList = []
        for key in self.history.keys():
            posList.append([key,self.history[key][0],self.history[key][1],self.history[key][2]])
        for i in range(len(posList)):
            speed = [0,0,0]
            pos = posList[i]
            if i != 0:
                speed = [pos[1] - posList[i-1][1], pos[2]- posList[i-1][2], pos[3]- posList[i-1][3]]
            self.dataToAnalyse.append((pos[0],pos[1],pos[2],pos[3],speed[0],speed[1],speed[2]))

        if write:
            with open('./DataDump/data_adv'+str(self.id)+'.csv', 'w+') as out:
                for data in self.dataToAnalyse:
                    out.write("%s,%s,%s,%s,%s,%s,%s\n"%data)


    def move(self, x, y, z):
        if z<2:
            z = 2
        if self.realSim:
            subprocess.check_output(["rosrun","rotors_gazebo", "waypoint_publisher", str(x), str(y), str(z), str(0), "__ns:=firefly"+str(self.id)])
        else:
            self.pos = [x,y,z]

    def setup(self):
        self.pos = [random.uniform(-10,10),random.uniform(-10,10),random.uniform(40,60)]
        self.move(self.pos[0], self.pos[1], self.pos[2])

    def calcVector(self):
        direction = [0,0,0]
        for opponent in self.allies:
            vector = list(map(lambda x: x*0.1, self.getVector(opponent.pos, self.pos)))
            for i in range(3):
                direction[i] += vector[i]

        vectorToCenter = self.getVector(self.pos, [0,0,50])
        vectors = [vectorToCenter]
        self.avgDistFromCenter += self.magnitude(vectorToCenter)
        vectors.append(self.getVector([self.pos[0],self.pos[1],200], self.pos))
        vectors.append(self.getVector([self.pos[0],self.pos[1],2], self.pos))
        vectors.append(self.getVector([self.pos[0],-200,self.pos[2]], self.pos))
        vectors.append(self.getVector([self.pos[0],200,self.pos[2]], self.pos))
        vectors.append(self.getVector([-200,self.pos[1],self.pos[2]], self.pos))
        vectors.append(self.getVector([200,self.pos[1],self.pos[2]], self.pos))
        for vector in vectors:
            for i in range(3):
                direction[i] += vector[i]

        for i in range(3):
            if abs(direction[i]) > self.maxSpeed:
                direction[i] = direction[i]/direction[i] * self.maxSpeed

        return [self.pos[0] + direction[0], self.pos[1] + direction[1], self.pos[2] + direction[2]]

    def getVector(self, start, end):
        return[end[0]-start[0], end[1]-start[1], end[2]-start[2]]

    def calcWaypoints(self):
        self.calcStatus()
        self.step += 1
        self.newPos = self.calcVector()


    def runMove(self):
        self.move(self.newPos[0], self.newPos[1], self.newPos[2])

    def magnitude(self, vector):
        return math.sqrt(vector[0]**2 + vector[1]**2 + vector[2]**2 )

class Ally:
    def __init__(self, id, realSim):
         self.id = id
         self.step = 0
         self.maxSpeed = 5
         self.prey = [0,0,0]
         self.pos = [0,0,0]
         self.history = {}
         self.allies = []
         self.adv = None
         self.newPos = [0,0,0]
         self.realSim = realSim
         self.dataToAnalyse = []

    def setAllies(self, allies):
        self.allies = allies

    def setAdv(self, adv):
        self.adv = adv

    def calcStatus(self):
        if self.realSim:
            self.pos = gs.roboStat(self.id)
        self.history[self.step] = self.pos

    def printHistory(self, write):
        self.calcStatus()
        # print("########################################")
        # print("Robo:" + str(self.id))

        posList = []
        for key in self.history.keys():
            posList.append([key,self.history[key][0],self.history[key][1],self.history[key][2]])
        for i in range(len(posList)):
            speed = [0,0,0]
            pos = posList[i]
            if i != 0:
                speed = [pos[1] - posList[i-1][1], pos[2]- posList[i-1][2], pos[3]- posList[i-1][3]]
            self.dataToAnalyse.append((pos[0],pos[1],pos[2],pos[3],speed[0],speed[1],speed[2]))

        if write:
            with open('./DataDump/data_'+str(self.id)+'.csv', 'w+') as out:
                for data in self.dataToAnalyse:
                    out.write("%s,%s,%s,%s,%s,%s,%s\n"%data)

    def move(self, x, y, z):
        if z<2:
            z = 2
        if self.realSim:
            subprocess.check_output(["rosrun","rotors_gazebo", "waypoint_publisher", str(x), str(y), str(z), str(0), "__ns:=firefly"+str(self.id)])
        else:
            self.pos = [x,y,z]

    def setup(self):
        x,y,z = (random.uniform(-50,50),random.uniform(-50,50),0)
        if self.realSim:
            subprocess.check_output(["rosrun","rotors_gazebo", "waypoint_publisher", str(x), str(y), str(z), str(0), "__ns:=firefly"+str(self.id)])
        # print(x,y,z)

    def checkCollision(self):
        if self.newPos[2]<10:
            self.newPos[2] = 10
        for ally in self.allies:
            if ally.id != self.id:
                ally.calcStatus()
                allyPos = ally.pos
                for i in range(3):
                    if allyPos[i] == self.newPos[i]:
                        self.newPos[i] += 1

    def calcWaypoints(self, direction):
        self.calcStatus()
        for i in range(3):
            self.newPos[i] = self.pos[i] + (direction[i] * self.maxSpeed)
        self.checkCollision()

    def runMove(self):
        self.move(self.newPos[0], self.newPos[1], self.newPos[2])


class CommunicationNetwork:
    @staticmethod
    def createLayers(observation):
        H0 = CommunicationNetwork.encoder(observation)
        C0 = tf.zeros(tf.shape(input=H0), name="C0")
        H1, C1 = CommunicationNetwork.execLayer("execLayer1", H0, C0)
        H2, C2 = CommunicationNetwork.execLayer("execLayer2", H1, C1)
        H3, _ = CommunicationNetwork.execLayer("execLayer3", H2, C2)
        return H3

    @staticmethod
    def actor_build_network(name, observation):
        with tf.compat.v1.variable_scope(name):
            H = CommunicationNetwork.createLayers(observation)
            return CommunicationNetwork.getActorActionDistribution(H)

    @staticmethod
    def critic_build_network(name, observation, action):
        with tf.compat.v1.variable_scope(name):
            H = CommunicationNetwork.createLayers(observation)
            return CommunicationNetwork.getCriticBaseline(H, action)

    @staticmethod
    def encoder(observation):
        observation = observation[0]
        H = []
        with tf.compat.v1.variable_scope("encoder", reuse=tf.compat.v1.AUTO_REUSE):
            for j in range(numOfAgents):
                encoded = tf.compat.v1.layers.dense(tf.reshape(observation[j], (1, observationLength)), hiddenValueLengths, name="dense")
                H.append(tf.squeeze(encoded))
            H = tf.stack(H)
            H = tf.reshape(H, (numOfAgents, hiddenValueLengths))

        return H

    @staticmethod
    def module(h, c):
        with tf.compat.v1.variable_scope("module", reuse=tf.compat.v1.AUTO_REUSE):
            w_H = tf.compat.v1.get_variable(name='w_H', shape=hiddenValueLengths,
                                  initializer=tf.compat.v1.keras.initializers.VarianceScaling(scale=1.0, mode="fan_avg", distribution="uniform"))
            w_C = tf.compat.v1.get_variable(name='w_C', shape=hiddenValueLengths,
                                  initializer=tf.compat.v1.keras.initializers.VarianceScaling(scale=1.0, mode="fan_avg", distribution="uniform"))

            tf.compat.v1.summary.histogram('w_H', w_H)
            tf.compat.v1.summary.histogram('w_C', w_C)

            return tf.tanh(tf.multiply(w_H, h) + tf.multiply(w_C, c))

    @staticmethod
    def execLayer(name, H, C):
        batch_size = 1
        with tf.compat.v1.variable_scope(name):
            next_H = tf.zeros(shape=(batch_size, 0, hiddenValueLengths))
            for j in range(numOfAgents):
                h = H[:, j]
                c = C[:, j]
                # print(h)
                # print(c)
                next_h = CommunicationNetwork.module(h, c)
                next_H = tf.concat([next_H, tf.reshape(next_h, (batch_size, 1, hiddenValueLengths))], 1)

            next_H = tf.identity(next_H, "H")

            next_C = tf.zeros(shape=(batch_size, 0, hiddenValueLengths))
            for j1 in range(numOfAgents):
                next_c = []
                for j2 in range(numOfAgents):
                    if j1 != j2:
                        next_c.append(next_H[:, j2])
                next_c = tf.reduce_mean(input_tensor=tf.stack(next_c), axis=0)
                next_C = tf.concat([next_C, tf.reshape(next_c, (batch_size, 1, hiddenValueLengths))], 1)


            return next_H, tf.identity(next_C, "C")

    @staticmethod
    def getActorActionDistribution(H):
        with tf.compat.v1.variable_scope("actor_output"):
            w_out = tf.compat.v1.get_variable(name='w_out', shape=(hiddenValueLengths, numOfActions),
                                    initializer=tf.compat.v1.keras.initializers.VarianceScaling(scale=1.0, mode="fan_avg", distribution="uniform"))
            b_out = tf.compat.v1.get_variable(name='b_out', shape=numOfActions, initializer=tf.compat.v1.zeros_initializer())

            tf.compat.v1.summary.histogram('w_out', w_out)
            tf.compat.v1.summary.histogram('b_out', b_out)

            batch_size = tf.shape(input=H)[0]

            actions = []
            for j in range(numOfAgents):
                h = tf.slice(H, [0, j, 0], [batch_size, 1, hiddenValueLengths])
                w_out_batch = tf.tile(tf.expand_dims(w_out, axis=0), [batch_size, 1, 1])
                action =  tf.squeeze(tf.matmul(h, w_out_batch) + b_out, [1])

                actions.append(action)
            actions = tf.stack(actions, name="actions", axis=1)

        return actions

    @staticmethod
    def getCriticBaseline(H, action):
        with tf.compat.v1.variable_scope("critic_output", reuse=tf.compat.v1.AUTO_REUSE):
            baseline = tf.compat.v1.layers.dense(inputs=tf.concat([H, action], 2),
                                       units=1,
                                       activation=tf.tanh,
                                       kernel_initializer=tf.compat.v1.keras.initializers.VarianceScaling(scale=1.0, mode="fan_avg", distribution="uniform"))
            baseline = tf.squeeze(baseline, [2])
            baseline = tf.compat.v1.layers.dense(inputs=baseline,
                                       units=1,
                                       kernel_initializer=tf.compat.v1.keras.initializers.VarianceScaling(scale=1.0, mode="fan_avg", distribution="uniform"))
            tf.compat.v1.summary.histogram("w_baseline", tf.compat.v1.get_variable("dense/kernel"))

            return baseline

class ActorNetwork(object):

    """
    This network will provide the action probability distribution as the policy for the agents given the observations and using the parameters optimised via the critic
    """
    def __init__(self, sess, action_dim, learning_rate, tau, batch_size = 1):
        self.sess = sess
        self.action_dim = action_dim
        self.learning_rate = learning_rate
        self.tau = tau
        self.batch_size = batch_size

        self.inputs, self.out = self.create_actor_network("actor_network")
        self.network_params = tf.compat.v1.trainable_variables()

        self.create_actor_network("target_actor_network")
        self.target_network_params = tf.compat.v1.trainable_variables()[
                                     len(self.network_params):]

        with tf.compat.v1.name_scope("actor_update_target_network_params"):
            self.update_target_network_params = [self.target_network_params[i].assign(tf.multiply(self.network_params[i], self.tau) + tf.multiply(self.target_network_params[i], 1. - self.tau)) for i in range(len(self.target_network_params))]

        self.action_gradient = tf.compat.v1.placeholder(tf.float32, (self.batch_size, self.action_dim[0], self.action_dim[1]), name="action_gradient")

        with tf.compat.v1.name_scope("actor_gradients"):
            self.unnormalized_actor_gradients = tf.gradients(ys=self.out, xs=self.network_params, grad_ys=-self.action_gradient)
            self.actor_gradients = list(map(lambda x: tf.compat.v1.div(x, self.batch_size), self.unnormalized_actor_gradients))

        self.optimize = tf.compat.v1.train.AdamOptimizer(self.learning_rate)
        self.optimize = self.optimize.apply_gradients(zip(self.actor_gradients, self.network_params))

        self.num_trainable_vars = len(self.network_params) + len(self.target_network_params)

    def create_actor_network(self, name):
        inputs = tf.compat.v1.placeholder(tf.float32, shape=(self.batch_size, numOfAgents, observationLength), name="actor_inputs")
        out = CommunicationNetwork.actor_build_network(name, inputs)
        return inputs, out

    def train(self, inputs, action_gradient):
        self.sess.run(self.optimize, feed_dict={
            self.inputs: inputs,
            self.action_gradient: action_gradient
        })

    def predict(self, inputs):
        return self.sess.run(self.out, feed_dict={
            self.inputs: inputs
        })

    def update_target_network(self):
        self.sess.run(self.update_target_network_params)

    def get_num_trainable_vars(self):
        return self.num_trainable_vars


class CriticNetwork(object):
    """
    This network will estimate the Q-value given the observations and actions
    """

    def __init__(self, sess, learning_rate, tau, gamma, num_actor_vars, batch_size = 1):
        self.sess = sess
        self.learning_rate = learning_rate
        self.tau = tau
        self.gamma = gamma
        self.batch_size = batch_size

        self.inputs, self.action, self.out = self.create_critic_network("critic_network")
        self.network_params = tf.compat.v1.trainable_variables()[num_actor_vars:]

        self.target_inputs, self.target_action, self.target_out = self.create_critic_network("target_critic_network")
        self.target_network_params = tf.compat.v1.trainable_variables()[(len(self.network_params) + num_actor_vars):]

        with tf.compat.v1.name_scope("critic_update_target_network_params"):
            self.update_target_network_params = \
                [self.target_network_params[i].assign(tf.multiply(self.network_params[i], self.tau)
                                                      + tf.multiply(self.target_network_params[i], 1. - self.tau))
                 for i in range(len(self.target_network_params))]

        self.predicted_q_value = tf.compat.v1.placeholder(tf.float32, (self.batch_size, 1), name="predicted_q_value")

        self.loss = tf.compat.v1.losses.mean_squared_error(self.predicted_q_value, self.out)

        self.optimize = tf.compat.v1.train.AdamOptimizer(
            self.learning_rate).minimize(self.loss)

        self.action_grads = tf.gradients(ys=self.out, xs=self.action, name="action_grads")

    def create_critic_network(self, name):
        inputs = tf.compat.v1.placeholder(tf.float32, shape=(self.batch_size, numOfAgents, observationLength), name="critic_inputs")
        action = tf.compat.v1.placeholder(tf.float32, shape=(self.batch_size, numOfAgents, numOfActions), name="critic_action")

        out = CommunicationNetwork.critic_build_network(name, inputs, action)
        return inputs, action, out

    def train(self, inputs, action, predicted_q_value):
        return self.sess.run([self.out, self.optimize, self.loss], feed_dict={
            self.inputs: inputs,
            self.action: action,
            self.predicted_q_value: predicted_q_value
        })

    def predict(self, inputs, action):
        return self.sess.run(self.out, feed_dict={
            self.inputs: inputs,
            self.action: action
        })

    def action_gradients(self, inputs, actions):
        return self.sess.run(self.action_grads, feed_dict={
            self.inputs: inputs,
            self.action: actions
        })

    def update_target_network(self):
        self.sess.run(self.update_target_network_params)


class EmptyWorld:
    def __init__(self):
        self.n_agents = 3
        self.allies = []
        self.adv = Adversary(4, False)
        self.step = 0
        self.maxIterations = 100
        for i in range(3):
            self.allies.append(Ally(i+1, False))

        for ally in self.allies:
            ally.setup()
            ally.setAllies(self.allies)
            ally.setAdv(self.adv)

        self.adv.setup()
        self.adv.setAllies(self.allies)

    def reset(self):
        return self.getObservations()

    def getObservations(self):
        observations = []
        self.adv.calcStatus()
        advPos = self.adv.pos
        for ally in self.allies:
            ally.calcStatus()
            observations.append((ally.pos[0],ally.pos[1],ally.pos[2],advPos[0],advPos[1],advPos[2]))
        return observations

    def getRewards(self):
        rewards = []
        for ally in self.allies:
            rewards.append(randint(-10, 10))
        return rewards

    def getIsDone(self):
        if self.step >= self.maxIterations:
            return True
        self.adv.calcStatus()
        advPos = self.adv.pos
        for ally in self.allies:
            ally.calcStatus()
            if self.isEqual(ally.pos,advPos):
                return True
        return False

    def isEqual(self, a, b):
        if a[0] == b[0] and a[1] == b[1] and a[2] == b[2]:
            return True
        return False


    def step(self, actions):
        self.runAllies(actions)
        self.runAdv()
        self.step +=1
        return (self.getObservations(), self.getRewards(), self.getIsDone())

    def runAllies(self, actions):
        i = 0
        for ally in self.allies:
            ally.calcWaypoints(self.decodeAction(actions[i]))
            ally.runMove()
            i += 1

    def runAdv(self):
        self.adv.calcWaypoints()
        self.adv.runMove()

    def decodeAction(self, action):
        if action == 0:
            return [0,0,0]
        if action == 1:
            return [0,1,0]
        if action == 2:
            return [1,1,0]
        if action == 3:
            return [1,0,0]
        if action == 4:
            return [1,-1,0]
        if action == 5:
            return [0,-1,0]
        if action == 6:
            return [-1,-1,0]
        if action == 7:
            return [-1,0,0]
        if action == 8:
            return [-1,1,0]
        if action == 9:
            return [0,0,1]
        if action == 10:
            return [0,1,1]
        if action == 11:
            return [1,1,1]
        if action == 12:
            return [1,0,1]
        if action == 13:
            return [1,-1,1]
        if action == 14:
            return [0,-1,1]
        if action == 15:
            return [-1,-1,1]
        if action == 16:
            return [-1,0,1]
        if action == 17:
            return [-1,1,1]
        if action == 18:
            return [0,0,-1]
        if action == 19:
            return [0,1,-1]
        if action == 20:
            return [1,1,-1]
        if action == 21:
            return [1,0,-1]
        if action == 22:
            return [1,-1,-1]
        if action == 23:
            return [0,-1,-1]
        if action == 24:
            return [-1,-1,-1]
        if action == 25:
            return [-1,0,-1]
        if action == 26:
            return [-1,1,-1]

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
hiddenValueLengths = 3
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
    env = EmptyWorld()

    action_dim = (numOfAgents, numOfActions)

    actor = ActorNetwork(sess, action_dim, learningRate, tau)

    critic = CriticNetwork(sess, learningRate, tau, gamma, actor.get_num_trainable_vars())

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
