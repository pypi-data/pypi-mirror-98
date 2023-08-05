'''This module contains the linear models'''

import numpy as np
import pandas as pd
import seaborn as sns

from .utils import compute_cost,compute_line_points
from ..common.utils import compute_metric


from ..optimizers.adam import AdamOptimizer


class LinearClassifier ():
    '''
    hand-made classifier supporting both svm (without kernel trick)
    and logistic_regression depending of the loss.
    So far the options available are:

        - param initializers : 'uniform'

        - loss functions : 'hinge', 'squared_hinge', 'logistic'

        - solver : SGD without momentum 'sgd', 'adam'
    '''
    def __init__ (self, input_dim=0, param_initializer='random_uniform'):
        self.input_dim=input_dim
        if param_initializer=='random_uniform':
            self.params=np.random.uniform(size=(input_dim + 1,))
        else:
            raise ValueError('Unknown param initializer type')
        self.cost_history=[]

    def set_input_dim (self, input_dim):
        self.input_dim = input_dim
        self.params=np.random.uniform(size=(input_dim + 1,))

    def predict (self, X, mode='binary'):
        '''
        If mode=='binary':
            Computes binary prediction : wether the point
            is above or bellow the hyperplane of the svm
        If mode=='distance':
            Computes the distance from each data point to the svm hyperplane,
            normalized by the half margin (i.e. that distance=1 is for a point
            lying on the upper boundary of the margin, -1 is for lower boundary)
        If mode=='proba':
            Computes the prediction in the form of proba using sigmoid of the distance

        Input X : list, list of lists, np array, pd DataFrame
               axis 0 = samples
               axis 1 = features

        Output = y_pred: 1D np-array
               axis 0 = samples
               values : 0/1 if mode=='binary'
                        distances, normalized by the half margin if mode=='distance'
                        float if mode=='proba'
           '''
        #converting DataFrames, lists or lists of lists to nparray
        X = np.array(X)
        w = self.params[:-1]
        b = self.params[-1]

        #deal with 1D input to forge a 1 * n_features 2D-array
        if len(X.shape) == 1:
            X = np.expand_dims(X, axis = 0)

        #raise errors for unconsistant input
        if len(X.shape) > 2:
            raise ValueError('X vector dimension too high. Must be 2 max')
        if X.shape[1] != self.input_dim:
            raise ValueError(f'Unconsistent numbers of features. \
The network input_dim is {self.input_dim}')

        #compute the prediction
        distance = np.dot(X,w)+b
        if mode=='binary':
            return (distance>0)*1
        if mode=='distance':
            return distance
        if mode=='proba':
            return 1/(1+np.exp(-distance))

        raise ValueError(f'unknown prediction mode {mode}')


    def score (self, X, y, metric):
        '''uses predict method, then compute_metric function
        TODO : for some metrics, such as roc_auc, we will need predict_proba'''

        y_pred=self.predict(X)
        return compute_metric(y, y_pred, metric)


    def fit (self, X, y, loss_type='hinge', penalty_type='l2', C=1,
             learning_rate=0.01, batch_size=1, n_epochs=10, verbose=1,
             optimizer_type='sgd', alpha_init=0.001, beta_1=0.9,
             beta_2=0.999, epsilon=1e-8):
        '''input X : 2D array or pd DataFrame
                axis 0 = samples
                axis 1 = features
        '''

        if optimizer_type == 'adam':
            optimizer = AdamOptimizer (([self.params]),
                                        alpha_init=alpha_init, beta_1=beta_1,
                                        beta_2=beta_2, epsilon=epsilon)

        X = np.array(X)
        y = np.array(y)
        n_samples = X.shape[0]
        n_minibatches_per_epoch = int((n_samples-1) / batch_size) + 1

        cost = compute_cost(X, y, self.params, C, loss_type,
                            penalty_type, derivative=False)

        if self.cost_history == []:
            self.cost_history.append(cost)
        if verbose>0:
            print(f'initial cost: {cost}')
            print(f'initial margin: {2/np.sqrt(np.square(self.params[:-1]).sum())}')

        for epoch_index in range (n_epochs):
            if verbose>1:
                print(f'beginning epoch n°{epoch_index + 1}')

            #progress_batches = ProgressBar()
            #for mini_batch_index in progress_batches(range(n_minibatches_per_epoch)):
            for mini_batch_index in range(n_minibatches_per_epoch):
                gradient = compute_cost(X[mini_batch_index * batch_size :\
                                          (mini_batch_index +1) * batch_size],
                                        y[mini_batch_index * batch_size :\
                                          (mini_batch_index +1) * batch_size],
                                        self.params,
                                        C,
                                        loss_type,
                                        penalty_type,
                                        derivative=True)

                if optimizer_type == 'sgd':
                    #compute the update directly
                    params_update = -learning_rate * gradient

                elif optimizer_type == 'adam':
                    #compute the update with the optimizer
                    params_update = optimizer.get_update(gradient)

                else:
                    raise ValueError(f'unsupported optimizer type {optimizer}')

                # updating weights and bias
                self.params = self.params + params_update

            cost = compute_cost(X, y, self.params, C, loss_type,
                                penalty_type, derivative=False)
            self.cost_history.append(cost)
            if verbose>1:

                print(f'end of epoch n°{epoch_index + 1}. cost: {cost}')

        if verbose==1:
            print(f'final cost: {cost}')
            print(f'final margin: {2/np.sqrt(np.square(self.params[:-1]).sum())}')


    def plot_cost_history(self):
        '''Make a simple plot cost versus epochs'''
        graph=sns.lineplot(x=range(len(self.cost_history)),y=self.cost_history)
        graph.set(xlabel="epochs", ylabel = "cost")


    def plot_2D_svc(self,x,y):
        '''only in 2D : x.shape=(n_samples,2)
        y.shape=(n_samples,)'''
        params=self.params
        x=np.array(x)
        y=np.array(y)

        if x.shape[1]!=2:
            raise ValueError(f'x.shape={x.shape}. Expected (n_sample,2)')
        if params.size!=3:
            raise ValueError(f'input_dim={params.size-1}. Expected 2')

        df=pd.DataFrame({'x1':x[:,0],'x2':x[:,1],'y':y})

        xline, yline = compute_line_points(params[0],params[1],params[2])
        xlineup, ylineup = compute_line_points(params[0],params[1],params[2]-1)
        xlinedown, ylinedown = compute_line_points(params[0],params[1],params[2]+1)

        g=sns.scatterplot(data=df,x='x1',y='x2',hue='y')
        sns.lineplot(x=xlinedown, y=ylinedown)
        sns.lineplot(x=xlineup, y=ylineup)
        sns.lineplot(x=xline, y=yline)
        g.set(xlim=(df.x1.min()-2,df.x1.max()+2))
        g.set(ylim=(df.x2.min()-2,df.x2.max()+2))
