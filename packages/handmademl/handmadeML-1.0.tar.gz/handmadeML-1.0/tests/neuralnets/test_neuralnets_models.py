import unittest

import sys
sys.path.append('../')

from handmadeML.neuralnets.models import *

#---------------------------------------------------------------------------
## tests for method add_dense_layer
#---------------------------------------------------------------------------
class Test_add_dense_layer(unittest.TestCase):

  def test_no_input_dim_exception(self):

    my_nn=HandmadeNN()
    test=unittest.TestCase()
    with test.assertRaises(ValueError) as context:
        my_nn.add_dense_layer(5,'relu')
    self.assertTrue ('Use set_input_dim before creating first layer'\
           in str(context.exception),\
        "no or wrong Exception raised when adding first layer\
         to a network without setting input_dim")

#---------------------------------------------------------------------------
  def test_unknown_activation_exception(self):
    my_nn=HandmadeNN(5)
    test=unittest.TestCase()
    with test.assertRaises(ValueError) as context:
        my_nn.add_dense_layer(10,'typo_error')
    self.assertTrue ('Unknown activation type' in str(context.exception),\
        "no or wrong Exception raised when inputing\
         an unknown activation_type while adding layer")


#---------------------------------------------------------------------------
## tests for method predict - normal mode (without intermediate states) ####
#---------------------------------------------------------------------------
class Test_predict_without_intermediate(unittest.TestCase):

  def test_no_input_dim_exception(self):
    my_nn=HandmadeNN(5)# Empty neural network : just a pass-through for 5-values inputs

    self.assertTrue(my_nn.predict([2,3,2,3,4]).shape == (1,5),\
        "list not supported as an input for predict")
#---------------------------------------------------------------------------
  def test_list_as_input(self):
    my_nn=HandmadeNN(5)# Empty neural network : just a pass-through for 5-values inputs

    self.assertTrue(my_nn.predict([[2,3,2,3,4],[-2,-1,1,3,4]]).shape == (2,5),\
        "list of list not supported as an input for predict")

#---------------------------------------------------------------------------
  def test_x_dimension_too_high_exception(self):
    my_nn=HandmadeNN(5)# Empty neural network : just a pass-through for 5-values inputs

    test=unittest.TestCase()
    with test.assertRaises(ValueError) as context:
        my_nn.predict(np.array([[[1,1],[1,2],[1,3],[1,4],[1,5]],
                                    [[2,1],[2,2],[2,3],[3,4],[3,5]]]))
    self.assertTrue ('X vector dimension too high' in str(context.exception),\
        "no or wrong Exception raised when inputing a 3D-array in predict method")

#---------------------------------------------------------------------------
  def test_unconsistent_n_features_exception(self):
    my_nn=HandmadeNN(5)# Empty neural network : just a pass-through for 5-values inputs

    test=unittest.TestCase()
    with test.assertRaises(ValueError) as context:
        my_nn.predict(np.array([[1,1],[1,2],[1,3],[1,4],[1,5]]))
    self.assertTrue ('Unconsistent number of features' in str(context.exception),\
        "no or wrong Exception raised when inputing a X\
         with unconsistant size vs. network input_dim in predict method")

#---------------------------------------------------------------------------
  def test_oneD_array_as_input(self):
    my_nn=HandmadeNN(5)
    my_nn.add_dense_layer(10, 'linear')
    my_nn.weights[0] = np.vstack((np.identity(5),np.zeros((5,5))))
    self.assertTrue(my_nn.predict(np.array([-2,-1,2,3,4])).shape == (1,10),\
        "1-D array not supported as an input for predict method")

#---------------------------------------------------------------------------
  def test_output_dimension(self):
    my_nn=HandmadeNN(5)
    my_nn.add_dense_layer(10, 'linear')
    my_nn.weights[0] = np.vstack((np.identity(5),np.zeros((5,5))))
    self.assertTrue (my_nn.predict(np.array([[-2,-1,2,3,4],
                                         [-12,-11,12,13,14]])).shape == (2,10),\
        "the shape of the prediction for a 2*5 X input\
         by a network having 10neurons on last layer should be 2*10")

#--General-test-of-predict-method-with-all-activation-types-----------------
  def test_general_predict_test_all_activations(self):

    my_nn=HandmadeNN(5)

    my_nn.add_dense_layer(10, 'relu')
    my_nn.weights[-1] = np.concatenate([np.identity(5), np.zeros((5,5))], axis=0)
    my_nn.bias[-1] = np.array([0,0,0,0,1,1,1,0,0,0])

    my_nn.add_dense_layer(10, 'linear')
    my_nn.weights[-1] = np.flip(np.identity(10), 1)
    my_nn.bias[-1] = np.array([1,1,1,1,1,1,0,0,0,0])

    my_nn.add_dense_layer(10, 'tanh')
    my_nn.weights[-1] = np.identity(10)
    my_nn.bias[-1] = np.array([0,0,0,0,1,1,1,1,0,0])

    my_nn.add_dense_layer(10, 'softmax')
    my_nn.weights[-1] = np.flip(np.identity(10), 1)
    my_nn.bias[-1] = np.array([0,0,0,0,0,0,1,1,1,1])

    my_nn.add_dense_layer(1, 'sigmoid')
    my_nn.weights[-1] = np.expand_dims(np.arange(1,11,1), axis=0)
    my_nn.bias[-1] = np.array([0.5])


    self.assertTrue (np.round(my_nn.predict([-2,-1,2,3,4])[0,0], decimals=8) == 0.99939824,\
        "the general test of predict method on a network involving\
         all activation types and manually set bias and weights\
         did not return the correct value")


