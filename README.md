Unethical python hacks
======================

A collection of script with proofs of crazy concepts.
Use at your own risk!

[mem_view.py](mem_view.py)
--------------------------

**Edit arbitrary memory of your python process!**
Provides a memory view `Mem`.
Modifies a `bytes` object `b'xyz' -> b'abc'` in-place as an example.
As a side effect, poisons object collection and causes `print(b'xyz')` to print `b'abc'`.

