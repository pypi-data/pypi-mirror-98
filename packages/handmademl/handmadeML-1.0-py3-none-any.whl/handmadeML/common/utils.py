'''This module contains common utility functions'''

#import pandas as pd
import numpy as np
#from progressbar.bar import ProgressBar

## Functions

def compute_metric (y, y_pred, metric, loss_derivative=False):
    '''Defining loss and metric functions
     Takes nparrays, lists or a single values

     ## IF loss_derivative==False:
         output: always scalar

     ## IF loss_derivative==True: (True will be ignored for non-loss metrics)
         Computes the partial derivative of the loss function
           with respect to each component of each sample
         output: 2Darray
            n_samples * 1 for binary_crossentropy or single output regression
            n_samples * n_class for categorical_crossentropy
            n_samples * n_features for multifeatures regression)
    '''

    #converting DataFrames, lists or lists of lists to nparray
    y = np.array(y)
    y_pred = np.array(y_pred)

    #deal with 1D inputs to forge a n_samples * 1 2D-array
    if len(y.shape) == 1:
        y = np.expand_dims(y, axis = 1)
    if len(y_pred.shape) == 1:
        y_pred = np.expand_dims(y_pred, axis = 1)

    #raise errors for unconsistant inputs
    if len(y.shape) > 2:
        raise ValueError('y vector dimension too high. Must be 2 max')
    if len(y_pred.shape) > 2:
        raise ValueError('y_pred vector dimension too high. Must be 2 max')
    if y.shape != y_pred.shape:
        raise ValueError(f'unconsistent vectors dimensions during scoring :\
y.shape= {y.shape} and y_pred.shape= {y_pred.shape}')

    #compute loss funtions (or derivatives if loss_derivative==True)
    if metric == 'mse':
        if not loss_derivative:
            return np.square(y-y_pred).mean()
        return 1 / y.size * 2 * (y_pred - y)

    if metric == 'mae':
        if not loss_derivative:
            return np.abs(y-y_pred).mean()
        return 1 / y.size * (y_pred - y) / np.abs(y - y_pred)

    if metric == 'categorical_crossentropy':
        if not loss_derivative:
            return -1 / y.shape[0] * ((y * np.log(y_pred)).sum())
        return -1 / y.shape[0] * (y / y_pred)

    if metric == 'binary_crossentropy':
        if y.shape[1]>1:
            raise ValueError('y vector dimension too high.\
Must be 1 max for binary_crossentropy')
        if not loss_derivative:
            return -(y*np.log(y_pred)+(1-y)*np.log(1-y_pred)).mean()
        return -1 / y.size * (y / y_pred - (1-y) / (1-y_pred))

    # compute other metrics functions
    #### accuracy, f1-score, recall, etc.. : not implemented yet

    raise ValueError(f'Unknown metric {metric}. Supported types :\
mse, mae, categorical_crossentropy, binary_crossentropy')
