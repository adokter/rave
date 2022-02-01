'''
Copyright (C) 2010 Swedish Meteorological and Hydrological Institute, SMHI,

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

Tests the overshooting quality plugin

@file
@author Anders Henja (Swedish Meteorological and Hydrological Institute, SMHI)
@date 2011-12-13
'''
import unittest
import os
import math
import string
import rave_overshooting_quality_plugin
import _raveio

class rave_overshooting_quality_plugin_test(unittest.TestCase):
  VOLUME_FIXTURE = "fixtures/pvol_seang_20090501T120000Z.h5"
  SCAN_FIXTURE = "fixtures/scan_sehuv_0.5_20110126T184500Z.h5"
  classUnderTest = None
  
  def setUp(self):
    self.classUnderTest = rave_overshooting_quality_plugin.rave_overshooting_quality_plugin() 

  def tearDown(self):
    self.classUnderTest = None

  def test_getQualityFields(self):
    result = self.classUnderTest.getQualityFields()
    self.assertEqual(1, len(result))
    self.assertEqual("se.smhi.detector.poo", result[0])

  def test_process(self):
    vol = _raveio.open(self.VOLUME_FIXTURE).object
    result, qfield = self.classUnderTest.process(vol)
    self.assertEqual(qfield, ["se.smhi.detector.poo"], "Wrong qfield returned from process")
    maxscan = result.getScanWithMaxDistance()
    field = maxscan.getQualityFieldByHowTask("se.smhi.detector.poo")
    self.assertTrue(field != None)

  def test_process_already_processed(self):
    vol = _raveio.open(self.VOLUME_FIXTURE).object
    result, _ = self.classUnderTest.process(vol, reprocess_quality_flag=False)
    maxscan = result.getScanWithMaxDistance()
    field = maxscan.getQualityFieldByHowTask("se.smhi.detector.poo")
    self.assertEqual(1, maxscan.getNumberOfQualityFields())
    self.assertTrue(field != None)

    result, _ = self.classUnderTest.process(vol, reprocess_quality_flag=False)
    maxscan = result.getScanWithMaxDistance()
    field2 = maxscan.getQualityFieldByHowTask("se.smhi.detector.poo")
    self.assertEqual(1, maxscan.getNumberOfQualityFields())

    self.assertTrue(field == field2)

  def test_process_already_processed_reprocess(self):
    vol = _raveio.open(self.VOLUME_FIXTURE).object
    result, _ = self.classUnderTest.process(vol, reprocess_quality_flag=True)
    maxscan = result.getScanWithMaxDistance()
    field = maxscan.getQualityFieldByHowTask("se.smhi.detector.poo")
    self.assertEqual(1, maxscan.getNumberOfQualityFields())
    self.assertTrue(field != None)

    result, _ = self.classUnderTest.process(vol, reprocess_quality_flag=True)
    maxscan = result.getScanWithMaxDistance()
    field2 = maxscan.getQualityFieldByHowTask("se.smhi.detector.poo")
    self.assertEqual(1, maxscan.getNumberOfQualityFields())

    self.assertTrue(field != field2)

  def test_process_scan(self):
    scan = _raveio.open(self.SCAN_FIXTURE).object
    result, _ = self.classUnderTest.process(scan)
    self.assertTrue(scan == result)

  def test_process_with_quality_control_mode(self):
    scan = _raveio.open(self.SCAN_FIXTURE).object
    result, _ = self.classUnderTest.process(scan,True,quality_control_mode="analyze")
    self.assertTrue(scan == result)

  def test_algorithm(self):
    result = self.classUnderTest.algorithm()
    self.assertNotEqual(-1, str(type(result)).find("CompositeAlgorithmCore"))
 
