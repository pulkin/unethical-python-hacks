import inspect

from mem_view import Mem


def _return(what):
    parent_frame = inspect.currentframe().f_back
    parent_code = parent_frame.f_code.co_code
    pos = parent_frame.f_lasti
    assert parent_code[pos] == 0x83  # CALL_FUNCTION
    assert len(parent_code) >= pos + 4
    mem = Mem.view(parent_code)
    mem[pos:pos + 4] = b'\x53\x00' * 2  # RETURN and RETURN
    return what


if __name__ == "__main__":
    def a():
        def b():
            def c():
                _return("h" + "acked123"[:-3])
                return 2
            return c()
        return b()
    print("return value:", a())
    print("return value (2):", a())

