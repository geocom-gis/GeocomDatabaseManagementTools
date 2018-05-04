# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Name:        gc_arcsde_create_conn_files
# Purpose:
#
# Author:      Geocom Informatik AG
#
# Created:     1.04.2018
# Copyright:   (c) Geocom Informatik AG 2018
#-------------------------------------------------------------------------------

import os, sys, arcpy, datetime

'''-------------------------------------------------------------------------------
# Create User Connection Files
-------------------------------------------------------------------------------'''
def main(instance,database_type,database,account_authentication,role,dbuser_pwd,out_folder_path):
    # Local variables
    if role == 'sde':
        dbuser_name = 'SDE'
    else:
        dbuser_name = database.upper() + '_' + role.upper()

    #if dbuser_pwd != '#':
    #    dbuser_pwd = database.lower() + '_' + role.upper() + '_' + str(datetime.datetime.now().year)
    #    arcpy.AddMessage(dbuser_pwd)

    instance_temp = instance.replace("\\","_")
    instance_temp = instance_temp.replace("/","_")
    instance_temp = instance_temp.replace(":","_")
    Conn_File_NameT = instance_temp + "." + database + "." + dbuser_name
    Connection_File_Name = Conn_File_NameT + ".sde"
    Connection_File_Name_full_path = out_folder_path + os.sep + Conn_File_NameT + ".sde"

    # Check for the .sde file and delete it if present
    arcpy.env.overwriteOutput=True
    if os.path.exists(Connection_File_Name_full_path):
        os.remove(Connection_File_Name_full_path)

    try:
        arcpy.AddMessage("Creating Database Connection File...")
        # Process: Create Database Connection File...
        # Usage:  out_file_location, out_file_name, DBMS_TYPE, instnace, account_authentication, username, password, database, save_username_password(must be true)
        arcpy.CreateDatabaseConnection_management(out_folder_path=out_folder_path, out_name=Connection_File_Name, database_platform=database_type, instance=instance, database=database, account_authentication=account_authentication, username=dbuser_name, password=dbuser_pwd, save_user_pass="TRUE")
        for i in range(arcpy.GetMessageCount()):
            if "000565" in arcpy.GetMessage(i):   #Check if database connection was successful
                arcpy.AddReturnMessage(i)
                arcpy.AddMessage("++++++++++++++++++")
                arcpy.AddMessage("Exiting!!")
                arcpy.AddMessage("++++++++++++++++++")
                sys.exit(3)
            else:
                arcpy.AddReturnMessage(i)
        arcpy.AddMessage("++++++++++++++++++")
    except:
        for i in range(arcpy.GetMessageCount()):
            arcpy.AddReturnMessage(i)
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