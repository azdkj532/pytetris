from tetris import game
from tetris.game.game_board import State
import unittest

class TestBoardHelperFunctions(unittest.TestCase):
    def setUp(self):
        self.gameboard = game.GameBoard()

    def test_deposit_test(self):
        block = game.blocks.get_block('O')
        self.gameboard.current_block = block
        self.gameboard.current_block_pos = (20, 0)
        self.gameboard._make_deposit()
        
        self.assertEqual(self.gameboard.board[20][0], 1)
        self.assertEqual(self.gameboard.board[20][0], 1)
        self.assertEqual(self.gameboard.board[20][1], 1)
        self.assertEqual(self.gameboard.board[20][2], 0)
        self.assertEqual(self.gameboard.board[21][0], 1)
        self.assertEqual(self.gameboard.board[21][1], 1)
        self.assertEqual(self.gameboard.board[21][2], 0)
        self.assertEqual(self.gameboard.board[22][0], 0)
        self.assertEqual(self.gameboard.board[22][1], 0)
        self.assertEqual(self.gameboard.board[22][2], 0)

    def test_block_next_tick(self):
        pos = self.gameboard.current_block_pos
        expect_pos = (pos[0]+1, pos[1])
        self.gameboard.next_tick()

        self.assertEqual(expect_pos, self.gameboard.current_block_pos)

    def test_down_test(self):
        block = game.blocks.get_block('O')
        self.gameboard.current_block = block
        self.gameboard.down()

        self.assertEqual(self.gameboard.board[21][5], 0)
        self.assertEqual(self.gameboard.board[21][6], 0)
        self.assertEqual(self.gameboard.board[21][7], 0)
        self.assertEqual(self.gameboard.board[22][5], 1)
        self.assertEqual(self.gameboard.board[22][6], 1)
        self.assertEqual(self.gameboard.board[22][7], 0)
        self.assertEqual(self.gameboard.board[23][5], 1)
        self.assertEqual(self.gameboard.board[23][6], 1)
        self.assertEqual(self.gameboard.board[23][7], 0)


    def test_bottom_conflict_test(self):
        block = game.blocks.get_block('O')
        c_pos = (40, 0)
        self.assertEqual(self.gameboard._conflict_detact(block, c_pos), State.OutOfBoard)

        c_pos = (self.gameboard.height, 0)
        self.assertEqual(self.gameboard._conflict_detact(block, c_pos), State.OutOfBoard)

        c_pos = (10, 0)
        self.assertEqual(self.gameboard._conflict_detact(block, c_pos), State.AllGreen)

    def test_edge_conflict_test(self):
        block = game.blocks.get_block('O')
        c_pos = (10, self.gameboard.width)
        self.assertEqual(self.gameboard._conflict_detact(block, c_pos), State.OutOfBoard)

        c_pos = (10, -1)
        self.assertEqual(self.gameboard._conflict_detact(block, c_pos), State.OutOfBoard)

        c_pos = (10, self.gameboard.width-2)
        self.assertEqual(self.gameboard._conflict_detact(block, c_pos), State.AllGreen)

    def test_block_conflict_test(self):
        block = game.blocks.get_block('O')
        pos = (20, 0)
        self.gameboard.current_block = block
        self.gameboard.current_block_pos = pos
        self.gameboard._make_deposit(block, pos)

        self.assertEqual(
            self.gameboard._conflict_detact(block, pos),
            State.ConflictWithBlock
        )

    def test_rotate(self):
        pass

    def test_move(self):
        pass

    def test_swap_block(self):
        pass

    def test_is_gameover(self):
        pass
