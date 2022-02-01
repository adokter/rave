'''
Copyright (C) 2014 Swedish Meteorological and Hydrological Institute, SMHI,

This file is part of RAVE.

RAVE is free software: you can redistribute it and/or modify
it under the terms of the GNU Lesser General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

RAVE is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public License
along with RAVE.  If not, see <http://www.gnu.org/licenses/>.
------------------------------------------------------------------------*/

Tests the py gra module.

@file
@author Anders Henja (Swedish Meteorological and Hydrological Institute, SMHI)
@date 2014-03-28
'''
import unittest
import os
import _gra
import _ravefield, _rave, _cartesianparam
import string
import numpy
import math

class PyGraTest(unittest.TestCase):
  def setUp(self):
    pass

  def tearDown(self):
    pass
  
  def test_new(self):
    obj = _gra.new()
    self.assertNotEqual(-1, str(type(obj)).find("GraCore"))

  def test_attribute_visibility(self):
    attrs = ['A', 'B', 'C', 'upperThreshold', 'lowerThreshold', 'zrA', 'zrb']
    gra = _gra.new()
    alist = dir(gra)
    for a in attrs:
      self.assertEqual(True, a in alist)

  def test_A(self):
    gra = _gra.new();
    self.assertAlmostEqual(0.0, gra.A, 4)
    gra.A = 10
    self.assertAlmostEqual(10.0, gra.A, 4)
    gra.A = 11.1
    self.assertAlmostEqual(11.1, gra.A, 4)
 
  def test_B(self):
    gra = _gra.new();
    self.assertAlmostEqual(0.0, gra.B, 4)
    gra.B = 10
    self.assertAlmostEqual(10.0, gra.B, 4)
    gra.B = 11.1
    self.assertAlmostEqual(11.1, gra.B, 4)
     
  def test_C(self):
    gra = _gra.new();
    self.assertAlmostEqual(0.0, gra.C, 4)
    gra.C = 10
    self.assertAlmostEqual(10.0, gra.C, 4)
    gra.C = 11.1
    self.assertAlmostEqual(11.1, gra.C, 4)
 
  def test_upperThreshold(self):
    gra = _gra.new();
    self.assertAlmostEqual(2.0, gra.upperThreshold, 4)
    gra.upperThreshold = 10
    self.assertAlmostEqual(10.0, gra.upperThreshold, 4)
    gra.upperThreshold = 11.1
    self.assertAlmostEqual(11.1, gra.upperThreshold, 4)
 
  def test_lowerThreshold(self):
    gra = _gra.new();
    self.assertAlmostEqual(-0.25, gra.lowerThreshold, 4)
    gra.lowerThreshold = 10
    self.assertAlmostEqual(10.0, gra.lowerThreshold, 4)
    gra.lowerThreshold = 11.1
    self.assertAlmostEqual(11.1, gra.lowerThreshold, 4)
     
  def test_zrA(self):
    gra = _gra.new();
    self.assertAlmostEqual(200.0, gra.zrA, 4)
    gra.zrA = 10
    self.assertAlmostEqual(10.0, gra.zrA, 4)
    gra.zrA = 11.1
    self.assertAlmostEqual(11.1, gra.zrA, 4)
     
  def test_zrb(self):
    gra = _gra.new();
    self.assertAlmostEqual(1.6, gra.zrb, 4)
    gra.zrb = 10
    self.assertAlmostEqual(10.0, gra.zrb, 4)
    gra.zrb = 11.1
    self.assertAlmostEqual(11.1, gra.zrb, 4)
     
  def test_apply(self):
    distance = _ravefield.new()
    distance.setData(numpy.zeros((2,2), numpy.float64))
    distance.setValue(0,0,0.1)
    distance.setValue(0,1,0.2)
    distance.setValue(1,0,0.3)
    distance.setValue(1,1,0.4)
    distance.addAttribute("what/gain", 10000.0)
    distance.addAttribute("what/offset", 0.0)
      
    param = _cartesianparam.new()
    param.setData(numpy.zeros((2,2), numpy.float64))
    param.setValue((0,0), 1)
    param.setValue((0,1), 2)
    param.setValue((1,0), 3)
    param.setValue((1,1), 4)
    param.quantity = "ACRR"
    param.gain = 10.0
    param.offset = 2.0
      
    gra = _gra.new()
    gra.A = 1.0
    gra.B = 2.0
    gra.C = 3.0
      
    result = gra.apply(distance, param)
    self.assertAlmostEqual(47.77, result.getConvertedValue((0,0))[1], 2)
    self.assertAlmostEqual(1102.61, result.getConvertedValue((0,1))[1], 2)
    self.assertAlmostEqual(3200.0, result.getConvertedValue((1,0))[1], 4)
    self.assertAlmostEqual(4200.0, result.getConvertedValue((1,1))[1], 4)
 
  def test_apply_DBZH(self):
    distance = _ravefield.new()
    distance.setData(numpy.zeros((2,2), numpy.float64))
    distance.setValue(0,0,0.1)
    distance.setValue(0,1,0.2)
    distance.setValue(1,0,0.3)
    distance.setValue(1,1,0.4)
    distance.addAttribute("what/gain", 10000.0)
    distance.addAttribute("what/offset", 0.0)
     
    param = _cartesianparam.new()
    param.setData(numpy.zeros((2,2), numpy.float64))
    param.setValue((0,0), 1)
    param.setValue((0,1), 2)
    param.setValue((1,0), 3)
    param.setValue((1,1), 4)
    param.quantity = "DBZH"
    param.gain = 10.0
    param.offset = 2.0
     
    gra = _gra.new()
    gra.A = 1.0
    gra.B = 2.0
    gra.C = 3.0
    gra.zrA = 100.0
    gra.zrb = 1.1
     
    result = gra.apply(distance, param)
     
    self.assertAlmostEqual(18.60, result.getConvertedValue((0,0))[1], 2)
    self.assertAlmostEqual(40.7, result.getConvertedValue((0,1))[1], 2)
    self.assertAlmostEqual(54.0, result.getConvertedValue((1,0))[1], 4)
    self.assertAlmostEqual(64.0, result.getConvertedValue((1,1))[1], 4)
    self.assertEqual("GRA: A=1.000000, B=2.000000, C=3.000000, low_db=-0.250000, high_db=2.000000", result.getAttribute("how/task_args"))
    
  def test_apply_DBZH_gain2000(self):
    distance = _ravefield.new()
    distance.setData(numpy.zeros((1,1), numpy.float64))
    distance.setValue(0,0,13)
    distance.addAttribute("what/gain", 2000.0)
    distance.addAttribute("what/offset", 0.0)
     
    param = _cartesianparam.new()
    param.setData(numpy.zeros((1,1), numpy.float64))
    param.setValue((0,0), 78)
    param.quantity = "DBZH"
    param.gain = 0.4
    param.offset = -30.0
     
    gra = _gra.new()
    gra.A = 0.323868
    gra.B = -0.001078
    gra.C = 0.000018
    gra.zrA = 200.0
    gra.zrb = 1.6
     
    result = gra.apply(distance, param)
     
    self.assertAlmostEqual(79.23, result.getValue((0,0))[1], 2)
