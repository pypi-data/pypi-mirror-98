import unittest

import sys
sys.path.append('../')

from handmadeML.common.utils import *


#---------------------------------------------------------------------------
### tests for function compute_metric - normal mode (not derivative)########
#---------------------------------------------------------------------------
class Test_compute_metric(unittest.TestCase):

  def test_y_dimension_too_high_exception(self):
    test=unittest.TestCase()
    with test.assertRaises(ValueError) as context:
        compute_metric(np.array([[[1,1],[1,2]],
                                 [[2,1],[2,2]]]),
                       np.array([[1,2],
                                 [3,4]]),
                       'mse')
    self.assertTrue ('y vector dimension too high' in str(context.exception),\
        "no or wrong Exception raised when inputing a 3D-array as y\
         in compute_metric function")

#---------------------------------------------------------------------------
  def test_y_pred_dimension_too_high_exception(self):
    test=unittest.TestCase()
    with test.assertRaises(ValueError) as context:
        compute_metric(np.array([[1,2],
                                 [3,4]]),
                       np.array([[[1,1],[1,2]],
                                 [[2,1],[2,2]]]),
                       'mse')
    self.assertTrue ('y_pred vector dimension too high' in str(context.exception),\
        "no or wrong Exception raised when inputing a 3D-array as y_pred\
         in compute_metric function")

#---------------------------------------------------------------------------
  def test_unconsistent_dimensions_exception(self):
    test=unittest.TestCase()
    with test.assertRaises(ValueError) as context:
        compute_metric(np.array([[1,2,3],
                                 [4,5,6]]),
                       np.array([[1,2],
                                 [3,4]]),
                       'mse')
    self.assertTrue ('unconsistent vectors dimensions' in str(context.exception),\
        "no or wrong Exception raised when inputing unconsistent\
         y vs y_pred vectors shapes in compute_metric function")

#---------------------------------------------------------------------------
  def test_mse(self):
    self.assertTrue (compute_metric([1,0],[0.5,1],'mse') == 0.625,\
        "uncorrect mse metric behaviour")

#---------------------------------------------------------------------------
  def test_mse_multi_features(self):
    self.assertTrue (compute_metric([[1,0],[0,0]],[[0.5,1],[1,1]],'mse') == 0.8125,\
        "uncorrect mse metric behaviour for multi-features regressions\
         (2D y and y_pred vectors)")

#---------------------------------------------------------------------------
  def test_mae(self):
    self.assertTrue (compute_metric([1,0],[0.5,1],'mae') == 0.75,\
        "uncorrect mae metric behaviour")

#---------------------------------------------------------------------------
  def test_categorical_crossentropy(self):
    self.assertTrue (np.round(compute_metric([[1,0,0],[0,1,0]],[[0.8,0.1,0.1],[0.2,0.6,0.2]],
                                   'categorical_crossentropy'),
                    decimals=8) == 0.36698459,\
        "uncorrect categorical_crossentropy metric behaviour")

#---------------------------------------------------------------------------
  def test_binary_crossentropy(self):
    self.assertTrue (np.round(compute_metric([1,0],[0.9,0.1],'binary_crossentropy'),
                    decimals=8) == 0.10536052,\
        "uncorrect binary_crossentropy metric behaviour")

#---------------------------------------------------------------------------
  def test_y_dimension_too_high_with_binary_crossentropy_exception(self):
    test=unittest.TestCase()
    with test.assertRaises(ValueError) as context:
        compute_metric([[1,0,1],[0,0,0]],
                       [[0.5,0.9,0.1],
                        [0.9,0.9,0.1]],
                       'binary_crossentropy')
    self.assertTrue ('1 max for binary_crossentropy' in str(context.exception),\
        "no or wrong Exception raised when inputing 2D y/y_pred vectors\
         with binary_crossentropy selected in compute_metric function")

#---------------------------------------------------------------------------
  def test_unknown_metric_exception(self):
    test=unittest.TestCase()
    with test.assertRaises(ValueError) as context:
        compute_metric([0],[0],'typo_error')
    self.assertTrue ('Unknown metric' in str(context.exception),\
        "no or wrong Exception raised when inputing\
         unknown metric in compute_metric function")


#---------------------------------------------------------------------------
### tests for function compute_metric - derivative mode ####################
#---------------------------------------------------------------------------
class Test_metric_derivative(unittest.TestCase):

  def test_output_format(self):
    self.assertTrue (len(compute_metric([1,0],[0.5,1],'mse', loss_derivative = True)\
               .shape) == 2,\
        "uncorrect output : compute_metric must return a 2D array in derivative mode")

#---------------------------------------------------------------------------
  def test_mse(self):
    self.assertTrue ((compute_metric([1,0],[0.5,1],'mse', loss_derivative = True)\
                == np.array([[-0.5],[1]])).all(),\
        "uncorrect mse metric behaviour in derivative mode")

#---------------------------------------------------------------------------
  def test_mse_multi_features(self):
    self.assertTrue ((compute_metric([[1,0],[0,0]],[[0.5,1],[1,1]],'mse',
                       loss_derivative = True)\
                == np.array([[-0.25, 0.5],[0.5, 0.5]])).all(),\
        "uncorrect mse metric behaviour for multi-features regressions\
         (2D y and y_pred vectors) in derivative mode")

#---------------------------------------------------------------------------
  def test_mae(self):
    self.assertTrue ((compute_metric([1,0],[0.5,1],'mae', loss_derivative = True)\
                == np.array([[-0.5],[0.5]])).all(),\
        "uncorrect mae metric behaviour in derivative mode")

#---------------------------------------------------------------------------
  def test_categorical_crossentropy(self):
    self.assertTrue ((np.round(compute_metric([[1,0,0],[0,1,0]],[[0.8,0.1,0.1],[0.2,0.6,0.2]],
                                   'categorical_crossentropy',
                                   loss_derivative = True),
                    decimals=8) == np.array([[-0.625, -0.        , -0.],
                                             [-0.   , -0.83333333, -0.]])).all(),\
        "uncorrect categorical_crossentropy metric behaviour in derivative mode")

#---------------------------------------------------------------------------
  def test_binary_crossentropy(self):
    self.assertTrue ((np.round(compute_metric([1,0],[0.9,0.1],
                                   'binary_crossentropy',
                                   loss_derivative = True),
                    decimals=8) == np.array([[-0.55555556],
                                             [ 0.55555556]])).all(),\
        "uncorrect binary_crossentropy metric behaviour in derivative mode")

