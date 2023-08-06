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
from vsc.impl.coverage_registry import CoverageRegistry

'''
Created on Jul 23, 2019

@author: ballance
'''

from vsc.model.constraint_expr_model import ConstraintExprModel

rand_obj_type_m = {}
constraint_scope_stack = []
expr_l = []
foreach_arr_s = []

def test_setup():
    rand_obj_type_m.clear()
    constraint_scope_stack.clear()
    expr_l.clear()
    foreach_arr_s.clear()
    CoverageRegistry._inst = None
    
def test_teardown():
    rand_obj_type_m.clear()
    foreach_arr_s.clear()
    if len(expr_l) != 0:
        print("Error: Leftbehind expressions")
        for ex in expr_l:
            print("Expr: " + str(ex))
        raise Exception("Leftbehind expressions")
    CoverageRegistry._inst = None

def push_foreach_arr(arr):
    foreach_arr_s.append(arr)
    
def is_foreach_arr(arr):
    return arr in foreach_arr_s

def pop_foreach_arr():
    foreach_arr_s.pop()

def push_expr(e):
    expr_l.append(e)
    
def pop_expr():
    return expr_l.pop()
    
def pop_exprs():
    ret = expr_l.copy()
    expr_l.clear()
    return ret

def clear_exprs():
    expr_l.clear()

def push_constraint_scope(s):
    constraint_scope_stack.append(s)
    
def push_constraint_stmt(s):
    for e in pop_exprs():
        constraint_scope_stack[-1].constraint_l.append(ConstraintExprModel(e))
    constraint_scope_stack[-1].constraint_l.append(s)
    
def pop_constraint_scope():
    for e in pop_exprs():
        constraint_scope_stack[-1].constraint_l.append(ConstraintExprModel(e))
    return constraint_scope_stack.pop()

def constraint_scope():
    return constraint_scope_stack[-1]

def constraint_scope_depth():
    return len(constraint_scope_stack)

def in_constraint_scope():
    return len(constraint_scope_stack) > 0

def last_constraint_stmt():
    if len(constraint_scope_stack) > 0 and len(constraint_scope_stack[-1].constraint_l) > 0:
        return constraint_scope_stack[-1].constraint_l[-1]
    else:
        return None
    
# def unk():
#     if t != None:
#         ret = []
#         t_qname = t.__qualname__
#         i=0
#         while i < len(constraint_l):
#             s = constraint_l[i]
#             s_qname = s.t.__qualname__
#             
#             if len(s_qname) > len(t_qname) and t_qname == s_qname[:s_qname.rfind('.')]:
#                 ret.append(s)
#                 constraint_l.remove(s)
#             else:
#                 i += 1
#     else:
#         ret = constraint_l.copy()
#         constraint_l.clear()
# 
#     return ret        
    