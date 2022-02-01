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

Tests the pgf volume plugin

@file
@author Anders Henja (Swedish Meteorological and Hydrological Institute, SMHI)
@date 2011-12-13
'''
import unittest
import os
import math
import string
import rave_pgf_volume_plugin
import rave_quality_plugin, rave_pgf_quality_registry
import mock

class rave_pgf_volume_plugin_test(unittest.TestCase):
  def setUp(self):
    self.qc_check_1_mock = mock.Mock(spec=rave_quality_plugin.rave_quality_plugin)
    self.qc_check_2_mock = mock.Mock(spec=rave_quality_plugin.rave_quality_plugin)
    rave_pgf_quality_registry.add_plugin("qc.check.1", self.qc_check_1_mock)
    rave_pgf_quality_registry.add_plugin("qc.check.2", self.qc_check_2_mock)

  def tearDown(self):
    rave_pgf_quality_registry.remove_plugin("qc.check.1")
    rave_pgf_quality_registry.remove_plugin("qc.check.2")
    
  def test_perform_quality_control(self):
    vol = object()
    
    self.qc_check_1_mock.process.return_value = vol
    self.qc_check_2_mock.process.return_value = vol

    result = rave_pgf_volume_plugin.perform_quality_control(vol, ["qc.check.1","qc.check.2"])
    
    expected_qc_check_1_calls = [mock.call.process(vol, True, "analyze_and_apply")]
    expected_qc_check_2_calls = [mock.call.process(vol, True, "analyze_and_apply")]
    
    self.assertTrue(expected_qc_check_1_calls == self.qc_check_1_mock.mock_calls)
    self.assertTrue(expected_qc_check_2_calls == self.qc_check_2_mock.mock_calls)
    self.assertTrue(vol == result)

  def test_perform_quality_control_process_return_tuple(self):
    vol = object()
    a1 = object()
    
    self.qc_check_1_mock.process.return_value = vol
    self.qc_check_2_mock.process.return_value = (vol,a1)

    result = rave_pgf_volume_plugin.perform_quality_control(vol, ["qc.check.1","qc.check.2"])
    
    expected_qc_check_1_calls = [mock.call.process(vol, True, "analyze_and_apply")]
    expected_qc_check_2_calls = [mock.call.process(vol, True, "analyze_and_apply")]
    
    self.assertTrue(expected_qc_check_1_calls == self.qc_check_1_mock.mock_calls)
    self.assertTrue(expected_qc_check_2_calls == self.qc_check_2_mock.mock_calls)
    self.assertTrue(vol == result)

  def test_perform_quality_control_quality_control_mode(self):
    vol = object()
    a1 = object()
    
    self.qc_check_1_mock.process.return_value = vol
    self.qc_check_2_mock.process.return_value = (vol,a1)

    result = rave_pgf_volume_plugin.perform_quality_control(vol, ["qc.check.1","qc.check.2"])
    
    expected_qc_check_1_calls = [mock.call.process(vol, True, "analyze_and_apply")]
    expected_qc_check_2_calls = [mock.call.process(vol, True, "analyze_and_apply")]
    
    self.assertTrue(expected_qc_check_1_calls == self.qc_check_1_mock.mock_calls)
    self.assertTrue(expected_qc_check_2_calls == self.qc_check_2_mock.mock_calls)
    self.assertTrue(vol == result)

  def test_perform_quality_control_quality_control_mode_2(self):
    vol = object()
    a1 = object()
    
    self.qc_check_1_mock.process.return_value = vol
    self.qc_check_2_mock.process.return_value = (vol,a1)

    result = rave_pgf_volume_plugin.perform_quality_control(vol, ["qc.check.1","qc.check.2"], "analyze")
    
    expected_qc_check_1_calls = [mock.call.process(vol, True, "analyze")]
    expected_qc_check_2_calls = [mock.call.process(vol, True, "analyze")]
    
    self.assertTrue(expected_qc_check_1_calls == self.qc_check_1_mock.mock_calls)
    self.assertTrue(expected_qc_check_2_calls == self.qc_check_2_mock.mock_calls)
    self.assertTrue(vol == result)

  def test_perform_quality_control_first_process_return_tuple(self):
    vol = object()
    a1 = object()
    
    self.qc_check_1_mock.process.return_value = (vol,a1)
    self.qc_check_2_mock.process.return_value = vol

    result = rave_pgf_volume_plugin.perform_quality_control(vol, ["qc.check.1","qc.check.2"])
    
    expected_qc_check_1_calls = [mock.call.process(vol, True, "analyze_and_apply")]
    expected_qc_check_2_calls = [mock.call.process(vol, True, "analyze_and_apply")]
    
    self.assertTrue(expected_qc_check_1_calls == self.qc_check_1_mock.mock_calls)
    self.assertTrue(expected_qc_check_2_calls == self.qc_check_2_mock.mock_calls)
    self.assertTrue(vol == result)


  def test_generateVolume(self):
    args={}
    args["date"] = "20110101"
    args["time"] = "100000"
    
    files=["fixtures/scan_sehuv_0.5_20110126T184500Z.h5",
           "fixtures/scan_sehuv_1.0_20110126T184600Z.h5",
           "fixtures/scan_sehuv_1.5_20110126T184600Z.h5"]
    
    
    result = rave_pgf_volume_plugin.generateVolume(files, args)
    self.assertEqual(3, result.getNumberOfScans())
    self.assertAlmostEqual(61.5771, result.latitude * 180.0 / math.pi, 4)
    self.assertAlmostEqual(16.7144, result.longitude * 180.0 / math.pi, 4)
    self.assertAlmostEqual(389.0, result.height, 4)
    self.assertTrue(result.source.find("RAD:SE44") >= 0)
    self.assertAlmostEqual(0.86, result.beamwidth * 180.0 / math.pi, 4)
    self.assertAlmostEqual(0.86, result.getScan(0).beamwidth * 180.0 / math.pi, 4)
    self.assertAlmostEqual(0.86, result.getScan(1).beamwidth * 180.0 / math.pi, 4)
    self.assertAlmostEqual(0.86, result.getScan(2).beamwidth * 180.0 / math.pi, 4)
