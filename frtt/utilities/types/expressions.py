from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Callable, Union
from math import pow

from frtt.utilities.types.generic import Variable

Literal = Union[int, float, str]

"""
Abstract expression
"""
class Expr(ABC):
    
    @abstractmethod
    def eval(self, assignment):
        pass

"""
Expression that supports assignment to subexpressions
"""    
class Expression(Expr):
    
    def __init__(self, expr : Expr):
        self.expr = expr
        self.mutexprs : dict[Variable, MutableExpr] = dict()

    def assign(self, var : Variable, expr : Expr):
        self.mutexprs[var].assign(expr)
        
    def eval(self):
        return self.expr.eval()
    
"""
Expression that accesses an array literal
"""
    
class ArrayAccess(Expr):
    def __init__(self, op : Expr, indices : list[Expr]):
        self.op = op
        self.indices = indices
    
    def eval(self):
        res = self.op.eval()
        for index in reversed(self.indices): res = res[index.eval()]
        return res

"""
Mutable expression
Supports assignment by external routines
"""
class MutableExpr(Expr):
        
    def __init__(self, expr : Expr):
        self.expr = expr

    def assign(self, expr : Expr):
        self.expr = expr

    def eval(self):
        return self.expr.eval()

"""
Unary expression
Implements a lambda function with one argument
"""
class UnaryExpr(Expr):
    def __init__(self, op : Expr, f : Callable[[Literal], Literal]):
        self.op = op
        self.f = f
        
    def eval(self):
        return self.f(self.op.eval())
    
# Integer / Real operations
unaryplus_op = lambda a : +a
negate_op = lambda a : -a
parentheses_op = lambda a : a

# Boolean operations
not_op = lambda a : not a

# Expressions
UnaryPlus = lambda op : UnaryExpr(op, unaryplus_op)
Negate = lambda op : UnaryExpr(op, negate_op)
Parentheses = lambda op : UnaryExpr(op, parentheses_op)
NOT = lambda op : UnaryExpr(op, not_op)
    
"""
Binary expression
Implements a lambda function with two arguments
"""
class BinaryExpr(Expr):
    def __init__(self, op1 : Expr, op2 : Expr, f : Callable[[Literal, Literal], Literal]):
        self.op1 = op1
        self.op2 = op2
        self.f = f
        
    def eval(self):
        return self.f(self.op1.eval(), self.op2.eval())
    

# Integer / Real operations
add_op = lambda a, b : a + b
subtract_op = lambda a, b : a - b
multiply_op = lambda a, b : a * b
divide_op = lambda a, b : a / b
power_op = lambda a, b : pow(a, b)

# String operations
concat_op = lambda a, b : a + b

# Boolean operations
and_op = lambda a, b : a and b
or_op = lambda a, b : a or b
eqv_op = lambda a, b : a == b
neqv_op = lambda a, b : a != b
eq_op = lambda a, b : a == b
ne_op = lambda a, b : a != b
le_op = lambda a, b : a >= b
ge_op = lambda a, b : a >= b
lt_op = lambda a, b : a < b
gt_op = lambda a, b : a > b

# Expressions
Add = lambda op1, op2 : BinaryExpr(op1, op2, add_op)
Subtract = lambda op1, op2 : BinaryExpr(op1, op2, add_op)
Multiply = lambda op1, op2 : BinaryExpr(op1, op2, add_op)
Divide = lambda op1, op2 : BinaryExpr(op1, op2, add_op)
Power = lambda op1, op2 : BinaryExpr(op1, op2, add_op)
Concat = lambda op1, op2 : BinaryExpr(op1, op2, add_op)
AND = lambda op1, op2 : BinaryExpr(op1, op2, add_op)
OR = lambda op1, op2 : BinaryExpr(op1, op2, add_op)
EQV = lambda op1, op2 : BinaryExpr(op1, op2, add_op)
NEQV = lambda op1, op2 : BinaryExpr(op1, op2, add_op)
EQ = lambda op1, op2 : BinaryExpr(op1, op2, add_op)
NE = lambda op1, op2 : BinaryExpr(op1, op2, add_op)
LE = lambda op1, op2 : BinaryExpr(op1, op2, add_op)
GE = lambda op1, op2 : BinaryExpr(op1, op2, add_op)
LT = lambda op1, op2 : BinaryExpr(op1, op2, add_op)
GT = lambda op1, op2 : BinaryExpr(op1, op2, add_op)

"""
Literal expression
Base case for recursive execution of Expr.eval()
"""
class LiteralConstant(Expr):
    def __init__(self, val : str, cast : Callable[[str], Literal]):
        self.val = cast(val)
        
    def eval(self):
        return self.val   
    
# Expressions
RealLiteralConstant = lambda val : LiteralConstant(val, float)
IntLiteralConstant = lambda val : LiteralConstant(val, int)
CharLiteralConstant = lambda val : LiteralConstant(val, str)




"""
TODO
"""

"""
Variable expressions

Designator
| Substring
| | DataRef
| | SubstringRange
| | | Scalar
| | | | DefaultChar
| | | | | Expr
| | | | Logical
| | | | | Expr
| DataRef

DataRef
| StructureComponent
| ArrayElement
| | DataRef
| | SectionSubscript
| | | Integer
| | | SubscriptTriplet
| | | | Scalar
| Name
| | ValueString

StructureComponent
| DataRef
| Name
| | ValueString

Integer
| Variable
| | Designator
| Name
| | ValueString
| Constant
| | Designator
| | Expr
| Expr

Scalar
| DefaultChar
| | Expr
| Logical
| | Expr
"""

class Designator:
    pass

class Substring:
    pass

class DataRef:
    pass

class SubstringRange:
    pass

class Scalar:
    pass

"""
Array expressions

ArrayConstructor
| AcSpec
| | AcValue
| | | AcImpliedDo
| | | | AcValue
"""

class ArrayConstructor:
    pass

class AcSpec:
    pass

class AcValue:
    pass

class AcImpliedDo:
    pass

"""
Descendent nodes of Expr that will have no class equivalent:
- string
- FunctionReference (will be resolved to return variable of function being referenced)
"""