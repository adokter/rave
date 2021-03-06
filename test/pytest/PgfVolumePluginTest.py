# -*- coding: latin-1 -*-
'''
Copyright (C) 2011 Swedish Meteorological and Hydrological Institute, SMHI,

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

Tests the volume plugin

@file
@author Anders Henja (Swedish Meteorological and Hydrological Institute, SMHI)
@date 2011-01-19
'''
import unittest
import string
import math
import _raveio
import os
import rave_pgf_volume_plugin
import odim_source

class PgfVolumePluginTest(unittest.TestCase):
  FIXTURES=["fixtures/Z_SCAN_C_ESWI_20101023180200_selul_000000.h5",
            "fixtures/Z_SCAN_C_ESWI_20101023180200_selul_000001.h5",
            "fixtures/Z_SCAN_C_ESWI_20101023180200_selul_000002.h5",
            "fixtures/Z_SCAN_C_ESWI_20101023180200_selul_000003.h5",
            "fixtures/Z_SCAN_C_ESWI_20101023180200_selul_000004.h5",
            "fixtures/Z_SCAN_C_ESWI_20101023180200_selul_000005.h5"]
  
  TEMPORARY_FILE="ravemodule_pgfvolumetest.h5"
  
  def setUp(self):
    if os.path.isfile(self.TEMPORARY_FILE):
      os.unlink(self.TEMPORARY_FILE)
      
  def tearDown(self):
    if os.path.isfile(self.TEMPORARY_FILE):
      os.unlink(self.TEMPORARY_FILE)

  def testGenerateVolume(self):
    args = {"source":"selul","date":"20101023","time":"180000"}
    volume = rave_pgf_volume_plugin.generateVolume(self.FIXTURES, args)

    self.assertNotEqual(-1, string.find(`type(volume)`, "PolarVolumeCore"))
    self.assertAlmostEquals(66, volume.height)
    self.assertAlmostEquals(65.432, volume.latitude*180.0/math.pi,4)
    self.assertAlmostEquals(21.87, volume.longitude*180.0/math.pi,4)
    self.assertEquals(6, volume.getNumberOfScans())
    self.assertAlmostEquals(2.5, volume.getScan(0).elangle * 180.0/math.pi, 4)
    self.assertAlmostEquals(4.0, volume.getScan(1).elangle * 180.0/math.pi, 4)
    self.assertAlmostEquals(8.0, volume.getScan(2).elangle * 180.0/math.pi, 4)
    self.assertAlmostEquals(14.0, volume.getScan(3).elangle * 180.0/math.pi, 4)
    self.assertAlmostEquals(24.0, volume.getScan(4).elangle * 180.0/math.pi, 4)
    self.assertAlmostEquals(40.0, volume.getScan(5).elangle * 180.0/math.pi, 4)
    self.assertEqual("NOD:selul,WMO:02092,RAD:SE41,PLC:Lule\xc3\xa5", volume.source)

  # Where's the test?
  def testGenerateVolumeAndSave(self):
    args = {"source":"selul","date":"20101023","time":"180000"}
    volume = rave_pgf_volume_plugin.generateVolume(self.FIXTURES, args)
    
    ios = _raveio.new()
    ios.object = volume
    ios.filename = self.TEMPORARY_FILE
    ios.save()

    ios = None
    
  def testGenerate(self):
    args = ["source", "selul","date","20101023","time","180000"]
    outfile = rave_pgf_volume_plugin.generate(self.FIXTURES, args)
    
    expected_outfile_beginning = "rave%d-" % os.getpid()
    expected_outfile_end = ".h5"
     
    outfile_base = os.path.basename(outfile)
    
    self.assertTrue(outfile_base.startswith(expected_outfile_beginning))
    self.assertTrue(outfile_base.endswith(expected_outfile_end))
    
    os.remove(outfile)

if __name__ == "__main__":
    unittest.main()
