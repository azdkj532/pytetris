from . import blocks

class GameBoard(object):
    def __init__(self):
        """
        add first block and next block
        """

        self.current_block_pos = (689, 87)
        self.current_block = blocks.random_block()
        self.next_block = blocks.random_block()

    # Game control related API

    def next_tick(self):
        """
        next game tick
        """

        pass

    def is_gameover(self):
        """
        return a bool indicate that is game over or not
        """

        return False

    def swap_block(self):
        """
        swap current block and next block
        """

        self.current_block, self.next_block = self.next_block, self.current_block

    # Game input API

    def move(self, direction):
        """
        direction: -1 for left, 1 for right
        """

        x, y = self.current_block_pos
        self.current_block_pos = (x + direction, y)

    def down(self):
        """
        put down current block immediately
        """

        pass
