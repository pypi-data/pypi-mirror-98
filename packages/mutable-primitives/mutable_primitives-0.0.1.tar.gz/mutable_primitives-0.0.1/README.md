# Python Mutable Primitives

While easy to create, it is crazy that python doesn't provide mutable primitives by default (AFAIK).

This package provides some simple python primitive types in a mutable shell:
- `Bool`
- `Float`
- `Int`
- `Str`


## Basic Usage and Invalid Uses

The safest usage is to always use `.set()` and `.get()`:
```
from mutable_primitives import Int

x = Int(5)

def make_x_seven():
    x.set(7)

make_x_seven()

print(x.get()) # should print 7
```

However if you understand the limitations, you can do some normal operations:
```
from mutable_primitives import Int
x = Int(5)
print(x + 4) # prints 9 (technically Int(9))
print(4 + x) # prints 9 (technically int(9))
assert x == 5
assert 5 == x
```

TODO some invalid/bad/dangerous use cases1


## Caveats, Reasoning, and FAQ

Q: This whole library is unnecessary.  
A: That's a statement.

Q: Why make a library when you can do this in a few lines when needed?  
A: Having a library just makes it more uniform and clear what's happening.

Q: There are 4 competing libraries for this functionality, why add another?  
A: There are now 5 competing libraries.

Q: Why use obfuscated/unsafe `compile`/`FunctionType` when you could just write the functions?  
A: I'm lazy, feel free to PR it.

Q: Why not subclass `int`/`float`/etc?  
A: You can't subclass `bool`, and subclassing the other primitives brings complexity.


## TODO List

In rough order of preference:

- Proper README.md
- LICENCE
- integrate with pypi
- Tests for `Bool` class
- Tests for `Int` class
- Tests for `Float` class
- Implement `Str` class
- Tests for `Str` class
- Add thread-safe mutables classes
