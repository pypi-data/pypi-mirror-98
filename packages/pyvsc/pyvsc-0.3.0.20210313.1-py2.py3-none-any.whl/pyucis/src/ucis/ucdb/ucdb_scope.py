# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#  http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.
from ucis.ucdb.ucdb_cover_index import UcdbCoverIndex
#from ucis.ucdb.ucdb_scope_iterator import UcdbScopeIterator
from typing import Iterator
'''
Created on Jan 11, 2020

@author: ballance
'''

from _ctypes import byref, pointer
from ucis.scope import Scope
from ucis.unimpl_error import UnimplError
from ucis import UCIS_COVERGROUP, UCIS_INT_SCOPE_GOAL, UCIS_INT_CVG_STROBE,\
    UCIS_INT_CVG_MERGEINSTANCES, UCIS_STR_COMMENT, UCIS_INT_SCOPE_WEIGHT

from ucis.cover_data import CoverData
from ucis.flags_t import FlagsT
from ucis.ucdb.ucdb_cover_data import UcdbCoverData
from ucis.ucdb.ucdb_obj import UcdbObj
from ucis.ucdb.ucdb_source_info import _UcdbSourceInfo, UcdbSourceInfo
from ucis.ucdb.libucdb import get_lib
from ucis.scope_type_t import ScopeTypeT
from ucis.source_info import SourceInfo
from ucis.source_t import SourceT
from ucis.toggle_dir_t import ToggleDirT
from ucis.toggle_metric_t import ToggleMetricT
from ucis.toggle_type_t import ToggleTypeT


class UcdbScope(UcdbObj, Scope):
    
    def __init__(self, db, obj):
        UcdbObj.__init__(self, db, obj)
        Scope.__init__(self)
        print("UcdbScope::init - db=" + str(self.db) + " " + str(self.obj))
        
    def getGoal(self)->int:
        return self.getIntProperty(-1, UCIS_INT_SCOPE_GOAL)
    
    def setGoal(self,goal)->int:
        self.setIntProperty(-1, UCIS_INT_SCOPE_GOAL, goal)
        
#     def getWeight(self):
#         return self.getIntProperty(-1, UCIS_INT_SCOPE_WEIGHT)
#     
#     def setWeight(self, w):
#         self.setIntProperty(-1, UCIS_INT_SCOPE_WEIGHT, w)
        
    def createScope(self, 
        name:str, 
        srcinfo:SourceInfo, 
        weight:int, 
        source, 
        type, 
        flags):
        srcinfo_p = None if srcinfo is None else byref(_UcdbSourceInfo.ctor(srcinfo))
        print("createScope: db=" + str(self.db) + " obj=" + str(self.obj) + 
              " name=" + str(name) + " srcinfo_p=" + str(srcinfo_p) +
              " weight=" + str(weight) + "source=" + hex(source) + " type=" + hex(type) + " flags=" + hex(flags));
        sh = get_lib().ucdb_CreateScope(
            self.db,
            self.obj,
            None if name is None else str.encode(name),
            srcinfo_p,
            weight,
            source,
            type,
            flags)
        
        if sh is None:
            print("Error: createScope failed: parent=" + str(self.obj))
            raise Exception("Failed to create scope")
        
        return UcdbScope(self.db, sh)
    
    def createInstance(self,
                    name : str,
                    fileinfo : SourceInfo,
                    weight : int,
                    source : SourceT,
                    type : ScopeTypeT,
                    du_scope : Scope,
                    flags : FlagsT):
        fileinfo_p = None if fileinfo is None else byref(_UcdbSourceInfo.ctor(fileinfo))
        sh = get_lib().ucdb_CreateInstance(
            self.db,
            self.obj,
            str.encode(name),
            fileinfo_p,
            weight,
            source,
            type,
            du_scope.obj,
            flags)
        
        if sh is None:
            print("Error: ucdb_CreateInstance failed: du=" + str(du_scope) + " du.obj=" + str(du_scope.obj))
            raise Exception("ucdb_CreateInstance failed")
        
        return UcdbScope(self.db, sh)
    
    def createCovergroup(self, 
        name:str, 
        srcinfo:SourceInfo, 
        weight:int, 
        source) -> 'Covergroup':
        from ucis.ucdb.ucdb_covergroup import UcdbCovergroup
        
        srcinfo_p = None if srcinfo is None else pointer(_UcdbSourceInfo.ctor(srcinfo))
        cg_obj = get_lib().ucdb_CreateScope(
            self.db,
            self.obj,
            str.encode(name),
            srcinfo_p,
            weight,
            source,
            UCIS_COVERGROUP,
            0)
        
        return UcdbCovergroup(self.db, cg_obj)
    
    def createToggle(self,
                    name : str,
                    canonical_name : str,
                    flags : FlagsT,
                    toggle_metric : ToggleMetricT,
                    toggle_type : ToggleTypeT,
                    toggle_dir : ToggleDirT) -> 'Scope':
        th = get_lib().ucdb_CreateToggle(
            self.db,
            self.obj,
            str.encode(name),
            None if canonical_name is None else str.encode(canonical_name),
            flags,
            toggle_metric,
            toggle_type,
            toggle_dir)
        return UcdbScope(self.db, th)
    
    def createNextCover(self,
                        name : str,
                        data : CoverData,
                        sourceinfo : SourceInfo) -> int:
        sourceinfo_p = None if sourceinfo is None else byref(_UcdbSourceInfo.ctor(sourceinfo))
        data_p = byref(UcdbCoverData.ctor(data))
        
        index =  get_lib().ucdb_CreateNextCover(
            self.db,
            self.obj,
            str.encode(name),
            data_p,
            sourceinfo_p)
        
        return UcdbCoverIndex(self.db, self.obj, index)
    
    def getSourceInfo(self)->SourceInfo:
        libsrcinfo = _UcdbSourceInfo()
        sourceinfo_p = byref(libsrcinfo)
        
        get_lib().ucdb_GetScopeSourceInfo(self.db, self.obj, sourceinfo_p)
        
        return UcdbSourceInfo.ctor(self.db, libsrcinfo)
    
    def scopes(self, mask:ScopeTypeT)->Iterator['Scope']:
        return UcdbScopeIterator(self.db, self.obj, mask)
        