
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
