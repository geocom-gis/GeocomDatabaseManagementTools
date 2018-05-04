# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
# Name:        gc_arcsde_create_copy
# Purpose:     creates
#
# Author:      Geocom Informatik AG
#
# Created:     01.04.2018
# Copyright:   (c) Geocom Informatik AG 2018
#-------------------------------------------------------------------------------

import gc_arcsde_createsde_roles_users_mssql
import gc_copy_gdb2gdb
import  gc_egdb_set_perm
import gc_egdb_reg_as_ver
import gc_egdb_set_spidx_geom_mssql

def main(instance,database,dbms_admin_pwd,gdb_admin_pwd,dbsize,dbgrowth,dblogsize,dbloggrowth,recoverymodel,dbowner_pwd,dbeditor_pwd,dbviewer_pwd,license,out_folder_path,spatial_type,ingdb,xmin,ymin,xmax,ymax,l1,l2,l3,l4,cells):

    ownerconnfile = gc_arcsde_createsde_roles_users_mssql.main(instance,database,dbms_admin_pwd,gdb_admin_pwd,dbsize,dbgrowth,dblogsize,dbloggrowth,recoverymodel,dbowner_pwd,dbeditor_pwd,dbviewer_pwd,license,out_folder_path,spatial_type)

    gc_copy_gdb2gdb.main(ingdb,ownerconnfile)

     gc_egdb_set_perm.main(ownerconnfile,"R_SDE_VIEWER","R_SDE_EDITOR")

    gc_egdb_reg_as_ver.main(ownerconnfile,"WITH TABLES","GN")

    if spatial_type == "GEOMETRY":
        gc_egdb_set_spidx_geom_mssql.main(ownerconnfile,dbms_admin_pwd,fc,xmin,ymin,xmax,ymax,l1,l2,l3,l4,cells)


if __name__ == '__main__':
    # Arguments are optional
    argv = tuple(arcpy.GetParameterAsText(i)
        for i in range(arcpy.GetArgumentCount()))
    main(*argv)
