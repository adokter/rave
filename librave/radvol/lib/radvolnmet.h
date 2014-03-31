/* --------------------------------------------------------------------
Copyright (C) 2012 Institute of Meteorology and Water Management -
National Research Institute, IMGW-PIB

This file is part of Radvol-QC package.

Radvol-QC is free software: you can redistribute it and/or modify
it under the terms of the GNU Lesser General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

Radvol-QC is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public License
along with Radvol-QC.  If not, see <http://www.gnu.org/licenses/>.
------------------------------------------------------------------------*/
/**
 * Radvol-QC algorithms for non-meteorological echoes removal.
 * @file radvolnmet.h
 * @author Katarzyna Osrodka (Institute of Meteorology and Water Management, IMGW-PIB)
 * @date 2013
 */
#ifndef RADVOLNMET_H
#define	RADVOLNMET_H
#include "rave_object.h"
#include "polarvolume.h"
#include "polarscan.h"

/**
 * Defines a RadvolNmet
 */
typedef struct _RadvolNmet_t RadvolNmet_t;

/**
 * Type definition to use when creating a rave object.
 */
extern RaveCoreObjectType RadvolNmet_TYPE;

/**
 * Runs algorithm for non-meteorological echoes removal and quality characterization with parameters from XML file
 * @param scan - input polar scan
 * @param paramFileName - name of XML file with parameters (otherwise default values are applied)
 * @returns 1 upon success, otherwise 0
 */
int RadvolNmet_nmetRemoval_scan(PolarScan_t* scan, char* paramFileName);

/**
 * Runs algorithm for non-meteorological echoes removal and quality characterization with parameters from XML file
 * @param pvol - input polar volume
 * @param paramFileName - name of XML file with parameters (otherwise default values are applied)
 * @returns 1 upon success, otherwise 0
 */
int RadvolNmet_nmetRemoval_pvol(PolarVolume_t* pvol, char* paramFileName);

#endif	/* RADVOLNMET_H */
