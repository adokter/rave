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
 * Defines the functions available when transforming between different
 * types of products
 * @file
 * @author Anders Henja (Swedish Meteorological and Hydrological Institute, SMHI)
 * @date 2009-10-20
 */
#include "transform.h"
#include "projection.h"
#include "rave_debug.h"
#include "rave_alloc.h"
#include <string.h>

/**
 * Represents one transformator
 */
struct _Transform_t {
  RAVE_OBJECT_HEAD /** Always on top */
  RaveTransformationMethod method;
};

/*@{ Private functions */
/**
 * Constructor
 */
static int Transform_constructor(RaveCoreObject* obj)
{
  Transform_t* transform = (Transform_t*)obj;
  transform->method = NEAREST;
  return 1;
}

/**
 * Destructor
 */
static void Transform_destructor(RaveCoreObject* obj)
{
}

/**
 * Internal routine to handle both cappis and pseudo-cappis since they are similar in behaviour.
 * @param[in] transform - the transformer instance
 * @param[in] pvol - the polar volume
 * @param[in] cartesian - the cartesian (resulting) product
 * @param[in] height - the altitude to create the cappi at
 * @param[in] insidee - the only difference between cappi and pseudo-cappi is if the range/height evaluates to an elevation that is inside or outside the min-max scan elevations.
 * @returns 1 on success otherwise 0
 */
static int Transform_cappis_internal(Transform_t* transform, PolarVolume_t* pvol, Cartesian_t* cartesian, double height, int insidee)
{
  int result = 0;
  long xsize = 0, ysize = 0, x = 0, y = 0;
  double cnodata = 0.0L, cundetect = 0.0L;
  Projection_t* sourcepj = NULL;
  Projection_t* targetpj = NULL;

  RAVE_ASSERT((transform != NULL), "transform was NULL");
  RAVE_ASSERT((pvol != NULL), "pvol was NULL");
  RAVE_ASSERT((cartesian != NULL), "cartesian was NULL");

  if (!Cartesian_isTransformable(cartesian)) {
    RAVE_ERROR0("Cartesian product is not possible to transform");
    goto done;
  }
  if (!PolarVolume_isTransformable(pvol)) {
    RAVE_ERROR0("Polar volume is not possible to transform");
    goto done;
  }

  sourcepj = Cartesian_getProjection(cartesian);
  targetpj = PolarVolume_getProjection(pvol);
  cnodata = Cartesian_getNodata(cartesian);
  cundetect = Cartesian_getUndetect(cartesian);
  xsize = Cartesian_getXSize(cartesian);
  ysize = Cartesian_getYSize(cartesian);

  for (y = 0; y < ysize; y++) {
    double herey = Cartesian_getLocationY(cartesian, y);
    double tmpy = herey;
    for (x = 0; x < xsize; x++) {
      double herex = Cartesian_getLocationX(cartesian, x);
      herey = tmpy; // So that we can use herey over and over again
      RaveValueType valid = RaveValueType_NODATA;
      double v = 0.0L;
      if (!Projection_transform(sourcepj, targetpj, &herex, &herey, NULL)) {
        RAVE_ERROR0("Transform failed");
        goto done;
      }
      valid = PolarVolume_getNearest(pvol, herex, herey, height, insidee, &v);

      if (valid == RaveValueType_NODATA) {
        v = cnodata;
      } else if (valid == RaveValueType_UNDETECT) {
        v = cundetect;
      }
      Cartesian_setValue(cartesian, x, y, v);
    }
  }

  result = 1;
done:
  RAVE_OBJECT_RELEASE(sourcepj);
  RAVE_OBJECT_RELEASE(targetpj);
  return result;
}
/*@} End of Private functions */

/*@{ Interface functions */
int Transform_setMethod(Transform_t* transform, RaveTransformationMethod method)
{
  int result = 0;
  RAVE_ASSERT((transform != NULL), "transform was NULL");
  if (method >= NEAREST && method <= INVERSE) {
    transform->method = method;
    result = 1;
  }
  return result;
}

RaveTransformationMethod Transform_getMethod(Transform_t* transform)
{
  RAVE_ASSERT((transform != NULL), "transform was NULL");
  return transform->method;
}

