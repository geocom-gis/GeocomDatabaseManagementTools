# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
# Name:        gc_egdb_set_spidx_utils
# Purpose:
#
# Author:      Geocom Informatik AG
#
# Created:     01.04.2018
# Copyright:   (c) Geocom Informatik AG 2018
#-------------------------------------------------------------------------------

import arcpy
import os
from arcpy import env
import datetime


class Spatial_Idx_Util(object):
    '''
    classdocs
    '''
    _qualifier = ""

    def __init__(self,params):
        '''
        Constructor
        '''
        pass
    def Message(self, messageText, severity=0):
        '''
        Minimales Messaging, welches die Zeit und den Text ausgiebt.
        @param messageText: Meldung welche ausgebene werdeb soll
        @param severity: 0: Message, 1: Warnung, 2: Fehler
        '''
        if severity == 0:
            arcpy.AddMessage("        %s :   %s" % (str(datetime.datetime.now()), messageText))
        if severity == 1:
            arcpy.AddWarning("        %s :   %s" % (str(datetime.datetime.now()), messageText))
        if severity == 2:
            arcpy.AddError("        %s :   %s" % (str(datetime.datetime.now()), messageText))

    
    def GetQualifier(self, p_InputWS):
        arcpy.env.workspace = p_InputWS
        featureDataSets = arcpy.ListDatasets()
	qualifier = ""
        for fds in featureDataSets:
            qualifier = ""
            messageText =  fds
            self.Message(messageText, 0)
            sp = str(fds).split(".")
            sp.remove(sp[len(sp) - 1])
            for s in sp:
                if len(s) > 0:
                    qualifier += "."
                    qualifier += s
        
        if len(qualifier) > 0:
            qualifier += "."
        return qualifier 
     
    
                
    def RulesForCalculateDefaultGridIndex(self, p_IndexGridValue, p_ElementCount):
        result =1000   #Default
        
        if p_ElementCount <=1000:
            result =1000
        
        if p_ElementCount >1000:
            result =1000
                
        if p_ElementCount >=100000:
            result =1000
            if p_IndexGridValue <=300:
                result =200
            if p_IndexGridValue >300 and p_IndexGridValue <=700:
                result =500
        
        if p_ElementCount >=1000000:
            result= p_IndexGridValue   
                
        return result  
    
    def BuildSpatialIndexParams(self, p_InputWS):
        env.workspace = p_InputWS
        ds = ['']
        for fds in arcpy.ListDatasets():
            ds.append("/" + str(fds))
    
        for currentDS in ds:
            env.workspace = p_InputWS + currentDS
            self.Message(p_InputWS + currentDS + ":-----------------------------")
            for fc in arcpy.ListFeatureClasses():
                desc = arcpy.Describe(fc)
                indexGrid = []
                try:
                    resultIdx = arcpy.CalculateDefaultGridIndex_management(fc)
                    for i in range(0, resultIdx.outputCount):
                        indexGrid.append(resultIdx.getOutput(i))         
                except:
                    pass
                
                result = arcpy.GetCount_management(fc)
                count = int(result.getOutput(0))
                gridVal=self.RulesForCalculateDefaultGridIndex(int(indexGrid[0]), count)
                messageText =  ("def_array.append(['%s/%s' , '%s' , %s, %s])")%(currentDS,fc,desc.shapeType,gridVal,count)
                self.Message(messageText, 1)
        
    
    def SetDefaultSpatialIndex(self, p_InputWS):
        env.workspace = p_InputWS
        ds = ['']
        for fds in arcpy.ListDatasets():
            ds.append("/" + str(fds))
    
        for currentDS in ds:
            env.workspace = p_InputWS + currentDS
            messageText =  str(p_InputWS + currentDS) + ":-----------------------------"
            self.Message(messageText, 0)
            for fc in arcpy.ListFeatureClasses():
                desc = arcpy.Describe(fc)
                if desc.hasSpatialIndex == False: 
                    indexGrid = []
                    result = arcpy.GetCount_management(fc)
                    count = int(result.getOutput(0))
                    try:
                        resultIdx = arcpy.CalculateDefaultGridIndex_management(fc)
                        for i in range(0, resultIdx.outputCount):
                            indexGrid.append(float(resultIdx.getOutput(i))) 
                        spIdx = self.RulesForCalculateDefaultGridIndex(int(indexGrid[0]), count)                    
                        arcpy.AddSpatialIndex_management(fc,spIdx) 
                        messageText =  ("Neuer Index def_array.append(['%s/%s' , '%s' , %s])")%(currentDS,fc,desc.shapeType,spIdx)
                        self.Message(messageText, 0)
                    except:        
                        messageText =  ("Index '%s/%s' , '%s' von Hand setzen! Vorschlag ArcGIS:%s")%(currentDS,fc,desc.shapeType,indexGrid)
                        self.Message(messageText, 2)
     
     
                        
    def SetSpatialIndexDefArray(self, p_InputWS, p_Array, p_qualif=""):

        for param in p_Array:
            if p_qualif!="":
                currentVal = str(param[0]).split('/')
                fc = os.path.join(p_InputWS, p_qualif[1:] + currentVal[1], p_qualif[1:] + currentVal[2])                
            else:
                fc=p_InputWS + param[0]
                
            spIdx=param[2]
            
            try:
                desc = arcpy.Describe(fc)
            except:
                pass
            try:
                desc = arcpy.Describe(fc)
                if desc.hasSpatialIndex:
                    arcpy.RemoveSpatialIndex_management(fc)
            except arcpy.ExecuteError:
                messageText =  arcpy.GetMessages(2) + "ERROR --> REMOVE = "  + "  fuer " +  fc
                self.Message(messageText, 2)
            try:
                arcpy.AddSpatialIndex_management(fc,spIdx[0])
                messageText =  "--> IDX = "  + str(spIdx[0]) +"  fuer " +  fc
                self.Message(messageText, 0)
            except arcpy.ExecuteError:
                messageText =  arcpy.GetMessages(2) + "ERROR --> IDX = "  + str(spIdx[0]) +"  fuer " +  fc
                self.Message(messageText, 2)
              
                        
