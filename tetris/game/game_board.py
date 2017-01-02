from . import blocks

class State:
    AllGreen = 0
    OutOfBoard = 1
    ConflictWithBlock = 2

class GameBoard(object):
    def __init__(self, _width = 10, _height=20):
        """
        add first block and next block
        """

        self.height = _height + 4
        self.width = _width

        # (0, 0) is leftest and highest corner
        self.board = [[0 for y in range(self.width)] for x in range(self.height)]

        self.current_block_pos = (0, int(self.width/2))
        self.current_block = blocks.random_block()
        self.next_block = blocks.random_block()

    # Game control related API

    def next_tick(self):
        """
        next game tick
        """
        x, y = self.current_block_pos
        next_block_pos = (x+1, y)
        next_state = self._conflict_detact(self.current_block, next_block_pos)

        if next_state is State.AllGreen:
            self.current_block_pos = next_block_pos
            return False

        elif next_state is State.ConflictWithBlock or next_state is State.OutOfBoard:
            self._make_deposit()
            return True

    def is_gameover(self):
        """
        return a bool indicate that is game over or not
        """
        for x in range(4):
            for y in range(width):
                if self.board[x][y] != 0:
                    return True

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
        next_block_pos = (x + direction, y)

        if self._conflict_detact(self.current_block, next_block_pos) is State.AllGreen:
            self.current_block_pos = next_block_pos

    def down(self):
        """
        put down current block immediately
        """
        while not self.next_tick():
            pass

    def rotate(self, direction):
        """
        Rotate the block, left for anticlockwise, right for clockwise
        """
        if direction not in ['right', 'left']:
            raise ValueError('direction should be right or left')

        block = self.current_block
        self.current_block = self.current_block.rotate(direction)

        if self._conflict_detact() is not State.AllGreen:
            self.current_block = block

    def __getitem__(self, pos):
        """
        raw board accessor

        p = block[0, 0]
        """

        x, y = pos
        return self.board[x][y]

    def clear(self):
        self.board = [[0 for y in range(self.width)] for x in range(self.height)]

    # Private functionis
    def _conflict_detact(self, block=None, pos=None):
        if block is None:
            block = self.current_block
        if pos is None:
            pos = self.current_block_pos

        for row in range(4):
            for column in range(4):
                if block[row, column] == 'O':
                    offset = (row + pos[0], column + pos[1])
                    if not offset[0] < self.height:
                        return State.OutOfBoard
                    
                    if not self.width > offset[1] >= 0:
                        return State.OutOfBoard

                    if self.board[offset[0]][offset[1]] > 0:
                        return State.ConflictWithBlock

        return State.AllGreen

    def _make_deposit(self, block=None, pos=None):
        """
        Make current block deposit
        """
        if block is None:
            block = self.current_block
        if pos is None:
            pos = self.current_block_pos

        for row in range(4):
            for column in range(4):
                offset = (row + pos[0], column + pos[1])
                if block[row, column] == 'O':
                    self.board[offset[0]][offset[1]] = 1

        self.current_block = self.next_block
        self.current_block_pos = (0, int(self.width/2))
        self.next_block = blocks.random_block()
