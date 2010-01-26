/* --------------------------------------------------------------------
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
/**
 * Defines the functions available when working with polar scans
 * @file
 * @author Anders Henja (Swedish Meteorological and Hydrological Institute, SMHI)
 * @date 2009-10-15
 */
#include "polarscanparam.h"
#include "rave_debug.h"
#include "rave_alloc.h"
#include <string.h>
#include "rave_object.h"
#include "rave_datetime.h"
#include "rave_transform.h"
#include "rave_data2d.h"

/**
 * Represents one param in a scan
 */
struct _PolarScanParam_t {
  RAVE_OBJECT_HEAD /** Always on top */
  RaveData2D_t* data; /**< data ptr */
  char* quantity;    /**< what does this data represent */
  double gain;       /**< gain when scaling */
  double offset;     /**< offset when scaling */
  double nodata;     /**< nodata */
  double undetect;   /**< undetect */
};

/*@{ Private functions */
/**
 * Constructor.
 */
static int PolarScanParam_constructor(RaveCoreObject* obj)
{
  PolarScanParam_t* this = (PolarScanParam_t*)obj;
  this->data = RAVE_OBJECT_NEW(&RaveData2D_TYPE);
  this->quantity = NULL;
  this->gain = 0.0L;
  this->offset = 0.0L;
  this->nodata = 0.0L;
  this->undetect = 0.0L;

  if (this->data == NULL) {
    goto error;
  }
  return 1;
error:
  RAVE_OBJECT_RELEASE(this->data);

  return 0;
}

static int PolarScanParam_copyconstructor(RaveCoreObject* obj, RaveCoreObject* srcobj)
{
  PolarScanParam_t* this = (PolarScanParam_t*)obj;
  PolarScanParam_t* src = (PolarScanParam_t*)srcobj;
  this->data = RAVE_OBJECT_CLONE(src->data);
  this->quantity = NULL;

  if (this->data == NULL) {
    goto error;
  }
  if (!PolarScanParam_setQuantity(this, PolarScanParam_getQuantity(src))) {
    goto error;
  }

  this->gain = src->gain;
  this->offset = src->offset;
  this->nodata = src->nodata;
  this->undetect = src->undetect;

  return 1;
error:
  RAVE_OBJECT_RELEASE(this->data);
  RAVE_FREE(this->quantity);
  return 0;
}

/**
 * Destructor.
 */
static void PolarScanParam_destructor(RaveCoreObject* obj)
{
  PolarScanParam_t* this = (PolarScanParam_t*)obj;
  RAVE_OBJECT_RELEASE(this->data);
  RAVE_FREE(this->quantity);
}

/*@} End of Private functions */

/*@{ Interface functions */
int PolarScanParam_setQuantity(PolarScanParam_t* scanparam, const char* quantity)
{
  int result = 0;
  RAVE_ASSERT((scanparam != NULL), "scanparam == NULL");
  if (quantity != NULL) {
    char* tmp = RAVE_STRDUP(quantity);
    if (tmp != NULL) {
      RAVE_FREE(scanparam->quantity);
      scanparam->quantity = tmp;
      result = 1;
    }
  } else {
    RAVE_FREE(scanparam->quantity);
    result = 1;
  }
  return result;
}

const char* PolarScanParam_getQuantity(PolarScanParam_t* scanparam)
{
  RAVE_ASSERT((scanparam != NULL), "scanparam == NULL");
  return (const char*)scanparam->quantity;
}

void PolarScanParam_setGain(PolarScanParam_t* scanparam, double gain)
{
  RAVE_ASSERT((scanparam != NULL), "scanparam == NULL");
  scanparam->gain = gain;
}

double PolarScanParam_getGain(PolarScanParam_t* scanparam)
{
  RAVE_ASSERT((scanparam != NULL), "scanparam == NULL");
  return scanparam->gain;
}

void PolarScanParam_setOffset(PolarScanParam_t* scanparam, double offset)
{
  RAVE_ASSERT((scanparam != NULL), "scanparam == NULL");
  scanparam->offset = offset;
}

