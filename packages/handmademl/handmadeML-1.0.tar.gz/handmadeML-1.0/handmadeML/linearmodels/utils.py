'''This module contains all functions needed for
the neural network model'''

#import pandas as pd
import numpy as np
#from progressbar.bar import ProgressBar

## Functions

def compute_hinge(x, y, w, b, loss_type='hinge', derivative=False):
    '''compute the hinge or squared_hinge loss
    returns scalar
    inputs :
        x: shape (n_sample, n_features)
        y: 1/0 binary classes, array or list'''

    #converting DataFrames, lists or lists of lists to nparray
    y = np.array(y) #converting 0/1 class into -1/1
    x = np.array(x)

    losses_using_minus_plus1=['hinge','squared_hinge']
    if loss_type in losses_using_minus_plus1:
        y = (y-0.5)*2

    if loss_type=='hinge':
        if not derivative:
            return np.maximum(0, 1-(np.dot(x,w)+b)*y).mean()

        hinge_values=np.expand_dims(1-y*(np.dot(x,w)+b),axis=1)
        positives=(hinge_values>0)
        dloss_dw=-(positives*(np.expand_dims(y,axis=1)*x)).mean(axis=0)
        dloss_db=-(positives*np.expand_dims(y,axis=1)).mean(axis=0)
        return np.concatenate((dloss_dw, dloss_db),axis=0)

    if loss_type=='squared_hinge':
        if not derivative:
            return np.square(np.maximum(0, 1-(np.dot(x,w)+b)*y)).mean()

        hinge_values=np.expand_dims(1-y*(np.dot(x,w)+b),axis=1)
        positives=(hinge_values>0)
        dloss_dw=-2*(positives*(np.expand_dims(y,axis=1)*hinge_values*x)).mean(axis=0)
        dloss_db=-2*(positives*np.expand_dims(y,axis=1)*hinge_values).mean(axis=0)
        return np.concatenate((dloss_dw, dloss_db),axis=0)

    raise ValueError(f'unknown loss_type {loss_type}')



def compute_penalty(w,penalty_type='l2', derivative=False):
    w=np.array(w)
    if penalty_type=='l2':
        if not derivative:
            return 0.5 * np.dot(w.T,w)
        return w

    if penalty_type=='l1':
        if not derivative:
            return np.absolute(w).sum()
        return np.divide(w, np.absolute(w))

    if penalty_type==None:
        if not derivative:
            return 0
        return np.zeros_like(w)

    raise ValueError(f'unknown penalty_type {penalty_type}')



def compute_cost(x, y, params, C, loss_type='hinge',
                 penalty_type='l2', derivative=False):
    '''y must be 0/1 binary classes'''
    y = np.array(y)
    x = np.array(x)
    params=np.array(params)
    w = params[:-1]
    b = params[-1]

    #raise errors for unconsistant inputs
    if len(y.shape) > 2:
        raise ValueError('y vect  or dimension too high. Must be 2 max')

    if y.shape[0] != x.shape[0]:
        raise ValueError(f'unconsistent vectors dimensions during loss_derivative: \
y.shape= {y.shape} and x.shape= {x.shape}')

    if x.shape[1] != w.size:
        raise ValueError(f'unconsistent vectors dimensions during loss_derivative: \
x.shape= {x.shape} and w.size= {w.size}')


    if derivative==False:
        return C * compute_hinge(x, y, w, b, loss_type, derivative=False)\
               + compute_penalty(w, penalty_type, derivative=False)
    return C * compute_hinge(x, y, w, b, loss_type, derivative=True)\
           + np.concatenate((compute_penalty(w, penalty_type, derivative=True),
                                  np.zeros((1,))),
                                 axis=0)


#---------------------------------------------------------------------------
## functions for results plot
#---------------------------------------------------------------------------


def compute_line_points(a,b,c):
    '''computes 2 points far away from origin on the line defined by equation
    a*x + b*y +c = 0
    returns : [x1,x2], [y1,y2]'''
    delta=4 * a**2 * b**2 -4 * (a**2 + b**2) * (c**2 - 10000 * b**2)
    xroot1= (-2*a*c +np.sqrt(delta)) / 2 /(a**2 + b**2)
    xroot2= (-2*a*c -np.sqrt(delta)) / 2 /(a**2 + b**2)
    yroot1=(-c-a*xroot1)/b
    yroot2=(-c-a*xroot2)/b
    return [xroot1,xroot2], [yroot1,yroot2]
