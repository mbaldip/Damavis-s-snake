# Host for the objects, functions and methods for Damavis's snake problem

# Classes
class SnakeSolver:
    # todo: implement Snake class
    def __init__(self, board, snake):
        # isinstance logics could make the code more robust

        self._board = self._isValidBoard(board)
        self._snake = self._isValidSnake(snake)

    # board constraints
    def _isValidBoard(self, board):
        
        if len(board) != 2:
            raise ValueError('Board must have 2 dimensions')
        if not ((1 <= board[0] <= 10) and (1 <= board[1] <= 10)):
            raise ValueError('Board sizes must be between 1 and 10')

        return board

    # snake constraints
    def _isValidSnake(self, snake):

        if not(3 <= len(snake) <= 7):
            raise ValueError('Snake lenght must be between 3 and 7')
        if any(len(block)!=2 for block in snake):
            raise ValueError('All sections of the snake must be two-dimensional')
        if any(self.isBlockInGrid(block)!=True for block in snake):
            raise ValueError('All blocks of the snake must be inside the grid')

        def is_snake_valid(snake_array):
            for i in range(len(snake_array)):
                current = snake_array[i]

                if i > 0:
                    # check continuity:
                    p = snake_array[i-1]
                    if current not in [[p[0],p[1]+1], [p[0],p[1]-1], [p[0]+1,p[1]], [p[0]-1,p[1]]]:
                        return False
                    # check self-intersections
                    if current in snake_array[:i]:
                        return False
            return True
        if not is_snake_valid(snake):
            raise ValueError('Snake must be continuous and have no self-intersections')

        return snake

    # check if a block is within the grid limits
    def isBlockInGrid(self, block):
        if (0 <= block[0] < self._board[0]) and (0 <= block[1] < self._board[1]):
            return True
        else:
            return False
    
    # Recursive solving for the snake problem
    def _solve_snake(self, snake_state, depth):
        npaths = 0
        if depth <= 0:
            return 1
        else:
            up    = [snake_state[-1][0],snake_state[-1][1]+1]
            down  = [snake_state[-1][0],snake_state[-1][1]-1]
            left  = [snake_state[-1][0]+1,snake_state[-1][1]]
            right = [snake_state[-1][0]-1,snake_state[-1][1]]
            snake_state.pop(0) # tailess snake

            for next_cell in [up, down, left, right]:
                # block in grid and not in snake
                if self.isBlockInGrid(next_cell) and next_cell not in snake_state:
                    next_state = snake_state.copy()
                    next_state.append(next_cell)
                    npaths += self._solve_snake(next_state, depth-1)
                    next_state.clear()
                
            return npaths

    def numberOfAvailableDifferentPaths(self, depth):
        # assert depth condition
        if not(1 <= depth <= 20):
            raise ValueError('Depth must be between 1 and 20')

        # run recursive paths
        # send a copy of the initial snake to avoid compromising other braches of the recursion
        snake_copy = self._snake.copy()
        # reversing is needed for efficiency, could also use collections.deque
        snake_copy.reverse() # reverses in-place
        npaths = self._solve_snake(snake_copy, depth)

        return npaths