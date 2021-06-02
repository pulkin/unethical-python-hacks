import sys
assert sys.version_info.major == 3
assert sys.version_info.minor == 9
import inspect
import struct
import dis
from itertools import count

from mem_view import Mem, _p_hex


locals().update(dis.opmap)


class Frame:
    def __init__(self, frame):
        self.code = frame.f_code.co_code
        self.code_view = Mem.view(self.code)
        self.pos = frame.f_lasti

    @property
    def current_opcode(self):
        return self.code[self.pos]

    @property
    def last_opcode(self):
        return self.code[-2]

    def __len__(self):
        return len(self.code)

    def __setitem__(self, pos, patch):
        assert len(patch) <= len(self.code_view), f"len(patch) = {len(patch)} > len(code) = {len(code)}"
        assert 0 <= pos < len(self.code_view) - len(patch), f"Index {pos:d} out of range [0, {len(self.code_view) - len(patch) - 1}]"
        self.code_view[pos:pos + len(patch)] = patch

    def patch(self, patch, pos, anchor="head"):
        if anchor == "head":
            self[pos] = patch
        elif anchor == "current":
            self[pos + self.pos] = patch
        else:
            raise NotImplementedError


def return_(what):
    frame = Frame(inspect.currentframe().f_back)
    assert frame.current_opcode == CALL_FUNCTION
    frame.patch(bytes([RETURN_VALUE, 0]) * 2, 0, "current")
    return what


def _jump_absolute(i):
    bts = i.to_bytes((i.bit_length() + 7) // 8, byteorder="big")
    assert len(bts) < 5
    return bytes(sum((
        [EXTENDED_ARG, b]
        for b in bts[:-1]
    ), []) + [JUMP_ABSOLUTE, bts[-1]])


def permajump(where, anchor="head"):
    frame = Frame(inspect.currentframe().f_back)
    if anchor == "head":
        pass
    elif anchor == "current":
        where += frame.pos
    else:
        raise NotImplementedError
    assert 0 <= where < len(frame), f"Cannot jump to {where:d}"
    assert frame.current_opcode == CALL_FUNCTION
    frame.patch(_jump_absolute(where), 4, "current")
    return


if __name__ == "__main__":
    def a():
        return_("h" + "acked123"[:-3])
        return 2
    assert a() == "hacked"

    def a():
        x = "hacked"
        permajump(8, "current")
        x = 42
        return x
    assert a() == "hacked"

