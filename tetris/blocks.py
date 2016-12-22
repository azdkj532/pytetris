import os
import random
from . import raw_blocks

prng = random.Random(int.from_bytes(os.urandom(16), 'big'))

def normalize(block):
    c = 0
    while all(block[i][0] != 'O' for i in range(len(block))):
        c += 1
        if c >= len(block):
            break
        block = [
            r[1:] + ['_']
            for r in block
        ]

    c = 0
    while all(block[0][i] != 'O' for i in range(len(block[0]))):
        c += 1
        if c >= len(block):
            break
        block = block[1:] + [block[0]]

    return block

def rotate_right(block):
    w, h = len(block[0]), len(block)

    new_block = [
        [
            block[h - j - 1][i]
            for j in range(h)
        ]
        for i in range(w)
    ]

    return new_block

def rotate_left(block):
    w, h = len(block[0]), len(block)

    new_block = [
        [
            block[j][w - i - 1]
            for j in range(h)
        ]
        for i in range(w)
    ]

    return new_block

class Block(object):
    @staticmethod
    def parse_block(raw_block):
        return [ list(s) for s in raw_block.split() ]

    @staticmethod
    def compose_block(block):
        return '\n'.join( ''.join(s) for s in block )

    def __init__(self, raw_block=None, block=None):
        if raw_block:
            self.block = Block.parse_block(raw_block)
        elif block:
            self.block = block
        else:
            raise ValueError('Either `raw_block` or `block` must be given')

    def rotate(self, direction):
        """
        Rotate current block and return new Block object

        direction -- can be 'left' or 'right'
        """
        if direction == 'left':
            return Block(block=normalize(rotate_left(self.block)))
        elif direction == 'right':
            return Block(block=normalize(rotate_right(self.block)))
        else:
            raise ValueError('`direction` should be either "left" or "right"')

    def __repr__(self):
        return 'Block(%r)' % Block.compose_block(self.block)

    def __str__(self):
        return Block.compose_block(self.block)

def get_block(type_):
    """
    Return a Block object with specific type

    type_ -- one of raw_blocks.BLOCK_TYPES
    """

    return Block(raw_blocks.BLOCKS[type_])

def random_block(types=raw_blocks.BLOCK_TYPES):
    """
    Return a Block object with random type
    """

    type_ = prng.choice(types)
    return get_block(type_)
