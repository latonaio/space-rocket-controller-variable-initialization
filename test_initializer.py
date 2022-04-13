import unittest
import initializer
import json
import numpy as np

class TestInitializer(unittest.TestCase):
  def setUp(self):
    self.input_vals = {}
    f = open('test.json')
    for k,v in json.load(f).items():
      self.input_vals[k] = float(v)
    self.initializer = initializer.main('test.json')
    f.close()
  def test_t_hb(self):
    vars = self.initializer.get_namespace('vars')
    self.assertEqual(type(vars), dict)
    self.assertAlmostEqual(vars['t_hb'][0][0], 
                          np.cos(self.input_vals['euler_angle_2'])
                          *np.cos(self.input_vals['euler_angle_3']))
    self.assertAlmostEqual(vars['t_hb'][0][1], 
                          np.cos(self.input_vals['euler_angle_2'])
                          *np.sin(self.input_vals['euler_angle_3']))
    self.assertAlmostEqual(vars['t_hb'][0][2], 
                          -np.sin(self.input_vals['euler_angle_2']))
    self.assertAlmostEqual(vars['t_hb'][1][0], 
                          np.sin(self.input_vals['euler_angle_1'])
                          *np.sin(self.input_vals['euler_angle_2'])
                          *np.cos(self.input_vals['euler_angle_3'])
                          -np.cos(self.input_vals['euler_angle_1'])
                          *np.sin(self.input_vals['euler_angle_3']))
    self.assertAlmostEqual(vars['t_hb'][1][1], 
                          np.sin(self.input_vals['euler_angle_1'])
                          *np.sin(self.input_vals['euler_angle_2'])
                          *np.sin(self.input_vals['euler_angle_3'])
                          +np.cos(self.input_vals['euler_angle_1'])
                          *np.cos(self.input_vals['euler_angle_3']))
    self.assertAlmostEqual(vars['t_hb'][1][2], 
                          np.sin(self.input_vals['euler_angle_1'])
                          *np.cos(self.input_vals['euler_angle_2']))
    self.assertAlmostEqual(vars['t_hb'][2][0], 
                          np.cos(self.input_vals['euler_angle_1'])
                          *np.sin(self.input_vals['euler_angle_2'])
                          *np.cos(self.input_vals['euler_angle_3'])
                          +np.sin(self.input_vals['euler_angle_1'])
                          *np.sin(self.input_vals['euler_angle_3']))
    self.assertAlmostEqual(vars['t_hb'][2][1], 
                          np.cos(self.input_vals['euler_angle_1'])
                          *np.sin(self.input_vals['euler_angle_2'])
                          *np.sin(self.input_vals['euler_angle_3'])
                          -np.sin(self.input_vals['euler_angle_1'])
                          *np.cos(self.input_vals['euler_angle_3']))
    self.assertAlmostEqual(vars['t_hb'][2][2], 
                          np.cos(self.input_vals['euler_angle_1'])
                          *np.cos(self.input_vals['euler_angle_2']))
if __name__== '__main__':
  unittest.main()