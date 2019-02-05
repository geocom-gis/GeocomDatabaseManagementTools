# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
# Name:        gc_arcsde_mssql_set_sp_indexes_geometry
# Purpose:
# Example:     cmd --> gc_arcsde_mssql_set_sp_indexes_geometry.py "C:/temp/vsdev4015_TEST_H_1_TEST_H_1_OWNER.sde" "vsdev4015" "sqlserver" "706490.780012436" "226923.969956476" "708124.09003469" "229125.969972171" "LOW" "LOW" "LOW" "LOW" "16"
#
# Author:      Geocom Informatik AG
#
# Created:     01.04.2018
# Copyright:   (c) Geocom Informatik AG 2018
#-------------------------------------------------------------------------------

import sys, pypyodbc, gc_sql_utils, arcpy
from arcpy import env
sys.path.append("/py")

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
'''-------------------------------------------------------------------------------
# Create Connection to MSSQL-Server with pypyodbc
-------------------------------------------------------------------------------'''
def createConn(instance,database,dbms_admin,dbms_admin_pwd):
    try:
        if dbms_admin_pwd != '':
            cnnctnstring = 'DRIVER={driver};SERVER={instance};DATABASE={db};UID={dbms_admin};PWD={dbms_admin_pwd}'.format(driver='SQL Server',instance=instance,db=database,dbms_admin=dbms_admin,dbms_admin_pwd=dbms_admin_pwd)
        else:
            cnnctnstring = 'DRIVER={driver};SERVER={instance};DATABASE={db};Trusted_Connection=Yes'.format(driver='SQL Server',instance=instance,db=database)
        cnnctn = pypyodbc.connect(cnnctnstring, autocommit=True)
        cursor = cnnctn.cursor()
        return cursor
    except pypyodbc.Error, msg:
        message(msg,2)
    except Exception as e:
        message(e.args[0],2)
'''-------------------------------------------------------------------------------
# Execute T-SQL
-------------------------------------------------------------------------------'''
def executeSQL(sql,instance,database,dbms_admin,dbms_admin_pwd):
    cursor = createConn(instance,database,dbms_admin,dbms_admin_pwd)
    try:
        cursor.execute(sql)
    except pypyodbc.Error, msg:
        message(msg,2)
	pass
'''-------------------------------------------------------------------------------
# Execute Select Statements with result
-------------------------------------------------------------------------------'''
def select(sql,instance,database,dbms_admin,dbms_admin_pwd):
    cursor = createConn(instance,database,dbms_admin,dbms_admin_pwd)
    try:
        cursor.execute(sql)
        #message(cursor.fetchone())
    except pypyodbc.Error, msg:
        message(msg,2)
    return cursor.fetchone()
'''-------------------------------------------------------------------------------
# Get informations about the workspace
-------------------------------------------------------------------------------'''
def getinstance(workspace):
    # Create a Describe object for an SDE database
    desc = arcpy.Describe(workspace)
    conn = desc.connectionProperties.instance
    instance = conn.split(':')
    #message(instance[2])
    return instance[2]