int Transform_ppi(Transform_t* transform, PolarScan_t* scan, Cartesian_t* cartesian)
{
  int result = 0;
  long xsize = 0, ysize = 0, x = 0, y = 0;
  double cnodata = 0.0L, cundetect = 0.0L;
  Projection_t* sourcepj = NULL;
  Projection_t* targetpj = NULL;

  RAVE_ASSERT((transform != NULL), "transform was NULL");
  RAVE_ASSERT((scan != NULL), "scan was NULL");
  RAVE_ASSERT((cartesian != NULL), "cartesian was NULL");

  if (!Cartesian_isTransformable(cartesian) ||
      !PolarScan_isTransformable(scan)) {
    RAVE_ERROR0("Cartesian product or scan is not possible to transform");
    goto done;
  }

  sourcepj = Cartesian_getProjection(cartesian);
  targetpj = PolarScan_getProjection(scan);
  cnodata = Cartesian_getNodata(cartesian);
  cundetect = Cartesian_getUndetect(cartesian);
  xsize = Cartesian_getXSize(cartesian);
  ysize = Cartesian_getYSize(cartesian);

  for (y = 0; y < ysize; y++) {
    double herey = Cartesian_getLocationY(cartesian, y);
    double tmpy = herey;
    for (x = 0; x < xsize; x++) {
      double herex = Cartesian_getLocationX(cartesian, x);
      herey = tmpy; // So that we can use herey over and over again
      RaveValueType valid = RaveValueType_NODATA;
      double v = 0.0L;
      if (!Projection_transform(sourcepj, targetpj, &herex, &herey, NULL)) {
        RAVE_ERROR0("Transform failed");
        goto done;
      }
      valid = PolarScan_getNearest(scan, herex, herey, &v);

      if (valid == RaveValueType_NODATA) {
        v = cnodata;
      } else if (valid == RaveValueType_UNDETECT) {
        v = cundetect;
      }
      Cartesian_setValue(cartesian, x, y, v);
    }
  }

  result = 1;
done:
  RAVE_OBJECT_RELEASE(sourcepj);
  RAVE_OBJECT_RELEASE(targetpj);
  return result;
}

int Transform_cappi(Transform_t* transform, PolarVolume_t* pvol, Cartesian_t* cartesian, double height)
{
  return Transform_cappis_internal(transform, pvol, cartesian, height, 1);
}

int Transform_pcappi(Transform_t* transform, PolarVolume_t* pvol, Cartesian_t* cartesian, double height)
{
  return Transform_cappis_internal(transform, pvol, cartesian, height, 0);
}

PolarScan_t* Transform_ctoscan(Transform_t* transform, Cartesian_t* cartesian, RadarDefinition_t* def, double angle, const char* quantity)
{
  Projection_t* sourcepj = NULL;
  Projection_t* targetpj = NULL;
  PolarScan_t* result = NULL;
  PolarScan_t* scan = NULL;
  PolarScanParam_t* parameter = NULL;
  CartesianParam_t* cparam = NULL;
  RaveDataType datatype = RaveDataType_UCHAR;

  double nodata = 0.0;
  double undetect = 0.0;
  long ray = 0, bin = 0;
  long nrays = 0, nbins = 0;

  RAVE_ASSERT((transform != NULL), "transform == NULL");
  RAVE_ASSERT((cartesian != NULL), "cartesian == NULL");
  RAVE_ASSERT((quantity != NULL), "quantity == NULL");
  RAVE_ASSERT((def != NULL), "def == NULL");

  if (!Cartesian_isTransformable(cartesian)) {
    RAVE_ERROR0("Cartesian product is not possible transform");
    goto error;
  }
  scan = RAVE_OBJECT_NEW(&PolarScan_TYPE);
  if (scan == NULL) {
    goto error;
  }
  parameter = RAVE_OBJECT_NEW(&PolarScanParam_TYPE);
  if (parameter == NULL) {
    goto error;
  }
  cparam = Cartesian_getParameter(cartesian, quantity);
  if (cparam != NULL) {
    datatype = CartesianParam_getDataType(cparam);
  }

  if (!PolarScanParam_setQuantity(parameter, quantity)) {
    goto error;
  }

  nodata = Cartesian_getNodata(cartesian);
  undetect = Cartesian_getUndetect(cartesian);

  PolarScan_setBeamwidth(scan, RadarDefinition_getBeamwidth(def));
  PolarScan_setElangle(scan, angle);
  PolarScan_setHeight(scan, RadarDefinition_getHeight(def));
  PolarScan_setLatitude(scan, RadarDefinition_getLatitude(def));
  PolarScan_setLongitude(scan, RadarDefinition_getLongitude(def));
  PolarScan_setRscale(scan, RadarDefinition_getScale(def));
  PolarScan_setRstart(scan, 0.0);
  PolarScan_setSource(scan, RadarDefinition_getID(def));
  PolarScanParam_setNodata(parameter, nodata);
  PolarScanParam_setUndetect(parameter, undetect);

  sourcepj = PolarScan_getProjection(scan);
  targetpj = Cartesian_getProjection(cartesian);

  if (!PolarScanParam_createData(parameter,
                                 RadarDefinition_getNbins(def),
                                 RadarDefinition_getNrays(def),
                                 datatype)) {
    goto error;
  }

  if (!PolarScan_addParameter(scan, parameter) ||
      !PolarScan_setDefaultParameter(scan, quantity)) {
    goto error;
  }

  nbins = RadarDefinition_getNbins(def);
  nrays = RadarDefinition_getNrays(def);

  for (ray = 0; ray < nrays; ray++) {
    for (bin = 0; bin < nbins; bin++) {
      double lon = 0.0, lat = 0.0;
      double v = 0.0L;
      if (PolarScan_getLonLatFromIndex(scan, bin, ray, &lon, &lat)) {
        double x = 0.0, y = 0.0;
        long xi = 0, yi = 0;
        if (!Projection_transformx(sourcepj, targetpj, lon, lat, 0.0, &x, &y, NULL)) {
          goto error;
        }
        xi = Cartesian_getIndexX(cartesian, x);
        yi = Cartesian_getIndexY(cartesian, y);
        Cartesian_getValue(cartesian, xi, yi, &v);
        PolarScan_setValue(scan, bin, ray, v);
      }
    }
  }

  result = RAVE_OBJECT_COPY(scan);
error:
  RAVE_OBJECT_RELEASE(sourcepj);
  RAVE_OBJECT_RELEASE(targetpj);
  RAVE_OBJECT_RELEASE(parameter);
  RAVE_OBJECT_RELEASE(cparam);
  RAVE_OBJECT_RELEASE(scan);
  return result;
}

