''' Mutable Primitives '''
#from types import FunctionType


EQUALITY_FUNCTIONS = [
        '__eq__',
        '__ne__',
        ]



class Mutable(object): # pylint: disable=useless-object-inheritance
    ''' Base class for mutable primitives '''
    def __init__(self, val):
        self.val = val

    def get(self):
        ''' get raw value of mutable '''
        return self.val

    def set(self, val):
        ''' set raw value of mutable '''
        self.val = val

    def __eq__(self, other):
        return self.val == other

    def __ne__(self, other):
        return self.val != other

    def __str__(self):
        return '{}({})'.format(self.__class__.__name__, self.val)

    def __repr__(self):
        return '<{}>'.format(self)



class Bool(Mutable):
    ''' Mutable version of float '''



class MutableNumeric(Mutable):
    ''' Base class for mutable numeric primitives '''


class Int(MutableNumeric):
    ''' Mutable version of int '''

class Float(MutableNumeric):
    ''' Mutable version of float '''