#---------------------------------------------------------------------------
## tests for method predict - backprop mode (with intermediate states) #####
#---------------------------------------------------------------------------
class Test_predict_backprop_mode(unittest.TestCase):

  def test_output_type_is_tuple(self):

    my_nn = HandmadeNN(5)# Empty neural network : just a pass-through for 5-values inputs
    my_nn.add_dense_layer(3, 'linear', weights_initializer='ones')

    outputs = my_nn.predict([2,3,2,3,4], keep_hidden_layers=True)
    n_outputs = len(np.array(outputs))
    output_type = type(outputs)
    self.assertTrue (output_type == tuple,\
        f"predict method with keep_hidden_layers must return a tuple. type is {output_type}")

#---------------------------------------------------------------------------
  def test_number_of_outputs(self):
    my_nn = HandmadeNN(5)# Empty neural network : just a pass-through for 5-values inputs
    my_nn.add_dense_layer(3, 'linear', weights_initializer='ones')

    outputs = my_nn.predict([2,3,2,3,4], keep_hidden_layers=True)
    n_outputs = len(np.array(outputs))
    output_type = type(outputs)

    self.assertTrue (n_outputs == 2,\
        f"predict method with keep_hidden_layers must return 2 output. here returns {n_outputs}")

#---------------------------------------------------------------------------
  def test_length_layers_outputs(self):
    my_nn = HandmadeNN(5)# Empty neural network : just a pass-through for 5-values inputs
    my_nn.add_dense_layer(3, 'linear', weights_initializer='ones')

    outputs = my_nn.predict([2,3,2,3,4], keep_hidden_layers=True)
    n_outputs = len(np.array(outputs))
    output_type = type(outputs)
    layers_outputs, layers_derivatives = outputs

    self.assertTrue (len(layers_outputs) == 2,\
        "the list of outputs of layers has not correct length using predict with keep_hidden_layers")

#---------------------------------------------------------------------------
  def test_length_layers_derivatives(self):
    my_nn = HandmadeNN(5)# Empty neural network : just a pass-through for 5-values inputs
    my_nn.add_dense_layer(3, 'linear', weights_initializer='ones')

    outputs = my_nn.predict([2,3,2,3,4], keep_hidden_layers=True)
    n_outputs = len(np.array(outputs))
    output_type = type(outputs)
    layers_outputs, layers_derivatives = outputs

    self.assertTrue (len(layers_derivatives) == 1,\
        "the list of derivatives of layers has not correct length using predict with keep_hidden_layers")

#---------------------------------------------------------------------------
  def test_layers_outputs_values(self):
    my_nn = HandmadeNN(5)# Empty neural network : just a pass-through for 5-values inputs
    my_nn.add_dense_layer(3, 'linear', weights_initializer='ones')

    outputs = my_nn.predict([2,3,2,3,4], keep_hidden_layers=True)
    n_outputs = len(np.array(outputs))
    output_type = type(outputs)
    layers_outputs, layers_derivatives = outputs

    self.assertTrue ((layers_outputs[1] == np.array([[14., 14., 14.]])).all(),\
        "uncorrect layers_outputs of predict method with keep_hidden_layers")

#---------------------------------------------------------------------------
  def test_layers_derivatives_values(self):
    my_nn = HandmadeNN(5)# Empty neural network : just a pass-through for 5-values inputs
    my_nn.add_dense_layer(3, 'linear', weights_initializer='ones')

    outputs = my_nn.predict([2,3,2,3,4], keep_hidden_layers=True)
    n_outputs = len(np.array(outputs))
    output_type = type(outputs)
    layers_outputs, layers_derivatives = outputs

    self.assertTrue ((layers_derivatives[0] == np.array([[1., 1., 1.]])).all(),\
        "uncorrect layers_derivatives of predict method with keep_hidden_layers")


#---------------------------------------------------------------------------
### tests for backpropagation method (computing the gradient) ##############
#---------------------------------------------------------------------------
class Test_backpropagation(unittest.TestCase):

  def test_output_type_is_tuple(self):

    my_nn=HandmadeNN(input_dim = 2)
    my_nn.add_dense_layer(2, 'linear', weights_initializer='ones')
    my_nn.add_dense_layer(1, 'linear', weights_initializer='ones')
    my_nn.set_loss('mse')

    outputs = my_nn.compute_backpropagation(np.array([[1,2],[2,3],[3,4]]), np.array([4,5,6]))
    n_outputs = len(np.array(outputs))
    output_type = type(outputs)
    self.assertTrue (output_type == tuple,\
        f"backpropagation method must return a tuple. type is {output_type}")

