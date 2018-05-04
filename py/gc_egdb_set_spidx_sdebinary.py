# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
# Name:        gc_egdb_set_spidx_sdebinary
# Purpose:
#
# Author:      Geocom Informatik AG
#
# Created:     01.04.2018
# Copyright:   (c) Geocom Informatik AG 2018
#-------------------------------------------------------------------------------


import arcpy

import gc_egdb_set_spidx_av
import gc_egdb_set_spidx_fwa
import gc_egdb_set_spidx_ele
import gc_egdb_set_spidx_gas
import gc_egdb_set_spidx_was
import gc_egdb_set_spidx_sew
import gc_egdb_set_spidx_utils

currentParam =[]
qualif=""

spUtil = gc_egdb_set_spidx_utils.Spatial_Idx_Util("MyObject")



if __name__ == '__main__':
    ws = arcpy.GetParameterAsText(0)
    model = arcpy.GetParameterAsText(1)
    qualif = spUtil.GetQualifier(ws)

    if str(model).startswith("AV"):
        currentParam= gc_egdb_set_spidx_av.def_array
    if str(model).startswith("ELE"):
        currentParam=gc_egdb_set_spidx_ele.def_array
    if str(model).startswith("FWA"):
        currentParam=gc_egdb_set_spidx_fwa.def_array
    if str(model).startswith("GAS"):
        currentParam=gc_egdb_set_spidx_gas.def_array
    if str(model).startswith("SEW"):
        currentParam=gc_egdb_set_spidx_sew.def_array
    if str(model).startswith("WAS"):
        currentParam=gc_egdb_set_spidx_was.def_array

    if len(currentParam)>0:
        spUtil.SetSpatialIndexDefArray(ws, currentParam, qualif)
    else:
        spUtil.SetDefaultSpatialIndex(ws)
    arcpy.AddMessage("Fertig")


