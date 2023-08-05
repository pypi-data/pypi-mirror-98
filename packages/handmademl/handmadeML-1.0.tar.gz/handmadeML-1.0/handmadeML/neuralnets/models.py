'''This module contains the neural network
model class itself'''

import numpy as np
import seaborn as sns

from .utils import compute_activation,compute_activation_derivative
from ..common.utils import compute_metric


from ..optimizers.adam import AdamOptimizer


class HandmadeNN ():
    '''
    hand-made version of neural network
    so far, the possibilities are :

        - layers activation functions :
            'linear', 'relu', 'sigmoid', 'tanh', 'softmax'

        - weights initializers : 'ones', 'glorot_uniform'
        - bias initializers : 'zeros', 'ones'

        - loss functions :
            'mse', 'mae', 'binary_crossentropy', 'categorical_crossentropy'

        - solver :
            SGD without momentum
    '''
    def __init__ (self, input_dim=0):
        self.weights=[]
        self.bias=[]
        self.activation_types=[]
        self.input_dim=input_dim
        self.n_layers=0

        self.loss_history=[]

    def set_input_dim (self, input_dim):
        '''manually sets the input_dim attribute of the model instance'''
        self.input_dim = input_dim

    def set_loss (self, loss):
        '''manually sets the loss attribute of the model instance'''
        self.loss = loss

    def add_dense_layer (self, n_neurons, activation_type,
                         weights_initializer='glorot_uniform', bias_initializer='zeros'):
        '''add a dense (fully connected) layer of neurons to the model
        This initializes the weights and bias according to selected initializer type,
        wich are yet implemented directly here'''
        #check if the input_dim is set
        if self.input_dim == 0:
            raise ValueError('input_dim = 0 .\
Use set_input_dim before creating first layer')

        #get the size of the input os this layer
        if len(self.bias) == 0:
            previous_dim=self.input_dim
        else:
            previous_dim=(self.bias[-1].shape[0])

        #initialize the layer parameters
        if weights_initializer == 'ones':
            self.weights.append(np.ones((n_neurons, previous_dim)))
        elif weights_initializer == 'glorot_uniform':
            limit = np.square(6 / (n_neurons + previous_dim))
            self.weights.append(np.random.uniform(-limit, limit, size = (n_neurons, previous_dim)))
        else:
            raise ValueError(f'Unknown weights initializer {weights_initializer}.\
Supported types : ones, glorot_uniform')

        if bias_initializer == 'zeros':
            self.bias.append(np.zeros(n_neurons))
        elif bias_initializer == 'ones':
            self.bias.append(np.ones(n_neurons))
        else:
            raise ValueError(f'Unknown bias initializer {bias_initializer}.\
Supported types : zeros, ones')

        self.activation_types.append(activation_type)
        self.n_layers += 1

        #test the activation type
        compute_activation(0, activation_type)

    def predict (self, X, keep_hidden_layers=False):
        '''input X : list, list of lists, np array, pd DataFrame
               axis 0 = samples
               axis 1 = features

           ## IF keep_hidden_layers==False:
           output = y_pred: 2D np-array
               axis 0 = samples
               axis 1 = output features, depending of the size of last layer

           ## IF keep_hidden_layers==True:
           outputs = layers_outputs, layers_activation_derivatives
           -output1 = layers_outputs:
               list of 2D np-arrays of outputs of each layer
               len(list)=n_layers+1: 1st element = X itself
                                     last element = y_pred
               axis 0 = samples
               axis 1 = number of neurons of the layer
           -output2 = layers_activation_derivatives:
               list of 2D np-arrays of d_act/d_input of each layer
               len(list)=n_layers
               axis 0 = samples
               axis 1 = number of neurons of the layer
           '''
        #converting DataFrames, lists or lists of lists to nparray
        X = np.array(X)

        #deal with 1D inputs to forge a 1 * n_features 2D-array
        if len(X.shape) == 1:
            X = np.expand_dims(X, axis = 0)

        #raise errors for unconsistant inputs
        if len(X.shape) > 2:
            raise ValueError('X vector dimension too high. Must be 2 max')
        if X.shape[1] != self.input_dim:
            raise ValueError(f'Unconsistent number of features. \
The network input_dim is {self.input_dim}')

        #compute the prediction
        layers_outputs = [X]
        layers_activation_derivatives = []
        for layer_index, activation_type in enumerate(self.activation_types):
            activation_input = np.dot(self.weights[layer_index], X.T)\
                               + np.expand_dims(self.bias[layer_index], axis=1)
            X = compute_activation(activation_input, activation_type).T

            layers_outputs.append(X)
            layers_activation_derivatives.append(\
                compute_activation_derivative(X, activation_type))

        if keep_hidden_layers:
            return layers_outputs, layers_activation_derivatives
        return X

    def score (self, X, y, metric):
        '''use predict method, then compute_metric function'''
        y_pred=self.predict(X)
        return compute_metric(y, y_pred, metric)

    def compute_backpropagation (self, X, y):
        '''This method :
            - executes self.predict(X) WITH keep_hidden_layers
                to keep all intermediate outputs
            - executes compute_metric (y, y_pred, loss) WITH loss_derivative
            - for each layer from last to first : computes loss
              derivatives (aka gradient) with respect to bias and weights

            output 1 : gradient with respect to weights
               (list of 2D arrays
               len(list) = n_layers
               axis 0 = number of neurons of the layer
               axis 1 = number of neurons of the previous layer (or features in the input)
            output 2 : gradient with respect to bias
               (list of 1D arrays)
               len(list) = n_layers
               axis 0 = number of neurons of the layer
            '''
        delta_weights=[]
        delta_bias=[]

        # compute the outputs and the derivatives of each layer
        layers_outputs, layers_activation_derivatives\
                = self.predict(X, keep_hidden_layers = True)
        # compute d_loss/d_ypred
        dloss_doutput = compute_metric (y,
                                        layers_outputs[-1],
                                        self.loss,
                                        loss_derivative = True)
        for layer_index in range(self.n_layers-1, -1, -1):
            # compute d_loss/d_input of the layer
            dloss_dinput = dloss_doutput * layers_activation_derivatives[layer_index]

            # compute gradient with respect to weights and bias
            delta_weights.append(np.dot(dloss_dinput.T, layers_outputs[layer_index]))
            delta_bias.append(np.sum(dloss_dinput, axis=0))

            # update dloss_doutput for next propagation
            if layer_index > 0:
                dloss_doutput = np.dot (dloss_dinput, self.weights[layer_index])

        delta_weights.reverse()
        delta_bias.reverse()

        return delta_weights, delta_bias



    def fit (self, X, y, loss=None, learning_rate=0.01,
             batch_size=1, n_epochs=10, verbose=1,
             optimizer_type='sgd',
             alpha_init=0.001, beta_1=0.9,
             beta_2=0.999, epsilon=1e-8):
        '''input X : 2D array or pd DataFrame
                axis 0 = samples
                axis 1 = features
        '''
        if loss:
            self.loss=loss

        if optimizer_type == 'adam':
            optimizer = AdamOptimizer ((self.weights, self.bias),
                                        alpha_init=alpha_init, beta_1=beta_1,
                                        beta_2=beta_2, epsilon=epsilon)
            #print(optimizer.v)

        X = np.array(X)
        y = np.array(y)
        n_samples = X.shape[0]
        n_minibatches_per_epoch = int(n_samples / batch_size)

        loss=self.score(X, y, self.loss)
        if self.loss_history == []:
            self.loss_history.append(loss)

        if verbose>0:
            print(f'initial loss: {self.score(X, y, self.loss)}')

        for epoch_index in range (n_epochs):
            if verbose>1:
                print(f'beginning epoch n°{epoch_index + 1}')

            #progress_batches = ProgressBar()
            #for mini_batch_index in progress_batches(range(n_minibatches_per_epoch)):
            for mini_batch_index in range(n_minibatches_per_epoch):
                gradient_weights, gradient_bias\
                    = self.compute_backpropagation(X[mini_batch_index * batch_size :\
                                                     (mini_batch_index +1) * batch_size],
                                                   y[mini_batch_index * batch_size :\
                                                     (mini_batch_index +1) * batch_size])

                if optimizer_type == 'sgd':
                    #compute the update directly
                    weights_update = [-learning_rate * grad for grad in gradient_weights]
                    bias_update = [-learning_rate * grad for grad in gradient_bias]

                elif optimizer_type == 'adam':
                    #compute the update with the optimizer
                    weights_update, bias_update = optimizer.get_update((gradient_weights,
                                                                       gradient_bias))

                else:
                    raise ValueError(f'unsupported optimizer type {optimizer_type}')

                # updating weights and bias
                self.weights = [w + w_update  for w, w_update in zip(self.weights, weights_update)]
                self.bias = [b + b_update for b, b_update in zip(self.bias, bias_update)]

            loss=self.score(X, y, self.loss)
            self.loss_history.append(loss)

            if verbose>1:
                print(f'end of epoch n°{epoch_index + 1}. loss: {self.score(X, y, self.loss)}')
        if verbose==1:
            print(f'final loss: {self.score(X, y, self.loss)}')

    def plot_loss_history(self):
        '''plots the complete loss history of the model since creation,
        including multiple .fit() calls'''
        graph=sns.lineplot(x=range(len(self.loss_history)),y=self.loss_history)
        graph.set(xlabel="epochs", ylabel = "loss")