#---------------------------------------------------------------------------
  def test_number_of_outputs(self):
    my_nn=HandmadeNN(input_dim = 2)
    my_nn.add_dense_layer(2, 'linear', weights_initializer='ones')
    my_nn.add_dense_layer(1, 'linear', weights_initializer='ones')
    my_nn.set_loss('mse')

    outputs = my_nn.compute_backpropagation(np.array([[1,2],[2,3],[3,4]]), np.array([4,5,6]))
    n_outputs = len(np.array(outputs))
    output_type = type(outputs)

    self.assertTrue (n_outputs == 2,\
        f"backpropagation method must return 2 output. here returns {n_outputs}")

#---------------------------------------------------------------------------
  def test_weights_gradient_length(self):
    my_nn=HandmadeNN(input_dim = 2)
    my_nn.add_dense_layer(2, 'linear', weights_initializer='ones')
    my_nn.add_dense_layer(1, 'linear', weights_initializer='ones')
    my_nn.set_loss('mse')

    outputs = my_nn.compute_backpropagation(np.array([[1,2],[2,3],[3,4]]), np.array([4,5,6]))
    n_outputs = len(np.array(outputs))
    output_type = type(outputs)

    gradient_weights, gradient_bias = outputs

    self.assertTrue (len(gradient_weights) == 2,\
        "using backpropagation: the list of weights has not correct length")

#---------------------------------------------------------------------------
  def test_bias_gradient_length(self):
    my_nn=HandmadeNN(input_dim = 2)
    my_nn.add_dense_layer(2, 'linear', weights_initializer='ones')
    my_nn.add_dense_layer(1, 'linear', weights_initializer='ones')
    my_nn.set_loss('mse')

    outputs = my_nn.compute_backpropagation(np.array([[1,2],[2,3],[3,4]]), np.array([4,5,6]))
    n_outputs = len(np.array(outputs))
    output_type = type(outputs)

    gradient_weights, gradient_bias = outputs

    self.assertTrue (len(gradient_bias) == 2,\
        "using backpropagation: the list of bias has not correct length")

#---------------------------------------------------------------------------
  def test_weights_gradient_values(self):
    my_nn=HandmadeNN(input_dim = 2)
    my_nn.add_dense_layer(2, 'linear', weights_initializer='ones')
    my_nn.add_dense_layer(1, 'linear', weights_initializer='ones')
    my_nn.set_loss('mse')

    outputs = my_nn.compute_backpropagation(np.array([[1,2],[2,3],[3,4]]), np.array([4,5,6]))
    n_outputs = len(np.array(outputs))
    output_type = type(outputs)

    gradient_weights, gradient_bias = outputs

    self.assertTrue ((gradient_weights[0] == np.array([[24., 34.],
                                             [24., 34.]])).all(),\
        "using backpropagation: uncorrect gradient with respect to weights")

#---------------------------------------------------------------------------
  def test_bias_gradient_values(self):
    my_nn=HandmadeNN(input_dim = 2)
    my_nn.add_dense_layer(2, 'linear', weights_initializer='ones')
    my_nn.add_dense_layer(1, 'linear', weights_initializer='ones')
    my_nn.set_loss('mse')

    outputs = my_nn.compute_backpropagation(np.array([[1,2],[2,3],[3,4]]), np.array([4,5,6]))
    n_outputs = len(np.array(outputs))
    output_type = type(outputs)

    gradient_weights, gradient_bias = outputs

    self.assertTrue ((gradient_bias[0] == np.array([10., 10.])).all(),\
        "using backpropagation: uncorrect gradient with respect to bias")


#---------------------------------------------------------------------------
### tests for fit method
#---------------------------------------------------------------------------
class Test_fit_method(unittest.TestCase):

  def test_convergence_on_trivial_regression(self):
    my_nn=HandmadeNN(input_dim = 2)
    my_nn.add_dense_layer(1, 'linear',)
    X= np.ones((10_000, 2))
    y= np.zeros((10_000,1))
    my_nn.fit(X,y, loss='mse',optimizer_type='sgd', batch_size=7, n_epochs=2)

    self.assertTrue (my_nn.score(X,y,'mse') < 0.5,\
        "fit method has not converged with build-in sgd optimizer on a trivial regression")

#---------------------------------------------------------------------------
### tests for adam optimizer
#---------------------------------------------------------------------------
class Test_fit_method_with_adam(unittest.TestCase):

  def test_convergence_on_trivial_regression(self):
    my_nn=HandmadeNN(input_dim = 2)
    my_nn.add_dense_layer(1, 'linear',)
    X= np.ones((10_000, 2))
    y= np.zeros((10_000,1))
    my_nn.fit(X,y, loss='mse',optimizer_type='adam', batch_size=7, n_epochs=2)

    self.assertTrue (my_nn.score(X,y,'mse') < 0.5,\
        f"not converged with adam optimizer on a trivial regression : loss={my_nn.score(X,y,'mse')}")

#---------------------------------------------------------------------------


print ('all tests successfully passed')
