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
import unittest, os, datetime
from rave_dom import wmo_station, observation
import rave_dom_db

import contextlib
from sqlalchemy import engine, event, exc as sqlexc, sql
from sqlalchemy.orm import mapper, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.exc import IntegrityError

Base = declarative_base()

#from sqlalchemy.orm import Base

DB_URL = os.environ.get("RAVE_TESTDB_URI", "")

##
# Simple helper for verifying that data access is behaving as expected
#
class testdb(object):
  def __init__(self):
    self._engine = engine.create_engine(DB_URL)
  
  def query(self, str):
    result = []
    with self.get_connection() as conn:
      cursor = conn.execute(str)
      for row in cursor:
        keys = row.keys()
        v = {}
        for k in keys:
          v[k] = row[k]
        #print row.keys()
        result.append(v)
    return result
  
  def add(self, obj):
    Session = sessionmaker(bind=self._engine)
    session = Session()
    session.add(obj)
    session.commit()
    session = None
  
  def get_connection(self):
    return contextlib.closing(self._engine.connect())

class rave_dom_db_test(unittest.TestCase):
  # I am using class under test for creating and dropping the tables.
  
  def setUp(self):
    self.classUnderTest = rave_dom_db.create_db(DB_URL)
    self.classUnderTest.drop()
    self.classUnderTest.create() 

  def tearDown(self):
    self.classUnderTest.drop()
    #pass

  def test_add(self):
    #station, country, type, date, time, longitude, latitude
    obs = observation("12345", "SWEDEN", 0, "20101010", "113000", 13.031, 60.123)
    self.classUnderTest.add(obs)
    
    result = testdb().query("SELECT * FROM rave_observation where station = '12345'")
    self.assertEquals(1, len(result))
    self.assertEquals("12345", result[0]["station"])
    self.assertEquals("SWEDEN", result[0]["country"])
    self.assertEquals("2010-10-10", result[0]["date"].strftime("%Y-%m-%d"))
    self.assertEquals("11:30:00", result[0]["time"].strftime("%H:%M:%S"))
    self.assertAlmostEquals(60.123, result[0]["latitude"], 4)
    self.assertAlmostEquals(13.031, result[0]["longitude"], 4)


  def test_add_2(self):
    #station, country, type, date, time, longitude, latitude
    obs = observation("12345", "SWEDEN", 0, "20101010", "113000", 13.031, 60.123)
    obs.visibility = 1.0
    obs.windtype = observation.WIND_TYPE_ESTIMATED
    obs.cloudcover = 2
    obs.winddirection = 3
    obs.temperature = 4.0
    obs.dewpoint = 5.0
    obs.relativehumidity = 6.0
    obs.pressure = 7.0
    obs.sea_lvl_pressure = 8.0
    obs.pressure_change = 9.0
    obs.liquid_precipitation = 10.0
    obs.accumulation_period = 11
    
    self.classUnderTest.add(obs)
    
    result = testdb().query("SELECT * FROM rave_observation where station = '12345'")
    self.assertEquals(1, len(result))
    self.assertEquals("12345", result[0]["station"])
    self.assertEquals("SWEDEN", result[0]["country"])
    self.assertEquals("2010-10-10", result[0]["date"].strftime("%Y-%m-%d"))
    self.assertEquals("11:30:00", result[0]["time"].strftime("%H:%M:%S"))
    self.assertAlmostEquals(60.123, result[0]["latitude"], 4)
    self.assertAlmostEquals(13.031, result[0]["longitude"], 4)
    
    self.assertAlmostEquals(1.0, result[0]["visibility"], 4)
    self.assertEquals(0, result[0]["windtype"])
    self.assertEquals(2, result[0]["cloudcover"])
    self.assertEquals(3, result[0]["winddirection"])
    self.assertAlmostEquals(4.0, result[0]["temperature"], 4)
    self.assertAlmostEquals(5.0, result[0]["dewpoint"], 4)
    self.assertAlmostEquals(6.0, result[0]["relativehumidity"], 4)
    self.assertAlmostEquals(7.0, result[0]["pressure"], 4)
    self.assertAlmostEquals(8.0, result[0]["sea_lvl_pressure"], 4)
    self.assertAlmostEquals(9.0, result[0]["pressure_change"], 4)
    self.assertAlmostEquals(10.0, result[0]["liquid_precipitation"], 4)
    self.assertEquals(11, result[0]["accumulation_period"])

  def test_get_observation(self):
    # I am using the dom defined observation instead of trying to define some generic dict variant
    # for populating a db table
    obs = observation("54321", "SWEDEN", 0, "20101010", "113000", 13.031, 60.123)
    obs.visibility = 1.0
    obs.windtype = observation.WIND_TYPE_ESTIMATED
    obs.cloudcover = 2
    obs.winddirection = 3
    obs.temperature = 4.0
    obs.dewpoint = 5.0
    obs.relativehumidity = 6.0
    obs.pressure = 7.0
    obs.sea_lvl_pressure = 8.0
    obs.pressure_change = 9.0
    obs.liquid_precipitation = 10.0
    obs.accumulation_period = 11
    obs2 = observation("54322", "SWEDEN", 0, "20101010", "113000", 13.031, 60.123)
    
    testdb().add(obs)
    testdb().add(obs2)
    
    # Test
    with self.classUnderTest.get_session() as s:
      result = s.query(observation).filter_by(station="54321").all()[0]
    #result = self.classUnderTest.get_session().query(observation).filter_by(station="54321").all()[0]
    self.assertEquals("54321", result.station)
    self.assertEquals("SWEDEN", result.country)
    self.assertEquals("2010-10-10", result.date.strftime("%Y-%m-%d"))
    self.assertEquals("11:30:00", result.time.strftime("%H:%M:%S"))
    self.assertAlmostEquals(60.123, result.latitude, 4)
    self.assertAlmostEquals(13.031, result.longitude, 4)

  def test_get_observations_in_bbox(self):
    db = testdb()
    db.add(observation("54321", "SWEDEN", 0, "20101010", "113000", 13.031, 60.123))
    db.add(observation("54322", "SWEDEN", 0, "20101010", "113000", 14.031, 61.123))  #X
    db.add(observation("54323", "SWEDEN", 0, "20101010", "113000", 13.531, 60.523))  #X
    db.add(observation("54324", "SWEDEN", 0, "20101010", "113000", 16.031, 62.123))
    db.add(observation("54325", "SWEDEN", 0, "20101010", "113000", 13.131, 60.223))
    db.add(observation("54326", "SWEDEN", 0, "20101010", "113000", 14.531, 61.523))
    db.add(observation("54325", "SWEDEN", 0, "20101010", "114500", 13.131, 60.223))
    
    # Test
    result = self.classUnderTest.get_observations_in_bbox(13.0,61.5,15.0,60.5)

    # Verify result
    self.assertEquals(2, len(result))
    self.assertEquals("54322", result[0].station)
    self.assertEquals("54323", result[1].station)

  def test_get_observations_in_bbox_2(self):
    # Tests that if we don't specify a dateinterval, we always get the latest
    db = testdb()
    db.add(observation("54321", "SWEDEN", 0, "20101010", "113000", 13.031, 60.123))
    db.add(observation("54322", "SWEDEN", 0, "20101010", "113000", 14.031, 61.123))  #X
    db.add(observation("54323", "SWEDEN", 0, "20101010", "113000", 13.531, 60.523))  #X
    db.add(observation("54324", "SWEDEN", 0, "20101010", "113000", 16.031, 62.123))
    db.add(observation("54325", "SWEDEN", 0, "20101010", "113000", 13.131, 60.223))  #X
    db.add(observation("54326", "SWEDEN", 0, "20101010", "113000", 14.531, 61.523))
    db.add(observation("54325", "SWEDEN", 0, "20101010", "114500", 13.131, 60.223))  #X
    
    # Test
    result = self.classUnderTest.get_observations_in_bbox(13.0,61.5,15.0,60.2)

    # Verify result
    self.assertEquals(3, len(result))
    self.assertEquals("54322", result[0].station)
    self.assertEquals("54323", result[1].station)   
    self.assertEquals("54325", result[2].station)   
    self.assertEquals("2010-10-10", result[2].date.strftime("%Y-%m-%d"))
    self.assertEquals("11:45:00", result[2].time.strftime("%H:%M:%S"))

  def test_get_observations_in_bbox_3(self):
    # Tests that date interval is working
    db = testdb()
    db.add(observation("54321", "SWEDEN", 0, "20101010", "113000", 13.031, 60.123))
    db.add(observation("54321", "SWEDEN", 0, "20101010", "114500", 13.031, 60.123))
    db.add(observation("54321", "SWEDEN", 0, "20101010", "120000", 13.031, 60.123))
    db.add(observation("54322", "SWEDEN", 0, "20101010", "113000", 14.031, 61.123)) #X
    db.add(observation("54323", "SWEDEN", 0, "20101010", "114500", 13.531, 60.523)) #X
    db.add(observation("54324", "SWEDEN", 0, "20101010", "120000", 16.031, 62.123))
    db.add(observation("54324", "SWEDEN", 0, "20101010", "120015", 16.031, 62.123))
    db.add(observation("54325", "SWEDEN", 0, "20101010", "113000", 13.131, 60.223)) #X
    db.add(observation("54326", "SWEDEN", 0, "20101010", "113000", 14.531, 61.523))
    
    # Test
    result = self.classUnderTest.get_observations_in_bbox(13.0,61.5,15.0,60.2,
                                                          datetime.datetime(2010,10,10,11,30),
                                                          datetime.datetime(2010,10,10,11,44))

    # Verify result
    self.assertEquals(2, len(result))
    self.assertEquals("54322", result[0].station)
    self.assertEquals("2010-10-10", result[0].date.strftime("%Y-%m-%d"))
    self.assertEquals("11:30:00", result[0].time.strftime("%H:%M:%S"))
    self.assertEquals("54325", result[1].station)   
    self.assertEquals("2010-10-10", result[1].date.strftime("%Y-%m-%d"))
    self.assertEquals("11:30:00", result[1].time.strftime("%H:%M:%S"))
  
  def test_get_observations_in_interval(self):
    db = testdb()
    db.add(observation("54321", "SWEDEN", 0, "20101010", "113000", 13.031, 60.123))
    db.add(observation("54321", "SWEDEN", 0, "20101010", "114500", 13.031, 60.123))
    db.add(observation("54321", "SWEDEN", 0, "20101010", "120000", 13.031, 60.123))
    db.add(observation("54322", "SWEDEN", 0, "20101010", "113000", 14.031, 61.123)) #X
    db.add(observation("54322", "SWEDEN", 0, "20101010", "114500", 13.531, 60.523)) #X
    db.add(observation("54323", "SWEDEN", 0, "20101010", "120000", 16.031, 62.123))
    db.add(observation("54324", "SWEDEN", 0, "20101010", "120030", 16.031, 62.123))
    
    # Test
    result = self.classUnderTest.get_observations_in_interval(datetime.datetime(2010,10,10,11,30),
                                                              datetime.datetime(2010,10,10,11,45))
    self.assertEquals(4, len(result))
    self.assertEquals("54321", result[0].station)
    self.assertEquals("11:30:00", result[0].time.strftime("%H:%M:%S"))
    self.assertEquals("54321", result[1].station)
    self.assertEquals("11:45:00", result[1].time.strftime("%H:%M:%S"))
    self.assertEquals("54322", result[2].station)
    self.assertEquals("11:30:00", result[2].time.strftime("%H:%M:%S"))
    self.assertEquals("54322", result[3].station)
    self.assertEquals("11:45:00", result[3].time.strftime("%H:%M:%S"))

  def test_get_observations_in_interval_2(self):
    db = testdb()
    db.add(observation("54321", "SWEDEN", 0, "20101010", "113000", 13.031, 60.123))
    db.add(observation("54321", "SWEDEN", 0, "20101010", "114500", 13.031, 60.123))
    db.add(observation("54321", "SWEDEN", 0, "20101010", "120000", 13.031, 60.123))
    db.add(observation("54322", "SWEDEN", 0, "20101010", "113000", 14.031, 61.123)) #X
    db.add(observation("54322", "SWEDEN", 0, "20101010", "114500", 13.531, 60.523)) #X
    db.add(observation("54323", "SWEDEN", 0, "20101010", "120000", 16.031, 62.123))
    db.add(observation("54324", "SWEDEN", 0, "20101010", "120030", 16.031, 62.123))
    
    # Test
    result = self.classUnderTest.get_observations_in_interval(datetime.datetime(2010,10,10,11,30),
                                                              datetime.datetime(2010,10,10,11,45),
                                                              ["54322","54323"])
    self.assertEquals(2, len(result))
    self.assertEquals("54322", result[0].station)
    self.assertEquals("11:30:00", result[0].time.strftime("%H:%M:%S"))
    self.assertEquals("54322", result[1].station)
    self.assertEquals("11:45:00", result[1].time.strftime("%H:%M:%S"))

  def test_get_observations_in_interval_3(self):
    db = testdb()
    db.add(observation("54321", "SWEDEN", 0, "20101010", "113000", 13.031, 60.123))
    db.add(observation("54321", "SWEDEN", 0, "20101010", "114500", 13.031, 60.123))
    db.add(observation("54321", "SWEDEN", 0, "20101010", "120000", 13.031, 60.123))
    db.add(observation("54322", "SWEDEN", 0, "20101010", "113000", 14.031, 61.123)) #X
    db.add(observation("54322", "SWEDEN", 0, "20101010", "114500", 13.531, 60.523)) #X
    db.add(observation("54323", "SWEDEN", 0, "20101010", "120000", 16.031, 62.123))
    db.add(observation("54324", "SWEDEN", 0, "20101010", "120030", 16.031, 62.123))
    
    # Test
    result = self.classUnderTest.get_observations_in_interval(datetime.datetime(2010,10,10,11,30),
                                                              datetime.datetime(2010,10,10,12,00),
                                                              ["54322","54323"])
    self.assertEquals(3, len(result))
    self.assertEquals("54322", result[0].station)
    self.assertEquals("11:30:00", result[0].time.strftime("%H:%M:%S"))
    self.assertEquals("54322", result[1].station)
    self.assertEquals("11:45:00", result[1].time.strftime("%H:%M:%S"))
    self.assertEquals("54323", result[2].station)
    self.assertEquals("12:00:00", result[2].time.strftime("%H:%M:%S"))
    
  
  def test_add_duplicate_observation(self):
    db = testdb()
    obs = observation("54321", "SWEDEN", 0, "20101010", "113000", 13.031, 60.123)
    obs.temperature = 10.0
    db.add(obs)
    obs = observation("54322", "SWEDEN", 0, "20101010", "113000", 13.031, 60.123)
    obs.temperature = 11.0
    db.add(obs)

    # Test
    nobs = observation("54321", "SWEDEN", 0, "20101010", "113000", 13.031, 60.123)
    nobs.temperature = 11.0
    try:
      self.classUnderTest.add(nobs)
      self.fail("Expected IntegrityError")
    except IntegrityError, e:
      pass

  def test_merge_observation(self):
    db = testdb()
    obs = observation("54321", "SWEDEN", 0, "20101010", "113000", 13.031, 60.123)
    obs.temperature = 10.0
    db.add(obs)

    # Test
    nobs = observation("54321", "SWEDEN", 0, "20101010", "113000", 13.031, 60.123)
    nobs.temperature = 11.0
    nobs2 = observation("54322", "SWEDEN", 0, "20101010", "113000", 13.031, 60.123)
    nobs2.temperature = 12.0

    self.classUnderTest.merge([nobs,nobs2])
    result = testdb().query("SELECT * FROM rave_observation order by station")
    self.assertEquals(2, len(result))
    self.assertEquals("54321", result[0]["station"])
    self.assertAlmostEquals(11.0, result[0]["temperature"], 4)
    self.assertEquals("54322", result[1]["station"])
    self.assertAlmostEquals(12.0, result[1]["temperature"], 4)

  def test_add_station(self):
    #__init__(self, country, countrycode, stationnbr, subnbr, stationname, longitude, latitude):
    station = wmo_station("SWEDEN", "0123", "12345", "0", "Pelle", 10.10, 20.20)
    
    self.classUnderTest.add(station)
    
    result = testdb().query("SELECT * FROM rave_wmo_station where stationnumber = '12345'")
    self.assertEquals(1, len(result))
    self.assertEquals("12345", result[0]["stationnumber"])
    self.assertEquals("0", result[0]["stationsubnumber"])
    self.assertEquals("Pelle", result[0]["stationname"])
    self.assertAlmostEquals(10.10, result[0]["longitude"], 4)
    self.assertAlmostEquals(20.20, result[0]["latitude"], 4)

  def test_add_substation(self):
    #__init__(self, country, countrycode, stationnbr, subnbr, stationname, longitude, latitude):
    station1 = wmo_station("SWEDEN", "0123", "12345", "0", "Pelle", 10.10, 20.20)
    station2 = wmo_station("SWEDEN", "0123", "12345", "1", "Pelle", 10.10, 20.20)
    
    self.classUnderTest.add(station1)
    self.classUnderTest.add(station2)
    
    result = testdb().query("SELECT * FROM rave_wmo_station where stationnumber = '12345' order by stationsubnumber")
    self.assertEquals(2, len(result))
    self.assertEquals("12345", result[0]["stationnumber"])
    self.assertEquals("0", result[0]["stationsubnumber"])
    self.assertEquals("12345", result[1]["stationnumber"])
    self.assertEquals("1", result[1]["stationsubnumber"])

  def test_get_station(self):
    #__init__(self, country, countrycode, stationnbr, subnbr, stationname, longitude, latitude):
    station1 = wmo_station("SWEDEN", "0123", "12345", "0", "Pelle", 10.10, 20.20)
    station2 = wmo_station("SWEDEN", "0123", "12346", "0", "Nisse", 30.10, 40.20)
    
    testdb().add(station1)
    testdb().add(station2)
    
    result = self.classUnderTest.get_station("12346")
    self.assertEquals("12346", result.stationnumber)
    self.assertEquals("Nisse", result.stationname)
    self.assertAlmostEquals(30.10, result.longitude, 4)
    self.assertAlmostEquals(40.20, result.latitude, 4)
      