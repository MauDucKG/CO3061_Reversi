import turtle, random
import time

from copy import deepcopy
import math

import turtle


SQUARE = 50
TILE = 20
BOARD_COLOR = 'blue2'
LINE_COLOR = 'black'
TILE_COLORS = ['black', 'white']

class Board:

    def __init__(self, n):
       
        self.n = n
        self.board = [[0] * n for i in range(n)]
        self.square_size = SQUARE
        self.board_color = BOARD_COLOR
        self.line_color = LINE_COLOR
        self.tile_size = TILE
        self.tile_colors = TILE_COLORS
        self.move = ()

    def draw_board(self):
   
        turtle.setup(self.n * self.square_size + self.square_size, 
                    self.n * self.square_size + self.square_size)
        turtle.screensize(self.n * self.square_size, self.n * self.square_size)
        turtle.bgcolor('white')

       
        othello = turtle.Turtle(visible = False)
        othello.penup()
        othello.speed(0)
        othello.hideturtle()

       
        othello.color(self.line_color, self.board_color)
        
      
        corner = -self.n * self.square_size / 2
        othello.setposition(corner, corner)
        
       
        othello.begin_fill()
        for i in range(4):
            othello.pendown()
            othello.forward(self.square_size * self.n)
            othello.left(90)
        othello.end_fill()
        
      
        for i in range(self.n + 1):
            othello.setposition(corner, self.square_size * i + corner)
            self.draw_lines(othello)
        
       
        othello.left(90)
        for i in range(self.n + 1):
            othello.setposition(self.square_size * i + corner, corner)
            self.draw_lines(othello)

    def draw_lines(self, turt):
      
        turt.pendown()
        turt.forward(self.square_size * self.n)
        turt.penup()

    def is_on_board(self, x, y):
       
        bound = self.n / 2 * self.square_size
        
        if - bound < x < bound and - bound < y < bound:
            return True
        return False

    def is_on_line(self, x, y):
     
        if self.is_on_board(x, y):   
            if x % self.square_size == 0 or y % self.square_size == 0:
                return True
        return False

    def convert_coord(self, x, y):
        
        if self.is_on_board(x, y):
            row = int(self.n / 2 - 1 - y // self.square_size)
            col = int(self.n / 2 + x // self.square_size)
            return (row, col)
        return ()

    def get_coord(self, x, y):
        
        if self.is_on_board(x, y) and not self.is_on_line(x, y):
            self.move = self.convert_coord(x, y)
        else:
            self.move = ()

    def get_tile_start_pos(self, square):
       
        if square == ():
            return ()
        
        for i in range(2):
            if square[i] not in range(self.n):
                return ()

        row, col = square[0], square[1]

        y = ((self.n - 1) / 2 - row) * self.square_size
        if col < self.n / 2:
            x = (col - (self.n - 1) / 2) * self.square_size - self.tile_size
            r = - self.tile_size
        else:
            x = (col - (self.n - 1) / 2) * self.square_size + self.tile_size
            r = self.tile_size
        
        return ((x, y), r)

    def draw_tile(self, square, color):
        
        pos = self.get_tile_start_pos(square)
        if pos:
            coord = pos[0]
            r = pos[1]
        else:
            print('Error drawing the tile...')
            return
        
       
        tile = turtle.Turtle(visible = False)
        tile.penup()
        tile.speed(0)
        tile.hideturtle()

      
        tile.color(self.tile_colors[color])

    
        tile.setposition(coord)
        tile.setheading(90)
        
       
        tile.begin_fill()
        tile.pendown()
        tile.circle(r)
        tile.end_fill()

    def __str__(self):
       
        explanation = 'State of the board:\n'
        board_str = ''
        for row in self.board:
            board_str += str(row) + '\n' 
        printable_str = explanation + board_str

        return printable_str

    def __eq__(self, other):
      
        return self.board == other.board

MAX_DEPTH = 3
MINIMUM = -math.inf
MAXIMUM = math.inf
MOVE_DIRS = [(-1, -1), (-1, 0), (-1, +1),
             (0, -1),           (0, +1),
             (+1, -1), (+1, 0), (+1, +1)]

class StateHolder:
    def __init__(self, board, player):
        self.n = 8
        self.board = board
        self.current_player = player
        self.move = ()

    def make_move(self):
        if self.is_legal_move(self.move):
            self.board[self.move[0]][self.move[1]] = self.current_player + 1
            self.flip_tiles()

    def flip_tiles(self):
        curr_tile = self.current_player + 1 
        for direction in MOVE_DIRS:
            if self.has_tile_to_flip(self.move, direction):
                i = 1
                while True:
                    row = self.move[0] + direction[0] * i
                    col = self.move[1] + direction[1] * i
                    if self.board[row][col] == curr_tile:
                        break
                    else:
                        self.board[row][col] = curr_tile
                        i += 1

    def has_tile_to_flip(self, move, direction):
        i = 1
        if self.current_player in (0, 1) and \
           self.is_valid_coord(move[0], move[1]):
            curr_tile = self.current_player + 1
            while True:
                row = move[0] + direction[0] * i
                col = move[1] + direction[1] * i
                if not self.is_valid_coord(row, col) or \
                    self.board[row][col] == 0:
                    return False
                elif self.board[row][col] == curr_tile:
                    break
                else:
                    i += 1
        return i > 1

    def has_legal_move(self):
        for row in range(self.n):
            for col in range(self.n):
                move = (row, col)
                if self.is_legal_move(move):
                    return True
        return False

    def get_legal_moves(self):
        moves = []
        for row in range(self.n):
            for col in range(self.n):
                move = (row, col)
                if self.is_legal_move(move):
                    moves.append(move)
        return moves
    
    def is_valid_coord(self, row, col):
       
        if 0 <= row < self.n and 0 <= col < self.n:
            return True
        return False
    
    def is_legal_move(self, move):
       
        if move != () and self.is_valid_coord(move[0], move[1]) \
           and self.board[move[0]][move[1]] == 0:
            for direction in MOVE_DIRS:
                if self.has_tile_to_flip(move, direction):
                    return True
        return False
    
    def get_squares(self, player):
        """ Get the coordinates (x,y) for all pieces on the board of the given color.
        (1 for white, -1 for black, 0 for empty spaces) """
        squares=[]
        for y in range(8):
            for x in range(8):
                if self.board[x][y]==(player+1):
                    squares.append((x,y))
        return squares



def alpha_beta_minimax(board, time_constrain):
    best_value = -10000
    moves = board.get_legal_moves()
    best_move = None

    alpha = MINIMUM
    beta = MAXIMUM

    end_time = time.time() + time_constrain

    while time.time() < end_time:
        for move in moves:
            tempBoard = deepcopy(board)
            tempBoard.move = move
            tempBoard.make_move()
            score = alpha_beta_search(tempBoard, 0, alpha, beta, False)

            if score > best_value:
                best_value = score
                best_move = move
            alpha = max(alpha, best_value)

            if beta <= alpha:
                break
        break
        
    if best_move == None:
        best_move = random.choice(moves)
    return best_move

def alpha_beta_search(board, depth, alpha, beta, player):
    
    if depth == MAX_DEPTH:
        return board_value(board)
        return calculate_heuristics(board, player)
    
    moves = board.get_legal_moves()
    if player:
        best = MINIMUM        
        for m in moves:
            trvBoard = deepcopy(board)
            trvBoard.move = m
            trvBoard.make_move()
            value = alpha_beta_search(trvBoard, depth + 1, alpha, beta, False)
            best = max(best, value)
            alpha = max(alpha, value)
            if beta <= alpha:
                break
        return best
    else:
        best = MAXIMUM
        for m in moves:
            trvBoard = deepcopy(board)
            trvBoard.move = m
            trvBoard.make_move()
            value = alpha_beta_search(trvBoard, depth + 1, alpha, beta, True)
            best = min(best, value)
            beta = min(beta, value)
            if beta <= alpha:
                break
        return best

def board_value(state):
    player = state.current_player + 1
    enemy = 2 - player

    player_num = 0
    enemy_num = 0
    player_front = 0
    enemy_front = 0

    p = 0
    c = 0
    l = 0
    m = 0
    f = 0
    d = 0

    X1 = [-1, -1, 0, 1, 1, 1, 0, -1]
    Y1 = [0, 1, 1, 1, 0, -1, -1, -1]

    V = [
            [20, -3, 11, 8, 8, 11, -3, 20],
            [-3, -7, -4, 1, 1, -4, -7, -3],
            [11, -4, 2, 2, 2, 2, -4, 11],
            [8, 1, 2, -3, -3, 2, 1, 8],
            [8, 1, 2, -3, -3, 2, 1, 8],
            [11, -4, 2, 2, 2, 2, -4, 11],
            [-3, -7, -4, 1, 1, -4, -7, -3],
            [20, -3, 11, 8, 8, 11, -3, 20]
        ]
    
    # Step 1
    for i in range(state.n):
        for j in range(state.n):
            if state.board[i][j] == player:
                d += V[i][j]
                player_num += 1
            elif state.board[i][j] == enemy:
                d -= V[i][j]
                enemy_num += 1

            if state.board[i][j] != 0:
                for k in range(8):
                    x = i + X1[k]
                    y = j + Y1[k]
                    if x >= 0 and x < 8 and y >= 0 and y < 8 and state.board[x][y] == 0:
                        if state.board[i][j] == player:
                            player_front += 1
                        else:
                            enemy_front += 1
                        break
    
    # Step 2
    if player_num > enemy_num:
        p = (100.0 * player_num) / (player_num + enemy_num)
    elif player_num < enemy_num:
        p = -(100.0 * enemy_num) / (player_num + enemy_num)
    else:
        p = 0

    # Step 3
    if player_front > enemy_front:
        f = -(100.0 * player_front) / (player_front + enemy_front)
    elif player_front < enemy_front:
        f = (100.0 * enemy_front) / (player_front + enemy_front)
    else:
        f = 0

    # Step 4
    player_num = enemy_num = 0
    if state.board[0][0] == player:
        player_num += 1
    elif state.board[0][0] == enemy:
        enemy_num += 1
    if state.board[0][7] == player:
        player_num += 1
    elif state.board[0][7] == enemy:
        enemy_num += 1
    if state.board[7][0] == player:
        player_num += 1
    elif state.board[7][0] == enemy:
        enemy_num += 1
    if state.board[7][7] == player:
        player_num += 1
    elif state.board[7][7] == enemy:
        enemy_num += 1
    c = 25 * (player_num - enemy_num)

    # Step 5
    player_num = enemy_num = 0
    if state.board[0][0] == 0:
        if state.board[0][1] == player:
            player_num += 1
        elif state.board[0][1] == enemy:
            enemy_num += 1
        if state.board[1][1] == player:
            player_num += 1
        elif state.board[1][1] == enemy:
            enemy_num += 1
        if state.board[1][0] == player:
            player_num += 1
        elif state.board[1][0] == enemy:
            enemy_num += 1

    if state.board[0][7] == 0:
        if state.board[0][6] == player:
            player_num += 1
        elif state.board[0][6] == enemy:
            enemy_num += 1
        if state.board[1][6] == player:
            player_num += 1
        elif state.board[1][6] == enemy:
            enemy_num += 1
        if state.board[1][7] == player:
            player_num += 1
        elif state.board[1][7] == enemy:
            enemy_num += 1

    if state.board[7][0] == 0:
        if state.board[7][1] == player:
            player_num += 1
        elif state.board[7][1] == enemy:
            enemy_num += 1
        if state.board[6][1] == player:
            player_num += 1
        elif state.board[6][1] == enemy:
            enemy_num += 1
        if state.board[6][0] == player:
            player_num += 1
        elif state.board[6][0] == enemy:
            enemy_num += 1

    if state.board[7][7] == 0:
        if state.board[6][7] == player:
            player_num += 1
        elif state.board[6][7] == enemy:
            enemy_num += 1
        if state.board[6][6] == player:
            player_num += 1
        elif state.board[6][6] == enemy:
            enemy_num += 1
        if state.board[7][6] == player:
            player_num += 1
        elif state.board[7][6] == enemy:
            enemy_num += 1

    l = -12.5 * (player_num - enemy_num)

    # Step 6
    player_num = enemy_num = 0
    if state.make_move() == []:
        player_moves = state.make_move()
        player_num = len(player_moves)

    temp = deepcopy(state)
    temp.current_player = enemy - 1
    if temp.make_move() == []:
        enemy_moves = temp.make_move()
        enemy_num = len(enemy_moves)
    if player_num > enemy_num:
        m = (100.0 * player_num)/(player_num + enemy_num)
    elif player_num < enemy_num:
        m = -(100.0 * enemy_num)/(player_num + enemy_num)
    else:
        m = 0

    return (10 * p) + (801.724 * c) + (382.026 * l) + \
               (78.922 * m) + (74.396 * f) + (10 * d)

def calculate_heuristics(board, player):

    #print "IN calculate_heuristics"
    #calculating the heuristics based on the following 4 components:
    #1) mobility
    #2) stability
    #3) corners
    #4) coin parity
    
    #for mobility
    max_player_moves = board.get_legal_moves()
    
    #print_moves(max_player_moves)
    # print "init-board: \n"
    # self.display(board)
    max_player_mobility = len(max_player_moves)
    #print "len: max_mob: "+str(max_player_mobility)
    
    min_player_mobility = float('inf')
    num_min_player_moves = 0

    for move in max_player_moves:

        newboard_mob = deepcopy(board)
        newboard_mob.move = move
        newboard_mob.make_move()
        newboard_mob.current_player = 1 - player
        
        min_player_moves = newboard_mob.get_legal_moves()
        # print "Min-player-moves"
        # print_moves(min_player_moves)

        num_min_player_moves = len(min_player_moves)

        if(num_min_player_moves < min_player_mobility):
            min_player_mobility = num_min_player_moves

    # print "Min-Player_mob: "+str(min_player_mobility)
    # print "MAX-Player_mob: "+str(max_player_mobility)

    if(max_player_mobility + min_player_mobility != 0):
        actual_mobility = 10000*( max_player_mobility - min_player_mobility )/( max_player_mobility + min_player_mobility )
    else:
        actual_mobility = 0


    #corners captured

    newboard_corner = deepcopy(board)
    all_corners = [(0,0),(7,7), (0,7), (7,0)]
    potential_corners = [(0,2),(2,0),(5,0),(0,5),(5,7),(7,5),(2,7),(7,2)]
    tobe_potential_corners = [(5,5),(5,2),(2,5),(2,2)]
    unlikely_corners = [(6,1),(6,6),(1,1),(1,6),(1,7),(7,1),(0,6),(6,0),(6,7),(7,6),(1,0),(0,1)]
    max_corner_count = 0
    min_corner_count = 0
    max_potential_corners = 0
    min_potential_corners = 0
    max_tobe_potential_corners = 0
    min_tobe_potential_corners = 0

    min_unlikely_corners = 0
    max_unlikely_corners = 0

    cood_max_squares = newboard_corner.get_squares(player)
    cood_min_squares = newboard_corner.get_squares(1-player)

    # print "min: "
    # print cood_min_squares
    # print "max: "
    # print cood_max_squares

    for cord_max in cood_max_squares:
        if cord_max in all_corners:   
            max_corner_count +=3
        if cord_max in potential_corners:
            max_potential_corners += 2
        if cord_max in tobe_potential_corners:
            max_tobe_potential_corners +=1

    for cord_min in cood_min_squares:
        if cord_min in all_corners:
            min_corner_count +=3
        if cord_min in potential_corners:
            min_potential_corners += 2
        if cord_min in tobe_potential_corners:
            min_tobe_potential_corners +=1

    total_max_corners = max_corner_count + max_potential_corners + max_tobe_potential_corners
    total_min_corners = min_corner_count + min_potential_corners + min_tobe_potential_corners

    # if (max_corner_count > 0):
    #     print "max: "+str(max_corner_count )

    # if(min_corner_count > 0):
    #     print "min: "+str(min_corner_count)

    # print "max-corners"+str(max_corner_count)
    # print "min-corners"+str(min_corner_count)
    
    if(total_max_corners + total_min_corners != 0):
        corner_heuristic = 10000*(( total_max_corners - total_max_corners )/( total_min_corners + total_max_corners ))
    else:
        corner_heuristic = 0

    #print "actual_mobility: "+str(actual_mobility)

    if(corner_heuristic != 0):
        return (actual_mobility + corner_heuristic)/2
    else: 
        return actual_mobility

MOVE_DIRS = [(-1, -1), (-1, 0), (-1, +1),
             (0, -1),           (0, +1),
             (+1, -1), (+1, 0), (+1, +1)]

class Othello(Board):
   

    def __init__(self, n = 8):
        turtle.title("OTHELLO")
        Board.__init__(self, n)
        self.current_player = 0
        self.num_tiles = [2, 2]
        self.ai = True
        self.player_go_first = False
        self.time_limit = 3
        self.time_start = 0
        self.time_end = 0

    def initialize_board(self):
        
        if self.n < 2:
            return

        coord1 = int(self.n / 2 - 1)
        coord2 = int(self.n / 2)
        initial_squares = [(coord1, coord2), (coord1, coord1),
                           (coord2, coord1), (coord2, coord2)]
        
        for i in range(len(initial_squares)):
            color = i % 2
            row = initial_squares[i][0]
            col = initial_squares[i][1]
            self.board[row][col] = color + 1
            self.draw_tile(initial_squares[i], color)
    
    def make_move(self):
       
        if self.is_legal_move(self.move):
            self.board[self.move[0]][self.move[1]] = self.current_player + 1
            self.num_tiles[self.current_player] += 1
            self.draw_tile(self.move, self.current_player)
            self.flip_tiles()
    
    def flip_tiles(self):
        
        curr_tile = self.current_player + 1 
        for direction in MOVE_DIRS:
            if self.has_tile_to_flip(self.move, direction):
                i = 1
                while True:
                    row = self.move[0] + direction[0] * i
                    col = self.move[1] + direction[1] * i
                    if self.board[row][col] == curr_tile:
                        break
                    else:
                        self.board[row][col] = curr_tile
                        self.num_tiles[self.current_player] += 1
                        self.num_tiles[(self.current_player + 1) % 2] -= 1
                        self.draw_tile((row, col), self.current_player)
                        i += 1

    def has_tile_to_flip(self, move, direction):
       
        i = 1
        if self.current_player in (0, 1) and \
           self.is_valid_coord(move[0], move[1]):
            curr_tile = self.current_player + 1
            while True:
                row = move[0] + direction[0] * i
                col = move[1] + direction[1] * i
                if not self.is_valid_coord(row, col) or \
                    self.board[row][col] == 0:
                    return False
                elif self.board[row][col] == curr_tile:
                    break
                else:
                    i += 1
        return i > 1

    def has_legal_move(self):
        
        for row in range(self.n):
            for col in range(self.n):
                move = (row, col)
                if self.is_legal_move(move):
                    return True
        return False
    
    def get_legal_moves(self):
        
        moves = []
        for row in range(self.n):
            for col in range(self.n):
                move = (row, col)
                if self.is_legal_move(move):
                    moves.append(move)
        return moves

    def is_legal_move(self, move):
       
        if move != () and self.is_valid_coord(move[0], move[1]) \
           and self.board[move[0]][move[1]] == 0:
            for direction in MOVE_DIRS:
                if self.has_tile_to_flip(move, direction):
                    return True
        return False

    def is_valid_coord(self, row, col):
       
        if 0 <= row < self.n and 0 <= col < self.n:
            return True
        return False
    

    def run(self):
        
        if self.current_player not in (0, 1):
            print('Error: unknown player. Quit...')
            return
        
        if not self.player_go_first:
            self.current_player = 1
            print('Computer\'s turn.')
            self.make_random_move()

        self.current_player = 0
        print('Your turn.')
        if self.ai:
            self.time_start = time.time()
            # temp = StateHolder(self.board, self.current_player)
            move = self.select_move(self.board, self.current_player, self.time_limit)
            self.time_end = time.time()
            # move = alpha_beta_minimax(temp, self.time_limit)
            self.play(move[0], move[1])
        else:
            turtle.onscreenclick(self.play)
        turtle.mainloop()

    def play(self, x, y):
        
        if self.has_legal_move():
            if self.ai:
                self.move = (x,y)
            else:
                self.get_coord(x, y)
            if self.is_legal_move(self.move):
                turtle.onscreenclick(None)
                self.make_move()
            else:
                return

       
        while True:
            print(self.time_end - self.time_start)
            self.current_player = 1
            if self.has_legal_move():
                print('Computer\'s turn.')
                self.make_random_move()
                self.current_player = 0
                if self.has_legal_move():  
                    break
            else:
                break
        
        
        self.current_player = 0

        
        if not self.has_legal_move() or sum(self.num_tiles) == self.n ** 2:
            turtle.onscreenclick(None)
            print('-----------')
            self.report_result()
            name = input('Enter your name for posterity\n')
            if not score.update_scores(name, self.num_tiles[0]):
                print('Your score has not been saved.')
            print('Thanks for playing Othello!')
            close = input('Close the game screen? Y/N\n')
            if close == 'Y':
                turtle.bye()
            elif close != 'N':
                print('Quit in 3s...')
                turtle.ontimer(turtle.bye, 3000)
        else:
            print('Your turn.')
            if self.ai:
                self.time_start = time.time()
                # temp = StateHolder(self.board, self.current_player)
                # move = alpha_beta_minimax(temp, 1)
                move = self.select_move(self.board, self.current_player, self.time_limit)
                self.time_end = time.time()
                self.play(move[0], move[1])
            else:
                turtle.onscreenclick(self.play)
        
    def make_random_move(self):
       
        moves = self.get_legal_moves()
        if moves:
            self.move = random.choice(moves)
            self.make_move()

    def report_result(self):
       
        print('GAME OVER!!')
        if self.num_tiles[0] > self.num_tiles[1]:
            print('YOU WIN!!',
                  'You have %d tiles, but the computer only has %d!' 
                  % (self.num_tiles[0], self.num_tiles[1]))
        elif self.num_tiles[0] < self.num_tiles[1]:
            print('YOU LOSE...',
                  'The computer has %d tiles, but you only have %d :(' 
                  % (self.num_tiles[1], self.num_tiles[0]))
        else:
            print("IT'S A TIE!! There are %d of each!" % self.num_tiles[0])
    
    def __str__(self):
     
        player_str = 'Current player: ' + str(self.current_player + 1) + '\n'
        num_tiles_str = '# of black tiles -- 1: ' + str(self.num_tiles[0]) + \
                        '\n' + '# of white tiles -- 2: ' + \
                        str(self.num_tiles[1]) + '\n'
        board_str = Board.__str__(self)
        printable_str = player_str + num_tiles_str + board_str

        return printable_str

    def __eq__(self, other):
       
        return Board.__eq__(self, other) and self.current_player == \
        other.current_player
    
def select_move(cur_state, player_to_move, remain_time):
    temp = StateHolder(cur_state, player_to_move)
    return alpha_beta_minimax(temp, remain_time)