'''This module contains all functions needed for
the neural network model'''

#import pandas as pd
import numpy as np
#from progressbar.bar import ProgressBar

## Functions

def compute_activation (X, activation_type):
    '''Defining activation functions
     Takes a nparray or a single value
    # Returns in the same format

    For softmax : assuming that X.shape[0]== n_neurons,
        the axis0 of array X is used for computing the mean
    '''
    X=np.array(X)
    if activation_type == 'relu':
        return np.maximum(X,0)
    if activation_type == 'sigmoid':
        return 1/(1+np.exp(-X))
    if activation_type == 'tanh':
        return np.tanh(X)
    if activation_type == 'linear':
        return X
    if activation_type == 'softmax':
        exp_x = np.exp(X)
        return exp_x / exp_x.sum(axis=0)

    #raise error if unknown type
    raise ValueError(f'Unknown activation type {activation_type}.\
Supported types : linear, relu, sigmoid, tanh, softmax')


def compute_activation_derivative (layer_output, activation_type):
    '''Computes the derivative of the activation functions,
       depending of the outputs of the output of these functions
           nota : if occures that for each of the 5 basic activations,
           f'(X) can be expressed simply as a function of f(X)

           Takes a nparray or a single value
        # Returns in the same format
           '''
    X_output=np.array(layer_output)
    if activation_type == 'relu':
        return (X_output > 0).astype(int)
    if activation_type == 'linear':
        return np.ones(X_output.shape)
    if activation_type == 'sigmoid':
        return X_output - np.square(X_output)
    if activation_type == 'tanh':
        return 1 - np.square(X_output)
    if activation_type == 'softmax':
        return X_output - np.square(X_output)

    #raise error if unknown type
    raise ValueError(f'Unknown activation type {activation_type}.\
Supported types : linear, relu, sigmoid, tanh, softmax')