'''-------------------------------------------------------------------------------
# MAIN
-------------------------------------------------------------------------------'''
def main(workspace,dbms_admin_pwd,fc,xmin,ymin,xmax,ymax,autogrid,l1,l2,l3,l4,cells,compression):

    message(' ')

    showsqlstatment = False

    # Check if SA password is provided
    if dbms_admin_pwd != '':
        dbms_admin = 'sa'
    else:
        message('No SA password provided, trying with OS-Authentication! (Windows-user has to be at least db-owner)\n',1)
        dbms_admin = ''

    # Set local variables
    database = ''
    dbschema = ''
    #tables = []
    #indexes = {}
    defaultxmin = xmin.replace(',', '.')
    defaultymin = ymin.replace(',', '.')
    defaultxmax = xmax.replace(',', '.')
    defaultymax = ymax.replace(',', '.')
    # End local variables

    env.workspace = workspace

    instance = getinstance(workspace)
    message('Got the following instance: ' + instance + '\n')

    # check if 'Use only default extent' was checked
    # if defaultextent == 'true':
        # if defaultxmin != '' and defaultymin != '' and defaultxmax != '' and defaultymax != '':
            # message('Use default extent for all feature classes!\n')
            # extentok = True
        # else:
            # message('No correct spatial extent provided. Do nothing!\n',1)
            # sys.exit()
    # else:
        # extentok = False

    # set Data compression - compression = 'PAGE' # DATA_COMPRESSION = {NONE | ROW | PAGE}
    compression = compression


    for dirpath, datasetnames, tablenames in arcpy.da.Walk(workspace,datatype='FeatureClass'):
        for table in tablenames:

            tables = []
            indexes = {}

            # with this option one could get the info if a table has a spatial index, BUT: performance would then not be acceptable!!
            #desc = arcpy.Describe(table)
            #hasspindex = desc.hasSpatialIndex

            database = table.split('.')[0]
            dbschema = table.split('.')[1]
            tablename = table.split('.')[2]

            tables.append(tablename)

            xmin = defaultxmin
            ymin = defaultymin
            xmax = defaultxmax
            ymax = defaultymax

            # if extentok == False:
                # desc = arcpy.Describe(table)
                # # check if table has a valid extent, if so then set value
                # if str(desc.extent.XMin) != 'nan' or str(desc.extent.YMin) != 'nan' or str(desc.extent.XMax) != 'nan' or str(desc.extent.YMax) != 'nan':
                    # xmin = desc.extent.XMin
                    # ymin = desc.extent.YMin
                    # xmax = desc.extent.XMax + 1 # plus 1 because the value of parameter 'xmax' of CREATE SPATIAL INDEX must be greater than the value of parameter 'xmin'
                    # ymax = desc.extent.YMax + 1 # # plus 1 because the value of parameter 'ymax' of CREATE SPATIAL INDEX must be greater than the value of parameter 'ymin'
                # # otherwise check the default values and set them
                # elif defaultxmin != '' and defaultymin != '' and defaultxmax != '' and defaultymax != '':
                    # message('No feature class extent found for table \"{tablename}\", use provided default extent'.format(tablename=tablename))
                    # xmin = defaultxmin
                    # ymin = defaultymin
                    # xmax = defaultxmax
                    # ymax = defaultymax
                # # if table has no extent and no default extent is provided then throw message and exit
                # else:
                    # message('No correct spatial extent provided for table \"{tablename}\". Please check values for XMin, YMin, XMax, YMax'.format(tablename=tablename),1)
                    # break
            # else:
                # xmin = defaultxmin
                # ymin = defaultymin
                # xmax = defaultxmax
                # ymax = defaultymax

            '''
            tableinfo = {}
            key = tablename
            tableinfo.setdefault(key, [])
            tableinfo[key].append(xmin)
            tableinfo[key].append(ymin)
            tableinfo[key].append(xmax)
            tableinfo[key].append(ymax)
            '''


            # get the id and the EVW of the table
            sql = gc_sql_utils.getTableId.format(tablename=tablename)
            table = select(sql,instance,database,dbms_admin,dbms_admin_pwd)

            # if table is not registered in 'sde_table_registry' then the table is possibly a view
            if table:
                # if the table has an EVW registered (means it is registered as versioned), then append Add-tablename to array, otherwise not
                if str(table[1]) != 'None':
                    # append table name to array
                    tables.append('a' + str(table[0]))
                    # tableinfo[key].append('a' + str(table[0]))
                    # tableversionname = 'a' + str(table[0])
                    # message(tableinfo)
            else:
                message('No table info found for table \"{tablename}" (perhaps it is a view)'.format(tablename=tablename),1)

            # iterate array of feature class and Add-table to get the indexnames
            for t in tables:
                # get the index names for tables
                sql = gc_sql_utils.getSpIndexName.format(tablename=t)
                queryresult = select(sql,instance,database,dbms_admin,dbms_admin_pwd)

                # if no GEOMETRY spatial index exists, then the result of the above query will be NULL - in this case, the spatial index can't be changed
                if queryresult:
                    idxname = str(queryresult[0])
                    # tables.append(tableidxname)
                    # tableinfo[key].append(tableidxname)
                    indexes[str(t)] = idxname
                else:
                    message('No GEOMETRY spatial index found for \"{tablename}\"'.format(tablename=tablename),1)
                    break

            # iterate dictionary and change spatial index for each table/spatial index
            for key,val in indexes.items():
                try:
                    # change spatial indexes for tables
                    # if autogrid = true then
                    if autogrid == 'true':
                        message('--- change autogrid-index \"{idx}\" for table \"{table}\" with extent \"{xmin}, {ymin}, {xmax}, {ymax}\"'.format(table=key,idx=val,xmin=xmin,ymin=ymin,xmax=xmax,ymax=ymax))
                        sql = gc_sql_utils.changeSpIndexAuto.format(idxname=val,dbschema=dbschema,tablename=key,xmin=xmin,ymin=ymin,xmax=xmax,ymax=ymax,cells=cells,compression=compression)
                    # if manual grid (autogrid = false)
                    else:
                        message('--- change manualgrid-index \"{idx}\" for table \"{table}\" with extent \"{xmin}, {ymin}, {xmax}, {ymax}\"'.format(table=key,idx=val,xmin=xmin,ymin=ymin,xmax=xmax,ymax=ymax))
                        sql = gc_sql_utils.changeSpIndex.format(idxname=val,dbschema=dbschema,tablename=key,xmin=xmin,ymin=ymin,xmax=xmax,ymax=ymax,l1=l1,l2=l2,l3=l3,l4=l4,cells=cells,compression=compression)
                    if showsqlstatment == True:
                        message(sql)
                    executeSQL(sql,instance,database,dbms_admin,dbms_admin_pwd)
                except Exception as e:
                    message('The following sql statement posed problems: \n' + sql)
                    message(e.args[0],2)


            xmin = ''
            ymin = ''
            xmax = ''
            ymax = ''


    message(' ')

'''-------------------------------------------------------------------------------
# START script
-------------------------------------------------------------------------------'''
# This test allows the script to be used from the operating
# system command prompt (stand-alone), in a Python IDE,
# as a geoprocessing script tool, or as a module imported in
# another script
if __name__ == '__main__':
    # Arguments are optional
    argv = tuple(arcpy.GetParameterAsText(i)
        for i in range(arcpy.GetArgumentCount()))
    main(*argv)
