Unethical python hacks
======================

A collection of script with proofs of crazy concepts.
Use at your own risk!

[mem_view.py](mem_view.py)
--------------------------

*Edit arbitrary memory of your python process!*

Provides a memory view `Mem`.
Modifies a `bytes` object `b'xyz' -> b'abc'` in-place as an example.
As a side effect, poisons object collection and causes `print(b'xyz')` to print `b'abc'`.

[flow_control.py](flow_control.py)
----------------------------------

*Patching opcodes during runtime!*

```python
from flow_control import return_, permajump

def f():
    return_("hacked")
    return 42

print(f())  # prints 'hacked'

def g():
    x = "hacked"
    jump(8, "current")
    x = 42
    return x
print(f())  # prints 'hacked'
```

