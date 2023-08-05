import unittest

import sys
sys.path.append('../')

from handmadeML.linearmodels.models import *


#---------------------------------------------------------------------------
## ttests for method predict
#---------------------------------------------------------------------------
class Test_predict(unittest.TestCase):

  def test_list_as_input(self):
    my_svc=LinearClassifier(5)
    self.assertTrue(my_svc.predict([2,3,2,3,4]).shape == (1,),\
            msg="lists should be supported as an input for predict")

#---------------------------------------------------------------------------
  def test_list_of_lists_as_input(self):
    my_svc=LinearClassifier(5)
    self.assertTrue(my_svc.predict([[2,3,2,3,4],[-2,-1,1,3,4]]).shape == (2,),\
            msg="lists of lists should be supported as an input for predict")

#---------------------------------------------------------------------------
  def test_x_dim_too_high_exception(self):
    my_svc=LinearClassifier(5)
    test=unittest.TestCase()
    with test.assertRaises(ValueError) as context:
        my_svc.predict(np.array([[[1,1],[1,2],[1,3],[1,4],[1,5]],
                                    [[2,1],[2,2],[2,3],[3,4],[3,5]]]))
    self.assertTrue('X vector dimension too high' in str(context.exception),\
        "no or wrong Exception raised when inputing a 3D-array in predict method")

#---------------------------------------------------------------------------
  def test_unconsistent_features_exception(self):
    my_svc=LinearClassifier(5)
    test=unittest.TestCase()
    with test.assertRaises(ValueError) as context:
        my_svc.predict(np.array([[1,1],[1,2],[1,3],[1,4],[1,5]]))
    self.assertTrue('Unconsistent numbers of features' in str(context.exception),\
        "no or wrong Exception raised when inputing a X\
with unconsistant size vs. model input_dim in predict method")

#---------------------------------------------------------------------------
  def test_1D_array_as_input(self):
    my_svc=LinearClassifier(5)
    self.assertTrue(my_svc.predict(np.array([-2,-1,2,3,4])).shape == (1,),\
        "1-D array should be supported as an input for predict method")

#--General-test-of-predict-method-------------------------------------------
  def test_predict_general_test(self):
    my_svc=LinearClassifier(2)
    my_svc.params=np.array([1,-1,0])
    self.assertTrue((my_svc.predict([[1,2],[2,1]]) == np.array([0,1])).all(),\
        "the general test of predict method on svc with\
manually set params did not return the correct value")
