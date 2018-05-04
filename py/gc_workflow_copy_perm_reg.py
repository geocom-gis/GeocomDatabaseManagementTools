# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
# Name:        gc_workflow_copy_perm_reg
# Purpose:     creates
#
# Author:      Geocom Informatik AG
#
# Created:     01.04.2018
# Copyright:   (c) Geocom Informatik AG 2018
#-------------------------------------------------------------------------------

import gc_copy_gdb2gdb
import  gc_egdb_set_perm
import gc_egdb_reg_as_ver


def main(ingdb,outgdb):

    gc_copy_gdb2gdb.main(ingdb,outgdb)

    gc_egdb_set_perm.main(outgdb,"R_SDE_VIEWER","R_SDE_EDITOR")

    gc_egdb_reg_as_ver.main(outgdb,"ONLY_FEATURECLASSES","")


if __name__ == '__main__':
    # Arguments are optional
    argv = tuple(arcpy.GetParameterAsText(i)
        for i in range(arcpy.GetArgumentCount()))
    main(*argv)
