from types import FunctionType


EQUALITY_FUNCTIONS = [
        '__eq__',
        '__ne__',
        ]



class Mutable:
    def __init__(self, val):
        self.val = val

    def get(self):
        return self.val

    def set(self, val):
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
    pass



class MutableNumeric(Mutable):
    pass


class Int(MutableNumeric):
    pass

class Float(MutableNumeric):
    pass

