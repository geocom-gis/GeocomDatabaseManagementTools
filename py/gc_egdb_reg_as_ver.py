# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Name:         gc_egdb_reg_as_ver
# Purpose:      This script register all FeatureClasses and Tables in a given SDE as versioned.
#               Defined exceptions are not registered as versioned (for example GN-tables)
#
# Author:       Geocom Informatik AG
#
# Created:      01.04.2018
# Copyright:    (c) Geocom Informatik AG
# -----------------------------------------------------------------------------

import arcpy
import re


# -----------------------------------------------------------------------------
def message(message_text, severity=0):
    """
    Zur Ausgabe auf der Konsole
    Zur Ausgabe in ArcGIS
    :param messageText:
    :param severity 0 = INFO, 1 = WARNING, 2 = ERROR
    :return:
    """
    if severity == 0:
        arcpy.AddMessage(message_text)
    if severity == 1:
        arcpy.AddWarning(message_text)
    if severity == 2:
        arcpy.AddError(message_text)


# -----------------------------------------------------------------------------
def checkexception(inputobject, exceptionlist):
    """
    Check if the table is an exception according the exceptionlist
    :param inputobject:
    :param exceptionlist:
    :return:
    """
    featurename = (inputobject.split('.', ))[-1]
    # Pruefe, ob das Inputobjekt versioniert werden soll oder nicht
    for exception in exceptionlist:
        if re.match(exception, featurename, re.IGNORECASE):
            # register = 0
            return 0
    return 1


# -----------------------------------------------------------------------------
def getcurrentrelease(workspace):
    """
    Get informations about the workspace
    :param workspace:
    :return:
    """
    # Create a Describe object for an SDE database
    desc = arcpy.Describe(workspace)
    iscurrent = desc.currentRelease
    gdbversion = desc.release
    #message(gdbversion)
    return (iscurrent, gdbversion)


# -----------------------------------------------------------------------------
def getarcgisversion(gdbversion):
    '''
    Create geodatabase version mapping table
    :param gdbversion:
    :return:
    '''
    # For a geodatabase workspace, returns the geodatabase release value.
    # Below is the mapping of geodatabase release values to ArcGIS version numbers.
    # For more information see: http://desktop.arcgis.com/en/arcmap/latest/analyze/arcpy-functions/workspace-properties.htm
    mappingtable = {'2,2,0': '9.2', '2,3,0': '9.3, 9.3.1', '3,0,0': '10.0, 10.1'}
    arcgisversion = mappingtable.get(gdbversion)
    return arcgisversion


# -----------------------------------------------------------------------------
def licence_check(workspace):
    """
    Check the current licence version
    :param workspace:
    :return:
    """
    iscurrent, gdbversion = getcurrentrelease(workspace)
    arcgisversion = getarcgisversion(gdbversion)
    if not iscurrent:
        message('''
            The geodatabase version \"{arcgisversion}\" does not exactly match the version of the desktop you are currently using!
            Please check if you should upgrade the geodatabase first.
            To administer a geodatabase we recommend to use the same versions on both sides - desktop and geodatabase.
            '''.format(arcgisversion=arcgisversion), 1)


# -----------------------------------------------------------------------------
def create_datasets_list():
    '''
    Create list with datasets from workspace
    :return:
    '''
    dataset_list = []
    for dataset in arcpy.ListDatasets("*", "Feature"):
        dataset_list.append(dataset)

    return dataset_list


# -----------------------------------------------------------------------------
def create_featureclasses_list():
    '''
    Create list with feature classes from workspace
    :return:
    '''
    feature_class_list = []
    for dataset in arcpy.ListFeatureClasses(""):
        feature_class_list.append(dataset)

    return feature_class_list


# -----------------------------------------------------------------------------
def create_tables_list(datatypes):
    '''
    Create list with tables from workspace
    :param datatypes:
    :return:
    '''
    table_List = []
    if datatypes.upper() == 'WITH_TABLES':
        for table in arcpy.ListTables(""):
            table_List.append(table)
	
    return table_List


# -----------------------------------------------------------------------------
def register_db_as_versioned(ds_list, exception_list):
    """
    Register the list as versioned in the workspace
    :param ds_list:
    :param exception_list:
    :return:
    """
    for i, ds in enumerate(ds_list):
        registerdataset = checkexception(ds, exception_list)
        if not registerdataset == 1:
            message(("--- exception-Rule! Do no register: " + "\"" + ds + "\""), 0)
        else:
            desc = arcpy.Describe(ds)
            if not desc.isVersioned:
                try:
                    message(("registering as versioned: " + "\"" + ds + "\""), 0)
                    arcpy.RegisterAsVersioned_management(ds, "NO_EDITS_TO_BASE")
                except Exception as ex:
                    message(("problem with registering: " + "\"" + ds + "\"" + '\n' + arcpy.GetMessages(2)), 2)
                    message(ex.message)
            else:
              message(("--- already registered as versioned: " + "\"" + ds + "\""), 0)


# -----------------------------------------------------------------------------
# MAIN
# -----------------------------------------------------------------------------
def main(workspace, datatypes, exceptionlist):
    """
    Workflow to register the datasets, featue classes and tables as versioned
    :param workspace:
    :param datatypes:
    :param exceptionlist:
    :return:
    """
    arcpy.env.workspace = workspace

    # Check if version of geodatabase and desktop match, if not, show message
    licence_check(workspace)

    # Create List for all datasets, feature classes and may tables
    ds_list = []
    ds_list.extend(create_datasets_list())
    ds_list.extend(create_featureclasses_list())
    ds_list.extend(create_tables_list(datatypes))

    # Delete the Workspace Cache for more info check
    # https://pro.arcgis.com/de/pro-app/tool-reference/data-management/clear-workspace-cache.htm
    arcpy.ClearWorkspaceCache_management()

    register_db_as_versioned(ds_list, exceptionlist)


# This test allows the script to be used from the operating
# system command prompt (stand-alone), in a Python IDE,
# as a geoprocessing script tool, or as a module imported in
# another script
# -----------------------------------------------------------------------------
if __name__ == '__main__':
    argv = tuple(arcpy.GetParameterAsText(i) for i in range(arcpy.GetArgumentCount()))
    try:
        main(*argv)
    except Exception as exc:
        arcpy.AddMessage(exc.message)