PolarVolume_t* Transform_ctop(Transform_t* transform, Cartesian_t* cartesian, RadarDefinition_t* def, const char* quantity)
{
  unsigned int nangles = 0;
  unsigned int i = 0;
  double* angles = NULL;
  PolarVolume_t* pvol = NULL;
  PolarVolume_t* result = NULL;
  PolarScan_t* scan = NULL;

  RAVE_ASSERT((transform != NULL), "transform == NULL");
  RAVE_ASSERT((cartesian != NULL), "cartesian == NULL");
  RAVE_ASSERT((def != NULL), "def == NULL");
  RAVE_ASSERT((quantity != NULL), "quantity == NULL");

  if (!Cartesian_isTransformable(cartesian)) {
    RAVE_ERROR0("Cartesian product is not possible to transform");
    goto error;
  }

  pvol = RAVE_OBJECT_NEW(&PolarVolume_TYPE);
  if (pvol == NULL) {
    goto error;
  }
  PolarVolume_setHeight(pvol, RadarDefinition_getHeight(def));
  PolarVolume_setLatitude(pvol, RadarDefinition_getLatitude(def));
  PolarVolume_setLongitude(pvol, RadarDefinition_getLongitude(def));
  if (!PolarVolume_setSource(pvol, RadarDefinition_getID(def)) ||
      !PolarVolume_setDate(pvol, Cartesian_getDate(cartesian)) ||
      !PolarVolume_setTime(pvol, Cartesian_getTime(cartesian))) {
    goto error;
  }

  if (!RadarDefinition_getElangles(def, &nangles, &angles)) {
    goto error;
  }

  for (i = 0; i < nangles; i++) {
    scan = Transform_ctoscan(transform, cartesian, def, angles[i], quantity);
    if (scan != NULL) {
      if (!PolarVolume_addScan(pvol, scan)) {
        goto error;
      }
    } else {
      goto error;
    }
    RAVE_OBJECT_RELEASE(scan);
  }

  result = RAVE_OBJECT_COPY(pvol);
error:
  RAVE_OBJECT_RELEASE(pvol);
  RAVE_OBJECT_RELEASE(scan);
  RAVE_FREE(angles);
  return result;
}

Cartesian_t* Transform_fillGap(Transform_t* transform, Cartesian_t* cartesian)
{
  Cartesian_t* result = NULL;
  Cartesian_t* filled = NULL;
  RaveList_t* names = NULL;
  int i = 0, nrnames = 0;
  CartesianParam_t* parameter = NULL;
  CartesianParam_t* paramclone = NULL;

  RAVE_ASSERT((transform != NULL), "transform == NULL");
  if (cartesian == NULL) {
    RAVE_ERROR0("Filling gap on NULL product!?");
    goto done;
  }

  filled = RAVE_OBJECT_CLONE(cartesian);
  if (filled == NULL) {
    RAVE_ERROR0("Failed to clone product");
    goto done;
  }

  names = Cartesian_getParameterNames(filled);
  if (names == NULL) {
    RAVE_ERROR0("Failed to get parameter names");
    goto done;
  }

  nrnames = RaveList_size(names);
  for (i = 0; i < nrnames; i++) {
    parameter = Cartesian_getParameter(filled, (const char*)RaveList_get(names, i));
    if (parameter != NULL) {
      paramclone = Transform_fillGapOnParameter(transform, parameter);
      if (paramclone == NULL ||
          !Cartesian_addParameter(filled, paramclone)) {
        RAVE_ERROR0("Failed to clone of add parameter clone to result");
        goto done;
      }
    } else {
      RAVE_ERROR0("Null parameter in cartesian product");
      goto done;
    }
    RAVE_OBJECT_RELEASE(parameter);
    RAVE_OBJECT_RELEASE(paramclone);
  }

  result = RAVE_OBJECT_COPY(filled);
done:
  RaveList_freeAndDestroy(&names);
  RAVE_OBJECT_RELEASE(parameter);
  RAVE_OBJECT_RELEASE(paramclone);
  RAVE_OBJECT_RELEASE(filled);
  return result;
}

