# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
# Name:         gc_egdb_set_perm
# Purpose:     This script changes the permissions for all Datasets,
#              FeatureClasses and Tables for the given roles (read/write)
#              Only the workpaket-tables are treated differently
#
# Author:      Geocom Informatik AG
#
# Created:     01.04.2018
# Copyright:   (c) Geocom Informatik AG 2018
#-------------------------------------------------------------------------------

import arcpy
from arcpy import env

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


def changePrivileges(dataset,role,view,write):
    try:
        arcpy.ChangePrivileges_management(dataset, role, view, write)
    except:
        for i in range(arcpy.GetMessageCount()):
            message(i,2)


def main(workspace,readRole,writeRole):
    env.workspace = workspace

    message("Setting permissions for data from \"" + workspace + "\"")

    for dataset in arcpy.ListDatasets():
        message("Setting permissions for dataset: " + "\"" + dataset + "\"")
        changePrivileges(dataset,readRole,"GRANT","AS_IS")
        changePrivileges(dataset,writeRole,"GRANT","GRANT")

    for fc in arcpy.ListFeatureClasses():
        message("Setting permissions for FeatureClass: " + "\"" + fc + "\"")
        changePrivileges(fc,readRole,"GRANT","AS_IS")
        changePrivileges(fc,writeRole,"GRANT","GRANT")

    for table in arcpy.ListTables():
        if 'GN_WORKPACKET' in table.upper():
            message("Setting permissions for GN_WORKPACKET table")
            changePrivileges(table,readRole,"GRANT", "GRANT")
            changePrivileges(table,writeRole,"GRANT","GRANT")
        elif 'GN_USER' in table.upper():
            message("Setting permissions for GN_USER table")
            changePrivileges(table,readRole,"GRANT","AS_IS")
            changePrivileges(table,writeRole,"GRANT","AS_IS")
        else:
            message("Setting permissions for table: " + "\"" + table + "\"")
            changePrivileges(table,readRole,"GRANT","AS_IS")
            changePrivileges(table,writeRole,"GRANT","GRANT")


# This test allows the script to be used from the operating
# system command prompt (stand-alone), in a Python IDE,
# as a geoprocessing script tool, or as a module imported in
# another script
if __name__ == '__main__':
    # Arguments are optional
    argv = tuple(arcpy.GetParameterAsText(i)
        for i in range(arcpy.GetArgumentCount()))
    main(*argv)
    #workspace = r'C:\geodb-testrun\sql\GNS_TESTING_SQL_OWNER.sde'
    #readRole = "R_SDE_VIEWER"
    #writeRole = "R_SDE_EDITOR"
    #main(workspace, readRole, writeRole)