double PolarScanParam_getOffset(PolarScanParam_t* scanparam)
{
  RAVE_ASSERT((scanparam != NULL), "scanparam == NULL");
  return scanparam->offset;
}

void PolarScanParam_setNodata(PolarScanParam_t* scanparam, double nodata)
{
  RAVE_ASSERT((scanparam != NULL), "scanparam == NULL");
  scanparam->nodata = nodata;
}

double PolarScanParam_getNodata(PolarScanParam_t* scanparam)
{
  RAVE_ASSERT((scanparam != NULL), "scanparam == NULL");
  return scanparam->nodata;
}

void PolarScanParam_setUndetect(PolarScanParam_t* scanparam, double undetect)
{
  RAVE_ASSERT((scanparam != NULL), "scanparam == NULL");
  scanparam->undetect = undetect;
}

double PolarScanParam_getUndetect(PolarScanParam_t* scanparam)
{
  RAVE_ASSERT((scanparam != NULL), "scanparam == NULL");
  return scanparam->undetect;
}

int PolarScanParam_setData(PolarScanParam_t* scanparam, long nbins, long nrays, void* data, RaveDataType type)
{
  RAVE_ASSERT((scanparam != NULL), "scanparam == NULL");
  return RaveData2D_setData(scanparam->data, nbins, nrays, data, type);
}

int PolarScanParam_createData(PolarScanParam_t* scanparam, long nbins, long nrays, RaveDataType type)
{
  RAVE_ASSERT((scanparam != NULL), "scanparam == NULL");
  return RaveData2D_createData(scanparam->data, nbins, nrays, type);
}

void* PolarScanParam_getData(PolarScanParam_t* scanparam)
{
  RAVE_ASSERT((scanparam != NULL), "scanparam == NULL");
  return RaveData2D_getData(scanparam->data);
}

long PolarScanParam_getNbins(PolarScanParam_t* scanparam)
{
  RAVE_ASSERT((scanparam != NULL), "scanparam == NULL");
  return RaveData2D_getXsize(scanparam->data);
}

long PolarScanParam_getNrays(PolarScanParam_t* scanparam)
{
  RAVE_ASSERT((scanparam != NULL), "scanparam == NULL");
  return RaveData2D_getYsize(scanparam->data);
}

RaveDataType PolarScanParam_getDataType(PolarScanParam_t* scanparam)
{
  RAVE_ASSERT((scanparam != NULL), "scanparam == NULL");
  return RaveData2D_getType(scanparam->data);
}

RaveValueType PolarScanParam_getValue(PolarScanParam_t* scanparam, int bin, int ray, double* v)
{
  RaveValueType result = RaveValueType_NODATA;
  double value = 0.0;

  RAVE_ASSERT((scanparam != NULL), "scanparam == NULL");

  value = scanparam->nodata;

  if (RaveData2D_getValue(scanparam->data, bin, ray, &value)) {
    result = RaveValueType_DATA;
    if (value == scanparam->nodata) {
      result = RaveValueType_NODATA;
    } else if (value == scanparam->undetect) {
      result = RaveValueType_UNDETECT;
    }
  }

  if (v != NULL) {
    *v = value;
  }

  return result;

}

RaveValueType PolarScanParam_getConvertedValue(PolarScanParam_t* scanparam, int bin, int ray, double* v)
{
  RaveValueType result = RaveValueType_NODATA;
  RAVE_ASSERT((scanparam != NULL), "scanparam == NULL");
  if (v != NULL) {
    result =  PolarScanParam_getValue(scanparam, bin, ray, v);
    if (result == RaveValueType_DATA) {
      *v = scanparam->offset + (*v) * scanparam->gain;
    }
  }
  return result;
}

/*@} End of Interface functions */

RaveCoreObjectType PolarScanParam_TYPE = {
    "PolarScanParam",
    sizeof(PolarScanParam_t),
    PolarScanParam_constructor,
    PolarScanParam_destructor,
    PolarScanParam_copyconstructor
};
