/* --------------------------------------------------------------------
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
/**
 * Adaptor for cartesian ODIM H5 files.
 * This object supports \ref #RAVE_OBJECT_CLONE.
 * @file
 * @author Anders Henja (Swedish Meteorological and Hydrological Institute, SMHI)
 * @date 2010-09-09
 */
#ifndef CARTESIAN_ODIM_ADAPTOR_H
#define CARTESIAN_ODIM_ADAPTOR_H
#include "rave_object.h"
#include "hlhdf.h"
#include "cartesian.h"

/**
 * Defines the odim h5 adaptor for cartesian products
 */
typedef struct _CartesianOdimAdaptor_t CartesianOdimAdaptor_t;

/**
 * Type definition to use when creating a rave object.
 */
extern RaveCoreObjectType CartesianOdimAdaptor_TYPE;

/**
 * Fills a HL nodelist with information from a cartesian product.
 * @param[in] self - self
 * @param[in] nodelist - the node list
 * @param[in] cartesian - the cartesian product
 * @returns 1 on success, 0 otherwise
 */
int CartesianOdimAdaptor_fillImageInformation(CartesianOdimAdaptor_t* self, HL_NodeList* nodelist, Cartesian_t* cartesian);

#endif /* CARTESIAN_ODIM_ADAPTOR_H */