CartesianParam_t* Transform_fillGapOnParameter(Transform_t* transform, CartesianParam_t* param)
{
  CartesianParam_t* result = NULL;
  CartesianParam_t* filled = NULL;
  long nxsize = 0, nysize = 0, xsize = 0, ysize = 0, x = 0, y = 0;

  RAVE_ASSERT((transform != NULL), "transform == NULL");

  if (param == NULL) {
    RAVE_ERROR0("Filling gap on NULL param!?");
    goto done;
  }

  filled = RAVE_OBJECT_CLONE(param);
  if (filled == NULL) {
    RAVE_ERROR0("Failed to clone parameter");
    goto done;
  }
  xsize = CartesianParam_getXSize(filled);
  ysize = CartesianParam_getYSize(filled);
  nxsize = xsize - 1;
  nysize = ysize - 1;
  for (y = 1; y < nysize; y++) {
    for (x = 1; x < nxsize; x++) {
      double v1 = 0.0, v2 = 0.0, v3 = 0.0, v4 = 0.0, v5 = 0.0;
      RaveValueType t1, t2, t3, t4, t5;
      t1 = t2 = t3 = t4 = t5 = RaveValueType_NODATA;

      t1 = CartesianParam_getValue(param, x, y, &v1);
      if (t1 == RaveValueType_UNDETECT) {
        t2 = CartesianParam_getValue(param, x-1, y, &v2);
        t3 = CartesianParam_getValue(param, x+1, y, &v3);
        t4 = CartesianParam_getValue(param, x, y-1, &v4);
        t5 = CartesianParam_getValue(param, x, y+1, &v5);
        if (t2 == RaveValueType_DATA && t3 == RaveValueType_DATA && t4 == RaveValueType_DATA && t5 == RaveValueType_DATA) {
          v1 = (v2 + v3 + v4 + v5) / 4.0;
          CartesianParam_setValue(filled, x, y, v1);
        } else {
          CartesianParam_setValue(filled, x, y, v1);
        }
      } else {
        CartesianParam_setValue(filled, x, y, v1);
      }
    }
  }
  result = RAVE_OBJECT_COPY(filled);
done:
  RAVE_OBJECT_RELEASE(filled);
  return result;
}

CartesianParam_t* Transform_accumulate(Transform_t* self, CartesianParam_t* param, double zr_a, double zr_b)
{
  CartesianParam_t* result = NULL;
  RaveField_t *nd = NULL, *dd = NULL, *cd = NULL, *sd = NULL;
  long xsize = 0, ysize = 0;
  RAVE_ASSERT((self != NULL), "self == NULL");
  if (param == NULL) {
    RAVE_ERROR0("CartesianParam == NULL");
    return NULL;
  }

  xsize = CartesianParam_getXSize(param);
  ysize = CartesianParam_getXSize(param);

  nd = RAVE_OBJECT_NEW(&RaveField_TYPE);
  dd = RAVE_OBJECT_NEW(&RaveField_TYPE);
  cd = RAVE_OBJECT_NEW(&RaveField_TYPE);
  sd = RAVE_OBJECT_NEW(&RaveField_TYPE);
  if (nd == NULL || dd == NULL || cd == NULL || sd == NULL ||
      !RaveField_createData(nd, xsize, ysize, RaveDataType_SHORT) ||
      !RaveField_createData(dd, xsize, ysize, RaveDataType_DOUBLE) ||
      !RaveField_createData(cd, xsize, ysize, RaveDataType_SHORT) ||
      !RaveField_createData(sd, xsize, ysize, RaveDataType_DOUBLE)) {
    RAVE_ERROR0("Memory allocation problems");
    goto done;
  }

done:
  RAVE_OBJECT_RELEASE(nd);
  RAVE_OBJECT_RELEASE(dd);
  RAVE_OBJECT_RELEASE(cd);
  RAVE_OBJECT_RELEASE(sd);
  return result;
}

/*@} End of Interface functions */

RaveCoreObjectType Transform_TYPE = {
    "Transform",
    sizeof(Transform_t),
    Transform_constructor,
    Transform_destructor
};