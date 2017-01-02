import tetris
import unittest

class TestBlockHelperFunctions(unittest.TestCase):
    def test_rotate_right(self):
        self.assertEqual(tetris.blocks.rotate_right([
            [1]
        ]), [
            [1]
        ])

        self.assertEqual(tetris.blocks.rotate_right([
            [1, 2]
        ]), [
            [1],
            [2]
        ])

        self.assertEqual(tetris.blocks.rotate_right([
            [1, 2],
            [3, 4],
            [5, 6]
        ]), [
            [5, 3, 1],
            [6, 4, 2]
        ])

    def test_rotate_left(self):
        self.assertEqual(tetris.blocks.rotate_left([
            [1]
        ]), [
            [1]
        ])

        self.assertEqual(tetris.blocks.rotate_left([
            [1, 2]
        ]), [
            [2],
            [1]
        ])

        self.assertEqual(tetris.blocks.rotate_left([
            [1, 2],
            [3, 4],
            [5, 6]
        ]), [
            [2, 4, 6],
            [1, 3, 5]
        ])

        src = [
            [ 1, 2, 3, 4, 5 ],
            [ 6, 7, 8, 9, 10],
            [ 7, 8, 9,10, 11]
        ]
        rright = tetris.blocks.rotate_right(src)
        rleft = tetris.blocks.rotate_left(rright)
        self.assertEqual(src, rleft)

    def test_random_block(self):
        for i in range(16):
            block = tetris.blocks.random_block()
            raw_block = str(block)
            self.assertIn(raw_block, tetris.raw_blocks.BLOCKS.values())

    def test_block_rotation(self):
        for i in range(16):
            block = tetris.blocks.random_block()
            rotated = block.rotate('left').rotate('right')
            self.assertEqual(str(block), str(rotated))
