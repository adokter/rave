'''
Copyright (C) 2010- Swedish Meteorological and Hydrological Institute (SMHI)

This file is part of RAVE.

RAVE is free software: you can redistribute it and/or modify
it under the terms of the GNU Lesser General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

RAVE is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
See the GNU Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public License
along with RAVE.  If not, see <http://www.gnu.org/licenses/>.

'''
## Utility functions for doing common tasks
##

## @file
## @author Anders Henja, SMHI
## @date 2014-05-06
import _polarscan, _polarvolume

def str_to_bool(s):
  if s != None:
    if s.lower() == 'true' or s.lower() == 'yes' or s.lower() == 'y' or s.lower() == '1':
      return True
  return False

def get_malfunc_from_obj(obj):
  if obj.hasAttribute("how/malfunc"):
    return str_to_bool(obj.getAttribute("how/malfunc"))
  return False

def is_polar_malfunc(obj):
  result = False
  if _polarvolume.isPolarVolume(obj):
    result = get_malfunc_from_obj(obj)
    if not result:
      for i in range(obj.getNumberOfScans()):
        result = get_malfunc_from_obj(obj.getScan(i))
        if result:
          break
  elif _polarscan.isPolarScan(obj):
    result = get_malfunc_from_obj(obj)
  else:
    raise Exception, "Neither polar volume or polar scan"
  return result

def remove_malfunc_from_volume(obj):
  result = obj
  if _polarvolume.isPolarVolume(obj):
    if get_malfunc_from_obj(obj):
      return None
    for i in range(obj.getNumberOfScans()-1,-1,-1):
      if get_malfunc_from_obj(obj.getScan(i)):
        obj.removeScan(i)
  return result

def remove_malfunc(obj):
  result = obj
  if _polarvolume.isPolarVolume(obj):
    result = remove_malfunc_from_volume(obj)
  elif _polarscan.isPolarScan(obj):
    if get_malfunc_from_obj(obj):
      result = None
  return result

    
