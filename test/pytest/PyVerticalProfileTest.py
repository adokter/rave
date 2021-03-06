'''
Copyright (C) 2009 Swedish Meteorological and Hydrological Institute, SMHI,

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

Tests the verticalprofile module.

@file
@author Anders Henja (Swedish Meteorological and Hydrological Institute, SMHI)
@date 2012-08-24

@co-author Ulf Nordh (Swedish Meteorological and Hydrological Institute, SMHI)
@date 2017-10-27. Updated code with new fields for vertical profiles.
'''
import unittest
import os
import _verticalprofile
import _ravefield
import string
import numpy
import math

class PyVerticalProfileTest(unittest.TestCase):
  def setUp(self):
    pass

  def tearDown(self):
    pass

  def test_new(self):
    obj = _verticalprofile.new()
    self.assertNotEqual(-1, string.find(`type(obj)`, "VerticalProfileCore"))

  def test_isVerticalProfile(self):
    obj = _verticalprofile.new()
    param = _ravefield.new()
    self.assertTrue(_verticalprofile.isVerticalProfile(obj))
    self.assertFalse(_verticalprofile.isVerticalProfile(param))

  def test_setGetLongitude(self):
    obj = _verticalprofile.new()
    self.assertAlmostEquals(0.0, obj.longitude, 4)
    obj.longitude = 1.0
    self.assertAlmostEquals(1.0, obj.longitude, 4)

  def test_setGetLatitude(self):
    obj = _verticalprofile.new()
    self.assertAlmostEquals(0.0, obj.latitude, 4)
    obj.latitude = 1.0
    self.assertAlmostEquals(1.0, obj.latitude, 4)

  def test_setGetHeight(self):
    obj = _verticalprofile.new()
    self.assertAlmostEquals(0.0, obj.height, 4)
    obj.height = 1.0
    self.assertAlmostEquals(1.0, obj.height, 4)

  def test_setGetInterval(self):
    obj = _verticalprofile.new()
    self.assertAlmostEquals(0.0, obj.interval, 4)
    obj.interval = 1.0
    self.assertAlmostEquals(1.0, obj.interval, 4)
    
  def test_setGetMinheight(self):
    obj = _verticalprofile.new()
    self.assertAlmostEquals(0.0, obj.minheight, 4)
    obj.minheight = 1.0
    self.assertAlmostEquals(1.0, obj.minheight, 4)

  def test_setGetMaxheight(self):
    obj = _verticalprofile.new()
    self.assertAlmostEquals(0.0, obj.maxheight, 4)
    obj.maxheight = 1.0
    self.assertAlmostEquals(1.0, obj.maxheight, 4)
    
  def test_setGetstartTime(self):
    obj = _verticalprofile.new()
    self.assertTrue(None == obj.starttime)
    obj.starttime = "000000"
    self.assertEquals("000000", obj.starttime, 4)
    
  def test_setGetendTime(self):
    obj = _verticalprofile.new()
    self.assertTrue(None == obj.endtime)
    obj.endtime = "000000"
    self.assertEquals("000000", obj.endtime, 4)
    
  def test_setGetstartDate(self):
    obj = _verticalprofile.new()
    self.assertTrue(None == obj.startdate)
    obj.startdate = "20171103"
    self.assertEquals("20171103", obj.startdate, 4)
    
  def test_setGetendDate(self):
    obj = _verticalprofile.new()
    self.assertTrue(None == obj.enddate)
    obj.enddate = "20171103"
    self.assertEquals("20171103", obj.enddate, 4)
    
  def test_setGetProduct(self):
    obj = _verticalprofile.new()
    self.assertTrue(None == obj.product)
    obj.product = "VP"
    self.assertEquals("VP", obj.product, 4)

  def test_setGetLevels(self):
    obj = _verticalprofile.new()
    self.assertEquals(0, obj.getLevels())
    obj.setLevels(1)
    self.assertEquals(1, obj.getLevels(), 4)

  def test_setLevels_withField(self):
    obj = _verticalprofile.new()
    f = _ravefield.new()
    f.setData(numpy.zeros((10,1), numpy.uint8))
    f.addAttribute("how/this", 1.0)
    f.addAttribute("what/quantity", "ff")
    obj.addField(f)
    self.assertEquals(10, obj.getLevels())
    try:
      obj.setLevels(1)
      self.fail("Expected AttributeError")
    except AttributeError, e:
      pass
    self.assertEquals(10, obj.getLevels())
  
  def test_setGetFF(self):
    obj = _verticalprofile.new()
    self.assertTrue(None == obj.getFF())
    f = _ravefield.new()
    f.setData(numpy.zeros((10,1), numpy.uint8))
    f.addAttribute("how/this", 1.0)
    obj.setFF(f)
    result = obj.getFF()
    self.assertAlmostEquals(1.0, result.getAttribute("how/this"), 4)
    self.assertEquals("ff", result.getAttribute("what/quantity"))
 
  def test_setGetFFDev(self):
    obj = _verticalprofile.new()
    self.assertTrue(None == obj.getFFDev())
    f = _ravefield.new()
    f.setData(numpy.zeros((10,1), numpy.uint8))
    f.addAttribute("how/this", 1.0)
    obj.setFFDev(f)
    result = obj.getFFDev()
    self.assertAlmostEquals(1.0, result.getAttribute("how/this"), 4)
    self.assertEquals("ff_dev", result.getAttribute("what/quantity"))
    
  def test_setGetW(self):
    obj = _verticalprofile.new()
    self.assertTrue(None == obj.getW())
    f = _ravefield.new()
    f.setData(numpy.zeros((10,1), numpy.uint8))
    f.addAttribute("how/this", 1.0)
    obj.setW(f)
    result = obj.getW()
    self.assertAlmostEquals(1.0, result.getAttribute("how/this"), 4)
    self.assertEquals("w", result.getAttribute("what/quantity"))

  def test_setGetWDev(self):
    obj = _verticalprofile.new()
    self.assertTrue(None == obj.getWDev())
    f = _ravefield.new()
    f.setData(numpy.zeros((10,1), numpy.uint8))
    f.addAttribute("how/this", 1.0)
    obj.setWDev(f)
    result = obj.getWDev()
    self.assertAlmostEquals(1.0, result.getAttribute("how/this"), 4)
    self.assertEquals("w_dev", result.getAttribute("what/quantity"))

  def test_setGetDD(self):
    obj = _verticalprofile.new()
    self.assertTrue(None == obj.getDD())
    f = _ravefield.new()
    f.setData(numpy.zeros((10,1), numpy.uint8))
    f.addAttribute("how/this", 1.0)
    obj.setDD(f)
    result = obj.getDD()
    self.assertAlmostEquals(1.0, result.getAttribute("how/this"), 4)
    self.assertEquals("dd", result.getAttribute("what/quantity"))

  def test_setGetDDDev(self):
    obj = _verticalprofile.new()
    self.assertTrue(None == obj.getDDDev())
    f = _ravefield.new()
    f.setData(numpy.zeros((10,1), numpy.uint8))
    f.addAttribute("how/this", 1.0)
    obj.setDDDev(f)
    result = obj.getDDDev()
    self.assertAlmostEquals(1.0, result.getAttribute("how/this"), 4)
    self.assertEquals("dd_dev", result.getAttribute("what/quantity"))

  def test_setGetDiv(self):
    obj = _verticalprofile.new()
    self.assertTrue(None == obj.getDiv())
    f = _ravefield.new()
    f.setData(numpy.zeros((10,1), numpy.uint8))
    f.addAttribute("how/this", 1.0)
    obj.setDiv(f)
    result = obj.getDiv()
    self.assertAlmostEquals(1.0, result.getAttribute("how/this"), 4)
    self.assertEquals("div", result.getAttribute("what/quantity"))

  def test_setGetDivDev(self):
    obj = _verticalprofile.new()
    self.assertTrue(None == obj.getDivDev())
    f = _ravefield.new()
    f.setData(numpy.zeros((10,1), numpy.uint8))
    f.addAttribute("how/this", 1.0)
    obj.setDivDev(f)
    result = obj.getDivDev()
    self.assertAlmostEquals(1.0, result.getAttribute("how/this"), 4)
    self.assertEquals("div_dev", result.getAttribute("what/quantity"))

  def test_setGetDef(self):
    obj = _verticalprofile.new()
    self.assertTrue(None == obj.getDef())
    f = _ravefield.new()
    f.setData(numpy.zeros((10,1), numpy.uint8))
    f.addAttribute("how/this", 1.0)
    obj.setDef(f)
    result = obj.getDef()
    self.assertAlmostEquals(1.0, result.getAttribute("how/this"), 4)
    self.assertEquals("def", result.getAttribute("what/quantity"))

  def test_setGetDefDev(self):
    obj = _verticalprofile.new()
    self.assertTrue(None == obj.getDefDev())
    f = _ravefield.new()
    f.setData(numpy.zeros((10,1), numpy.uint8))
    f.addAttribute("how/this", 1.0)
    obj.setDefDev(f)
    result = obj.getDefDev()
    self.assertAlmostEquals(1.0, result.getAttribute("how/this"), 4)
    self.assertEquals("def_dev", result.getAttribute("what/quantity"))

  def test_setGetAD(self):
    obj = _verticalprofile.new()
    self.assertTrue(None == obj.getAD())
    f = _ravefield.new()
    f.setData(numpy.zeros((10,1), numpy.uint8))
    f.addAttribute("how/this", 1.0)
    obj.setAD(f)
    result = obj.getAD()
    self.assertAlmostEquals(1.0, result.getAttribute("how/this"), 4)
    self.assertEquals("ad", result.getAttribute("what/quantity"))

  def test_setGetADDev(self):
    obj = _verticalprofile.new()
    self.assertTrue(None == obj.getADDev())
    f = _ravefield.new()
    f.setData(numpy.zeros((10,1), numpy.uint8))
    f.addAttribute("how/this", 1.0)
    obj.setADDev(f)
    result = obj.getADDev()
    self.assertAlmostEquals(1.0, result.getAttribute("how/this"), 4)
    self.assertEquals("ad_dev", result.getAttribute("what/quantity"))

  def test_setGetDBZ(self):
    obj = _verticalprofile.new()
    self.assertTrue(None == obj.getDBZ())
    f = _ravefield.new()
    f.setData(numpy.zeros((10,1), numpy.uint8))
    f.addAttribute("how/this", 1.0)
    obj.setDBZ(f)
    result = obj.getDBZ()
    self.assertAlmostEquals(1.0, result.getAttribute("how/this"), 4)
    self.assertEquals("dbz", result.getAttribute("what/quantity"))

  def test_setGetDBZDev(self):
    obj = _verticalprofile.new()
    self.assertTrue(None == obj.getDBZDev())
    f = _ravefield.new()
    f.setData(numpy.zeros((10,1), numpy.uint8))
    f.addAttribute("how/this", 1.0)
    obj.setDBZDev(f)
    result = obj.getDBZDev()
    self.assertAlmostEquals(1.0, result.getAttribute("how/this"), 4)
    self.assertEquals("dbz_dev", result.getAttribute("what/quantity"))

  def test_setGetHGHT(self):
    obj = _verticalprofile.new()
    self.assertTrue(None == obj.getHGHT())
    f = _ravefield.new()
    f.setData(numpy.zeros((10,1), numpy.uint8))
    f.addAttribute("how/this", 1.0)
    obj.setHGHT(f)
    result = obj.getHGHT()
    self.assertAlmostEquals(1.0, result.getAttribute("how/this"), 4)
    self.assertEquals("HGHT", result.getAttribute("what/quantity"))
    
  def test_setGetUWND(self):
    obj = _verticalprofile.new()
    self.assertTrue(None == obj.getUWND())
    f = _ravefield.new()
    f.setData(numpy.zeros((10,1), numpy.uint8))
    f.addAttribute("how/this", 1.0)
    obj.setUWND(f)
    result = obj.getUWND()
    self.assertAlmostEquals(1.0, result.getAttribute("how/this"), 4)
    self.assertEquals("UWND", result.getAttribute("what/quantity"))
    
  def test_setGetVWND(self):
    obj = _verticalprofile.new()
    self.assertTrue(None == obj.getVWND())
    f = _ravefield.new()
    f.setData(numpy.zeros((10,1), numpy.uint8))
    f.addAttribute("how/this", 1.0)
    obj.setVWND(f)
    result = obj.getVWND()
    self.assertAlmostEquals(1.0, result.getAttribute("how/this"), 4)
    self.assertEquals("VWND", result.getAttribute("what/quantity"))
    
  def test_setGetNV(self):
    obj = _verticalprofile.new()
    self.assertTrue(None == obj.getNV())
    f = _ravefield.new()
    f.setData(numpy.zeros((10,1), numpy.uint8))
    f.addAttribute("how/this", 1.0)
    obj.setNV(f)
    result = obj.getNV()
    self.assertAlmostEquals(1.0, result.getAttribute("how/this"), 4)
    self.assertEquals("n", result.getAttribute("what/quantity"))

  def test_addField(self):
    obj = _verticalprofile.new()
    f = _ravefield.new()
    f.setData(numpy.zeros((10,1), numpy.uint8))
    f.addAttribute("how/this", 1.0)
    f.addAttribute("what/quantity", "ff")
    obj.addField(f)
    result = obj.getField("ff")
    self.assertAlmostEquals(1.0, result.getAttribute("how/this"), 4)
    self.assertEquals("ff", result.getAttribute("what/quantity"))
    self.assertEquals(10, obj.getLevels())

  def test_addField_withLevels_preset(self):
    obj = _verticalprofile.new()
    obj.setLevels(10)
    f = _ravefield.new()
    f.setData(numpy.zeros((11,1), numpy.uint8))
    f.addAttribute("how/this", 1.0)
    f.addAttribute("what/quantity", "ff")
    try:
      obj.addField(f)
      self.fail("Expected AttributeError")
    except AttributeError, e:
      pass
    result = obj.getField("ff")
    self.assertEquals(None, result)

  def test_addField_differentSize(self):
    obj = _verticalprofile.new()
    f = _ravefield.new()
    f.setData(numpy.zeros((10,1), numpy.uint8))
    f.addAttribute("how/this", 1.0)
    f.addAttribute("what/quantity", "ff")
    obj.addField(f)
    f2 = _ravefield.new()
    f2.setData(numpy.zeros((11,1), numpy.uint8))
    f2.addAttribute("how/this", 2.0)
    f2.addAttribute("what/quantity", "ff_dev")

    try:
      obj.addField(f2)
      self.fail("Expected AttributeError")
    except AttributeError, e:
      pass
    result = obj.getField("ff")
    self.assertAlmostEquals(1.0, result.getAttribute("how/this"), 4)
    result2 = obj.getField("ff_dev")
    self.assertEquals(None, result2)

  def test_addField_tooHighXsize(self):
    obj = _verticalprofile.new()
    f = _ravefield.new()
    f.setData(numpy.zeros((10,10), numpy.uint8))
    f.addAttribute("how/this", 1.0)
    f.addAttribute("what/quantity", "ff")
    try:
      obj.addField(f)
      self.fail("Expected AttributeError")
    except AttributeError, e:
      pass
    self.assertEquals(None, obj.getField("ff"))

  def test_addField_dev_bird(self):
    obj = _verticalprofile.new()
    f = _ravefield.new()
    f.setData(numpy.zeros((10,1), numpy.uint8))
    f.addAttribute("how/this", 1.0)
    f.addAttribute("what/quantity", "dev_bird")
    obj.addField(f)
    result = obj.getField("dev_bird")
    self.assertAlmostEquals(1.0, result.getAttribute("how/this"), 4)
    self.assertEquals("dev_bird", result.getAttribute("what/quantity"))
    self.assertEquals(10, obj.getLevels())
    
  def test_addField_no_quantity(self):
    obj = _verticalprofile.new()
    f = _ravefield.new()
    f.setData(numpy.zeros((10,1), numpy.uint8))
    f.addAttribute("how/this", 1.0)
    try:
      obj.addField(f)
      self.fail("Expected AttributeError")
    except AttributeError, e:
      pass

  def test_getFields(self):
    obj = _verticalprofile.new()
    f = _ravefield.new()
    f.setData(numpy.zeros((10,1), numpy.uint8))
    f.addAttribute("how/this", 1.0)
    f.addAttribute("what/quantity", "ff")
    obj.addField(f)

    f2 = _ravefield.new()
    f2.setData(numpy.zeros((10,1), numpy.uint8))
    f2.addAttribute("how/this", 2.0)
    f2.addAttribute("what/quantity", "ff_dev")
    obj.addField(f2)
    
    result = obj.getFields()
    self.assertEquals(2, len(result))
    if result[0].getAttribute("what/quantity") == "ff":
      self.assertEquals("ff_dev", result[1].getAttribute("what/quantity"))
    elif result[0].getAttribute("what/quantity") == "ff_dev":
      self.assertEquals("ff", result[1].getAttribute("what/quantity"))
    else:
      self.fail("Unexpected combination of quantities")

  def test_addAttribute(self):
    obj = _verticalprofile.new()
    obj.addAttribute("how/astr", "astr")
    obj.addAttribute("how/int", 10)
    obj.addAttribute("how/double", 10.2)
    self.assertEquals("astr", obj.getAttribute("how/astr"))
    self.assertEquals(10, obj.getAttribute("how/int"))
    self.assertAlmostEqual(10.2, obj.getAttribute("how/double"), 4)
    
  def test_add_how_array_attribute_double(self):
    obj = _verticalprofile.new()
    obj.addAttribute("how/something", numpy.arange(10).astype(numpy.float32))
    result = obj.getAttribute("how/something")
    self.assertTrue(isinstance(result, numpy.ndarray))
    self.assertEquals(10, len(result))
    self.assertAlmostEquals(0.0, result[0], 2)
    self.assertAlmostEquals(3.0, result[3], 2)
    self.assertAlmostEquals(5.0, result[5], 2)
    self.assertAlmostEquals(9.0, result[9], 2)
  
  def test_hasAttribute(self):
    obj = _verticalprofile.new()
    obj.addAttribute("how/something", 1.0)
    obj.addAttribute("how/something2", "jupp")
    self.assertEquals(True, obj.hasAttribute("how/something"))
    self.assertEquals(True, obj.hasAttribute("how/something2"))
    self.assertEquals(False, obj.hasAttribute("how/something3"))
    try:
      obj.hasAttribute(None)
      self.fail("Expected TypeError")
    except TypeError, e:
      pass

  def test_getAttributeNames(self):
    obj = _verticalprofile.new()
    obj.addAttribute("how/something", 1.0)
    obj.addAttribute("how/something2", "jupp")
    result = obj.getAttributeNames()
    self.assertTrue(set(result) == set(["how/something", "how/something2"]))

if __name__ == "__main__":
  #import sys;sys.argv = ['', 'Test.testName']
  unittest.main()
