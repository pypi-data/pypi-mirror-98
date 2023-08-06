'''
Created on May 16, 2020

@author: ballance
'''
from vsc.model.expr_model import ExprModel
from vsc.model.expr_fieldref_model import ExprFieldRefModel

class ExprArraySubscriptModel(ExprModel):
    
    def __init__(self, lhs : 'FieldArrayModel', rhs : ExprModel):
        self.lhs = lhs
        self.rhs = rhs
        
    def build(self, btor):
        index = int(self.rhs.val())
        if isinstance(self.lhs, ExprFieldRefModel):
            fm = self.lhs.fm.field_l[index]
            return fm.build(btor)
        else:
            # TODO: support array slicing
            raise NotImplementedError("Cannot subscript an lvalue of type " + str(type(self.lhs)))
        
    def subscript(self):
        index = int(self.rhs.val())
        if isinstance(self.lhs, ExprFieldRefModel):
            if index < len(self.lhs.fm.field_l):
                return self.lhs.fm.field_l[index]
            else:
                raise Exception("List size: " + str(len(self.lhs.fm.field_l)) + " index: " + str(index))
        else:
            # TODO: support array slicing
            raise NotImplementedError("Cannot subscript an lvalue of type " + str(type(self.lhs)))
        
        
    def is_signed(self):
        index = int(self.rhs.val())
        if isinstance(self.lhs, ExprFieldRefModel):
            return self.lhs.fm.field_l[index].is_signed
        else:
            # TODO: support array slicing
            raise NotImplementedError("Cannot subscript an lvalue of type " + str(type(self.lhs)))
        
    def width(self):
        index = int(self.rhs.val())
        if isinstance(self.lhs, ExprFieldRefModel):
            return self.lhs.fm.field_l[index].width()
        else:
            # TODO: support array slicing
            raise NotImplementedError("Cannot subscript an lvalue of type " + str(type(self.lhs)))
        
    def accept(self, v):
        v.visit_expr_array_subscript(self)
        
    def val(self):
        index = int(self.rhs.val())
        if isinstance(self.lhs, ExprFieldRefModel):
            return self.lhs.fm.field_l[index].val()
        else:
            # TODO: support array slicing
            raise NotImplementedError("Cannot subscript an lvalue of type " + str(type(self.lhs)))
        
    def getFieldModel(self):
        index = int(self.rhs.val())
        if isinstance(self.lhs, ExprFieldRefModel):
            return self.lhs.fm.field_l[index]
        else:
            # TODO: support array slicing
            raise NotImplementedError("Cannot subscript an lvalue of type " + str(type(self.lhs)))
        
