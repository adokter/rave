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
## Provides access to the bdb api if it is reachable. Requires both baltrad.bdbclient and jprops
##
## @file
## @author Anders Henja
## @date 2012-04-11

from rave_defines import BDB_CONFIG_FILE, DEX_NODENAME
import string, os, traceback, tempfile, shutil, contextlib
import jprops
import _raveio
import rave_pgf_logger
import rave_tempfile
from baltrad.bdbclient import rest

logger = rave_pgf_logger.create_logger()

class rave_bdb(object):
  config = {}
  configfile = None
  nodename = None
  database = None
  initialized = False
  
  def __init__(self, configfile=BDB_CONFIG_FILE, nodename=DEX_NODENAME):
    self.configfile = configfile
    self.nodename = nodename
    self.config = self._load_configuration(configfile)
    self.database = None
    self.initialized = False
  
  def _load_configuration(self, configfile):
    '''loads the java property configuration file as defined by BDB_CONFIG_FILE
    If jprops not available in classpath or if the file isn't defined it will just
    be ignored.
    :return the properties as a dictionary
    '''
    properties = {}
    try:
      with open(configfile) as fp:
        properties = jprops.load_properties(fp)
    except:
      pass

    return properties

  def load_auth_provider(self):
    ''' loads the authorization provider, default is NoAuth but if noauth isn't found
    it will try with keyczar if it exists in the properties
    :param config: the java properties in a dictionary 
    '''
    providers=[]
    if self.config.has_key('baltrad.bdb.server.auth.providers'):
      providers = [string.strip(s) for s in string.split(self.config['baltrad.bdb.server.auth.providers'],',')]
  
    keyczar_ks_root = None
    keyczar_key = None
    if self.config.has_key('baltrad.bdb.server.auth.keyczar.keystore_root'):
      keyczar_ks_root = self.config['baltrad.bdb.server.auth.keyczar.keystore_root']
    if self.config.has_key("baltrad.bdb.server.auth.keyczar.keys.%s"%self.nodename):
      keyczar_key = self.config["baltrad.bdb.server.auth.keyczar.keys.%s"%self.nodename]

    auth = None
    
    try:
      # Always try to use noauth if possible
      auth = rest.NoAuth()
      if 'noauth' not in providers and 'keyczar' in providers:
        if keyczar_ks_root != None and keyczar_key != None:
          auth = rest.KeyczarAuth("%s/%s"%(keyczar_ks_root, keyczar_key), DEX_NODENAME)
    except Exception, e:
      traceback.print_exc(e)
  
    return auth

  def get_database(self):
    ''' returns the database that provides connection to the bdb server
    '''
    if self.initialized == False:
      try:
        if self.config.has_key('baltrad.bdb.server.uri'):
          uri = self.config['baltrad.bdb.server.uri']
          self.database = rest.RestfulDatabase(uri, self.load_auth_provider())
          self.initialized = True
      except Exception, e:
        traceback.print_exc(e)
  
    return self.database

  def get_rave_object(self, fname):
    ''' returns the rave object as defined by the fname. If the fname is an existing file on the file system, then
    the file will be opened and returned as a rave object. If no fname can be found, an atempt to fetch the file from
    bdb is made. The fetched file will be returned as a rave object on success otherwise an exception will be raised.
    :param fname: the full file path or an bdb uuid
    :return a rave object on success
    :raises an exception if the rave object not can be returned
    '''
    if os.path.exists(fname):
      return _raveio.open(fname).object

    content = self.get_database().get_file_content(fname)
    if content:
      fpd, tmppath = tempfile.mkstemp(suffix='.h5', prefix='ravetmp')
      try:
        with contextlib.closing(content):
          with os.fdopen(fpd, "w") as outf:
            shutil.copyfileobj(content, outf)
            outf.close()
        return _raveio.open(tmppath).object
      finally:
        os.unlink(tmppath)
    else:
      raise Exception, "No content for file %s"%fname

  def get_file(self, uuid):
    ''' returns a file name to a file that can be accessed. The uuid should be an
    identifier in bdb. The returned filename will be a temporary file so it is 
    recommended to remove the file after usage.
    For example
      myname = None
      try:
        myname = bdb.get_file(uuid)
        ... process file ...
      finally:
        if myname != None and os.path.exists(myname):
          os.unlink(myname)
    :param fname: The file name
    :return a temporary file on success
    :raises an Exception on failure or no file could be found
    '''
    content = self.get_database().get_file_content(uuid)
    if content:
      fpd, tmppath = rave_tempfile.mktemp(suffix='.h5', close="True")
      #fpd, tmppath = tempfile.mkstemp(suffix='.h5', prefix='ravetmp')
      try:
        with contextlib.closing(content):
          #with os.fdopen(fpd, "w") as outf:
          with open(tmppath, "w") as outf:
            shutil.copyfileobj(content, outf)
            outf.close()
        return tmppath
      except Exception, e:
        if os.path.exists(tmppath):
          os.unlink(tmppath)
        raise e
    else:
      raise Exception, "No content for file %s"%uuid

if __name__=='__main__':
  dbapi = rave_bdb()
  #print dbapi.get_rave_object('c3ba1289-59d8-498d-8894-414f552ca2a2').date
  print dbapi.get_file('7ced67c2-a519-4d7d-9ad7-a7c239d6b784')
  
#  import math
#  print `get_database().get_sources()`
#  print get_rave_object('c3ba1289-59d8-498d-8894-414f552ca2a2').elangle * 180.0 / math.pi
#  print get_rave_object('c3ba1289-59d8-498d-8894-414f552ca2a2').date

