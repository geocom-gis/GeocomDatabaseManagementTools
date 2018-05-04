# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Name:        gc_copy_gdb2gdb
# Purpose:
#
# Author:      Geocom Informatik AG
#
# Created:     1.04.2018
# Copyright:   (c) Geocom Informatik AG 2018
#-------------------------------------------------------------------------------

import arcpy
from arcpy import env
import os

def message(messageText, severity=0):
        '''zur Ausgabe auf der Konsole'''
        #print messageText
        '''zur Ausgabe in ArcGIS'''
        if severity == 0:
            arcpy.AddMessage(messageText)
        if severity == 1:
            arcpy.AddWarning(messageText)
        if severity == 2:
            arcpy.AddError(messageText)

def main(in_data,out_data):

    # Overwriting the output, if it already exist
    env.overwriteOutput = True
    env.workspace = in_data

    for dataset in arcpy.ListDatasets():
        try:
            message("Copying dataset " + "\"" + dataset + "\"" + " to " + out_data,0)
            arcpy.Copy_management(dataset, out_data + os.sep + dataset)
        except arcpy.ExecuteError:
            message(arcpy.GetMessages(2),2)

    for fc in arcpy.ListFeatureClasses():
        try:
            message("Copying feature class " + "\"" + fc + "\"" + " to " + out_data,0)
            arcpy.Copy_management(fc, out_data + os.sep + fc)
        except arcpy.ExecuteError:
           message(arcpy.GetMessages(2),2)

    for table in arcpy.ListTables():
        try:
            message("Copying table " + "\"" + table + "\"" + " to " + out_data,0)
            arcpy.Copy_management(table, out_data + os.sep + table)
        except arcpy.ExecuteError:
            message(arcpy.GetMessages(2),2)

    try:
        del dataset, fc, table
    except:
        pass

# This test allows the script to be used from the operating
# system command prompt (stand-alone), in a Python IDE,
# as a geoprocessing script tool, or as a module imported in
# another script
if __name__ == '__main__':
    # Arguments are optional
    argv = tuple(arcpy.GetParameterAsText(i)
        for i in range(arcpy.GetArgumentCount()))
    main(*argv)
