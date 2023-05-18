from convert_templog import *

def test_conversion():
    TXT = '1.0\n1.1\n1.2\n1.3\n'
    BIN = to_binary(TXT)

    assert TXT == to_text(BIN)
    assert BIN == to_binary(to_text(BIN))

    print("test_conversion passed")
