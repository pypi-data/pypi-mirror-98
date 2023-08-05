import unittest

import sys
sys.path.append('../')

from handmadeML.neuralnets.utils import *


#---------------------------------------------------------------------------
## tests for function compute_activation
#---------------------------------------------------------------------------
class Test_compute_activation(unittest.TestCase):

  def test_activation_relu(self):
    expected = np.array([[0,0], [0, 1], [1, 3]])
    actual = compute_activation(np.array([[-1,0], [0, 1], [1, 3]]), 'relu')
    self.assertTrue((actual == expected).all(),\
            msg="uncorrect relu function behaviour")

#---------------------------------------------------------------------------
  def test_activation_linear(self):
    expected = np.array([[-1,0], [0, 1], [1, 3]])
    actual = compute_activation(np.array([[-1,0], [0, 1], [1, 3]]), 'linear')

    self.assertTrue((actual == expected).all(),\
            msg="uncorrect linear function behaviour")

#---------------------------------------------------------------------------
  def test_activation_sigmoid(self):
    expected = np.array([[0.26894142, 0.5       ],
                         [0.5       , 0.73105858],
                         [0.73105858, 0.95257413]])
    actual = compute_activation(np.array([[-1,0], [0, 1], [1, 3]]),
                                        'sigmoid')
    self.assertTrue((np.round(actual,decimals=8) == expected).all(),\
            msg="uncorrect sigmoid function behaviour")

#---------------------------------------------------------------------------
  def test_activation_tanh(self):
    expected = np.array([[-0.76159416,  0.        ],
                         [ 0.        ,  0.76159416],
                         [ 0.76159416,  0.99505475]])
    actual = compute_activation(np.array([[-1,0], [0, 1], [1, 3]]),
                                        'tanh')
    self.assertTrue((np.round(actual,decimals=8) == expected).all(),\
            msg="uncorrect tanh function behaviour")

#---------------------------------------------------------------------------
  def test_activation_softmax(self):
    expected = np.array([[0.09003057, 0.04201007],
                         [0.24472847, 0.1141952 ],
                         [0.66524096, 0.84379473]])
    actual = compute_activation(np.array([[-1,0], [0, 1], [1, 3]]),
                                        'softmax')
    self.assertTrue((np.round(actual,decimals=8) == expected).all(),\
            msg="uncorrect softmax function behaviour")

#---------------------------------------------------------------------------
  def test_unknown_activation_type_error(self):
    test=unittest.TestCase()
    with test.assertRaises(ValueError) as context:
        compute_activation(0,'typo_error')
    self.assertTrue ('Unknown activation type' in str(context.exception),\
        "no or wrong Exception raised when inputing an unknown activation_type\
         while calling compute_activation")


#---------------------------------------------------------------------------
## tests for function compute_activation_derivative
#---------------------------------------------------------------------------
class Test_compute_activation_derivative(unittest.TestCase):

  def test_activation_derivative_relu(self):
    expected = np.array([[0,0], [0, 1], [1, 1]])
    actual = compute_activation_derivative(np.array([[-1,0], [0, 1], [1, 3]]),
                                          'relu')
    self.assertTrue((actual == expected).all(),\
                    msg="uncorrect relu function derivative behaviour")

#---------------------------------------------------------------------------
  def test_activation_derivative_linear(self):
    expected = np.array([[1,1], [1, 1], [1, 1]])
    actual = compute_activation_derivative(np.array([[-1,0], [0, 1], [1, 3]]),
                                          'linear')
    self.assertTrue((actual == expected).all(),\
                    msg="uncorrect linear function derivative behaviour")

#---------------------------------------------------------------------------
  def test_activation_derivative_sigmoid(self):
    expected = np.array([[0.19661193, 0.25      ],
                         [0.25      , 0.19661193],
                         [0.19661193, 0.04517666]])
    actual = compute_activation_derivative\
                     (np.array([[0.26894142, 0.5       ],
                                [0.5       , 0.73105858],
                                [0.73105858, 0.95257413]]),
                      'sigmoid')
    self.assertTrue((np.round(actual,decimals=8) == expected).all(),\
            msg="uncorrect sigmoid function derivative behaviour")

#---------------------------------------------------------------------------
  def test_activation_derivative_tanh(self):
    expected = np.array([[0.41997434, 1.        ],
                         [1.        , 0.41997434],
                         [0.41997434, 0.00986604]])
    actual = compute_activation_derivative\
                     (np.array([[-0.76159416,  0.        ],
                                [ 0.        ,  0.76159416],
                                [ 0.76159416,  0.99505475]]),
                      'tanh')
    self.assertTrue((np.round(actual,decimals=8) == expected).all(),\
            msg="uncorrect tanh function derivative behaviour")

#---------------------------------------------------------------------------
  def test_activation_derivative_softmax(self):
    expected = np.array([[0.08192507, 0.04024522],
                         [0.18483645, 0.10115466],
                         [0.22269543, 0.13180518]])
    actual = compute_activation_derivative\
                     (np.array([[0.09003057, 0.04201007],
                                [0.24472847, 0.1141952 ],
                                [0.66524096, 0.84379473]]),
                      'softmax')
    self.assertTrue((np.round(actual,decimals=8) == expected).all(),\
            msg="uncorrect softmax function derivative behaviour")

#---------------------------------------------------------------------------
  def test_unknown_activation_exception(self):
    test=unittest.TestCase()
    with test.assertRaises(ValueError) as context:
        compute_activation_derivative(0,'typo_error')
    self.assertTrue ('Unknown activation type' in str(context.exception),\
        "no or wrong Exception raised when inputing an unknown activation_type\
         while calling compute_activation_derivative")

