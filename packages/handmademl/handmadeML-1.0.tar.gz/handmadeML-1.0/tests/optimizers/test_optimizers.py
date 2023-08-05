import unittest

import sys
sys.path.append('../')

from handmadeML.optimizers.adam import *


#---------------------------------------------------------------------------
## tests for function NAME
#---------------------------------------------------------------------------
class Test_name_of_group(unittest.TestCase):

  def test_name_of_test(self):
    expected = 'value'
    actual = 'function(arguments)'
    self.assertTrue((actual != expected),\
            msg="message")
