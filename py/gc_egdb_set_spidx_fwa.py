# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
# Name:        gc_egdb_set_spidx_fwa
# Purpose:
#
# Author:      Geocom Informatik AG
#
# Created:     01.04.2018
# Copyright:   (c) Geocom Informatik AG 2018
#-------------------------------------------------------------------------------





# Variables

def_array=[]

def_array.append(['/DIV/DIMENSION' , 'Polygon' , [1000]])
def_array.append(['/DIV/KONSTRUKTION_FLA' , 'Polygon' , [1000]])
def_array.append(['/DIV/KONSTRUKTION_LIN' , 'Polyline' , [1000]])
def_array.append(['/DIV/KONSTRUKTION_PKT' , 'Point' , [500]])

def_array.append(['/FWA/FWA_STGLTG_ARMATUR' , 'Point' , [250]])
def_array.append(['/FWA/FWA_STGLTG_LEITUNG' , 'Polyline' , [200]])
def_array.append(['/FWA/FWA_DEHNZONE' , 'Polygon' , [200]])
def_array.append(['/FWA/FWA_MESSPUNKT' , 'Point' , [1000]])
def_array.append(['/FWA/FWA_MESSLEITUNG' , 'Polyline' , [200]])
def_array.append(['/FWA/FWA_KABELPUNKT' , 'Point' , [200]])
def_array.append(['/FWA/FWA_KABEL' , 'Polyline' , [250]])
def_array.append(['/FWA/FWA_BAUWERK_LIN' , 'Polyline' , [500]])
def_array.append(['/FWA/FWA_BAUWERK_FLA' , 'Polygon' , [500]])
def_array.append(['/FWA/FWA_BAUWERK' , 'Point' , [500]])
def_array.append(['/FWA/FWA_SCHUTZMASSNAHME' , 'Polygon' , [1000]])
def_array.append(['/FWA/FWA_LEITUNG' , 'Polyline' , [200]])
def_array.append(['/FWA/FWA_UEBERGABEPUNKT' , 'Point' , [1000]])
def_array.append(['/FWA/FWA_LEITUNGSPUNKT' , 'Point' , [1000]])
def_array.append(['/FWA/FWA_EINBAUTE' , 'Point' , [1000]])
def_array.append(['/FWA/FWA_ABGANG' , 'Point' , [1000]])
def_array.append(['/FWA/FWA_FORMSTUECK' , 'Point' , [250]])
def_array.append(['/FWA/FWA_ARMATUR' , 'Point' , [250]])
def_array.append(['/FWA/FWA_STATIKPUNKT' , 'Point' , [500]])
def_array.append(['/FWA/FWA_TRASSEPUNKT' , 'Point' , [500]])
def_array.append(['/FWA/FWA_TRASSE' , 'Polyline' , [250]])
def_array.append(['/FWA/FWA_TOPO_LIN' , 'Polyline' , [250]])
def_array.append(['/FWA/FWA_SCHADEN' , 'Point' , [500]])
def_array.append(['/FWA/FWA_NET_Junctions' , 'Point' , [200]])
def_array.append(['/FWA/FWA_LINIE' , 'Polyline' , [500]])
def_array.append(['/FWA/FWA_SCHADEN' , 'Point' , [500]])
def_array.append(['/FWA/FWA_NET_Junctions' , 'Point' , [200]])
def_array.append(['/FWA/FWAT_HOEHE_ABGANG' , 'Polyline' , [500]])
def_array.append(['/FWA/FWAT_HOEHE_ARMATUR' , 'Polyline' , [500]])
def_array.append(['/FWA/FWAT_HOEHE_UEBERGABEPUNKT' , 'Polyline' , [500]])
def_array.append(['/FWA/FWAT_HOEHE_FORMSTUECK' , 'Polyline' , [500]])
def_array.append(['/FWA/FWAT_HOEHE_STATIKPUNKT' , 'Polyline' , [500]])
def_array.append(['/FWA/FWAT_HOEHE_LEITUNGSPUNKT' , 'Polyline' , [500]])
def_array.append(['/FWA/FWAT_NAME_BAUWERK' , 'Polyline' , [500]])
def_array.append(['/FWA/FWAT_TEXT' , 'Polyline' , [500]])
def_array.append(['/FWA/FWAT_TXT_TRASSE' , 'Polyline' , [500]])
def_array.append(['/FWA/FWAT_STELLUNG_ARMATUR' , 'Polyline' , [500]])
def_array.append(['/FWA/FWAT_NR_UEBERGABEPUNKT' , 'Polyline' , [1000]])
def_array.append(['/FWA/FWAT_BEM_LEITUNG' , 'Polyline' , [500]])
def_array.append(['/FWA/FWAT_MAT_DURCH_LEITUNG' , 'Polyline' , [500]])
def_array.append(['/FWA/FWAA_d7df3bc73a0b067e5222e694' , 'Annotation' , [500]])
def_array.append(['/FWA/FWAA_9e84df84299ea7c7bd683cab' , 'Annotation' , [1000]])
def_array.append(['/FWA/FWAA_2d3407a66e4c3f5f4af708a6' , 'Annotation' , [500]])
def_array.append(['/FWA/FWAA_913931eeceaecadaa7e42b9a' , 'Annotation' , [500]])
def_array.append(['/FWA/FWAA_45dd1353150b50ff0a4ffd50' , 'Annotation' , [500]])
def_array.append(['/FWA/FWAA_29257ca617467af974a491a8' , 'Annotation' , [500]])
def_array.append(['/FWA/FWAA_01c091b7efa67fe9aa747ab0' , 'Annotation' , [500]])
def_array.append(['/FWA/FWAA_6ea8f27808febb1a25e1f17b' , 'Annotation' , [500]])
def_array.append(['/FWA/FWAA_42de2db58f7626abfa4deeab' , 'Annotation' , [500]])
def_array.append(['/FWA/FWAA_e962105f2ecf129bfec1abbe' , 'Annotation' , [500]])
def_array.append(['/FWA/FWAA_2abe326229b91c20012993a8' , 'Annotation' , [500]])
def_array.append(['/FWA/FWAA_64c6ce30eab2c31e340a483d' , 'Annotation' , [500]])
def_array.append(['/FWA/FWAA_cc15bba1247c59a0efe42e90' , 'Annotation' , [500]])