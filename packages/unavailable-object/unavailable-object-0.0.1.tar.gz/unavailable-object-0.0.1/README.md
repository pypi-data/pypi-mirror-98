# Unavailable Object

A placeholder object for optional dependencies.

## Usage

```python
from unavailable_object import UnavailableObject

try:
    import optional_module
except ImportError:
        optional_module = UnavailableObject("optional_module")
```

## Type Checking
To not disturb the type checker, the alternative definition of `optional_object` should be guarded by `if not TYPE_CHECKING`
and type annotations put in quotes:

```python
from typing import TYPE_CHECKING
from unavailable_object import UnavailableObject

try:
    import optional_module
except ImportError:
    if not TYPE_CHECKING:
        optional_module = UnavailableObject("optional_module")

def foo(arg: "optional_module.SomeType") -> None:
    pass
```
