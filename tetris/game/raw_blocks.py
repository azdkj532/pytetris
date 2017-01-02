__all__ = ('BLOCKS', 'BLOCK_TYPES')

BLOCK_TYPES = 'IJLOSTZ'

RAW_BLOCK_I = """\
O___
O___
O___
O___\
"""

RAW_BLOCK_J = """\
O___
OOO_
____
____\
"""

RAW_BLOCK_L = """\
__O_
OOO_
____
____\
"""

RAW_BLOCK_O = """\
OO__
OO__
____
____\
"""

RAW_BLOCK_S = """\
_OO_
OO__
____
____\
"""

RAW_BLOCK_T = """\
_O__
OOO_
____
____\
"""

RAW_BLOCK_Z = """\
OO__
_OO_
____
____\
"""

BLOCKS = {
    t: globals()['RAW_BLOCK_' + t] for t in BLOCK_TYPES
}
