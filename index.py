import turtle
import random
from rand import rand
from minimax import *
import time


SQUARE = 50
TILE = 20
BOARD_COLOR = 'green'
LINE_COLOR = 'white'
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
        return

        turtle.setup(self.n * self.square_size + self.square_size,
                     self.n * self.square_size + self.square_size)
        turtle.screensize(self.n * self.square_size, self.n * self.square_size)
        turtle.bgcolor('white')

        othello = turtle.Turtle(visible=False)
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
        return
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
        return
        pos = self.get_tile_start_pos(square)
        if pos:
            coord = pos[0]
            r = pos[1]
        else:
            print('Error drawing the tile...')
            return

        tile = turtle.Turtle(visible=False)
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


SCORE_FILE = 'scores.txt'


def read_scores(filename=SCORE_FILE):

    try:
        infile = open(filename, 'r')
        data = infile.read()
        infile.close()
        return data
    except FileNotFoundError:
        return ''
    except OSError:
        print('Error reading the score file.')
        return


def write_scores(new_data, filename=SCORE_FILE, mode='a'):

    try:
        outfile = open(filename, mode)
        outfile.write(new_data)
        outfile.close()
    except OSError:
        print('Error updating the score file.')
        return ''


def update_scores(name, score, filename=SCORE_FILE):

    new_record = name + ' ' + str(score)
    new_data = new_record + '\n'
    scores_data = read_scores(filename)

    if scores_data == None:
        return ''

    if scores_data:
        records = scores_data.splitlines()
        high_scorer = records[0].rsplit(' ', 1)
        try:
            highest_score = int(high_scorer[1])
            if score > highest_score:
                scores_data = new_data + scores_data
                if write_scores(scores_data, filename, 'w') == '':
                    return ''
                else:
                    return new_record
        except ValueError:
            print('Unknown format for the score file.')
            return ''
        if scores_data[-1] != '\n':
            new_data = '\n' + new_data

    if write_scores(new_data, filename) == '':
        return ''
    else:
        return new_record


MOVE_DIRS = [(-1, -1), (-1, 0), (-1, +1),
             (0, -1),           (0, +1),
             (+1, -1), (+1, 0), (+1, +1)]

def select_move_by_mode(mode, cur_state, player_to_move, remain_time = 60):
    if mode == 1: # random
        return rand(cur_state, player_to_move)
    elif mode == 2: # simple table
        return select_move(cur_state, player_to_move, remain_time, evaluate_simple_table)
    elif mode == 3: # good bad evaluate
        return select_move(cur_state, player_to_move, remain_time, evaluate_goodbad)
    elif mode == 4: # corner table
        return select_move(cur_state, player_to_move, remain_time, evaluate_corner)
    
    raise Exception("wrong mode id")
    

class Othello(Board):

    def __init__(self, n=8):
        # turtle.title("OTHELLO")
        Board.__init__(self, n)
        self.n = n
        self.current_player = 1
        self.num_tiles = [2, 2]

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
            if color == 0:
                self.board[row][col] = 1
            else:
                self.board[row][col] = -1
            
            self.draw_tile(initial_squares[i], color)

    def make_move(self):

        if self.is_legal_move(self.move):
            self.board[self.move[0]][self.move[1]] = self.current_player
            self.num_tiles[self.current_player] += 1
            color =  0 if self.current_player == 1 else 1
            self.draw_tile(self.move, color)
            self.flip_tiles()

    def flip_tiles(self):

        curr_tile = self.current_player
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
                        self.num_tiles[self.current_player*-1] -= 1
                        color =  0 if self.current_player == 1 else 1
                        self.draw_tile((row, col), color)
                        i += 1

    def has_tile_to_flip(self, move, direction):

        i = 1
        if self.current_player in (-1, 1) and \
           self.is_valid_coord(move[0], move[1]):
            curr_tile = self.current_player
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

    def playingTurn(self, mode, cur_state, player_to_move, remain_time = 60):
        if player_to_move == 1:
            print("Player 1's turn:")
        else:
            print("Player 2's turn:")

        time_amount = 0
        if self.has_legal_move():
            start_time = time.perf_counter()
            self.move = select_move_by_mode(mode, cur_state, player_to_move, remain_time)
            end_time = time.perf_counter()
            time_amount = end_time - start_time
            print("time: ", time_amount)
            if time_amount > 3:
                raise Exception("time limit is 3s")
            if time_amount > remain_time:
                raise Exception("total time limit is 60s")

            print(self.move)
            self.make_move()
            print("table:")
            print("    0  1  2  3  4  5  6  7")
            for i, row in enumerate(self.board):
                strow = str(i) + "   "
                for j, tale in enumerate(row):
                    if i == self.move[0] and j == self.move[1]:
                        if tale == -1:
                            strow += "O  "
                        elif tale == 1:
                            strow += "X  "
                        else:
                            strow += "_  "
                    else:
                        if tale == -1:
                            strow += "o  "
                        elif tale == 1:
                            strow += "x  "
                        else:
                            strow += "_  "
                print(strow)
        else: 
            print('no legal move.')
        print("=============================")
        return time_amount

    def run1(self, mode1, mode2):
        num_moves = 60
        if self.current_player not in (-1, 1):
            print('Error: unknown player. Quit...')
            return
        print("Game started:")
        print("    0  1  2  3  4  5  6  7")
        for i, row in enumerate(self.board):
            strow = str(i) + "   "
            for j, tale in enumerate(row):
                if tale == -1:
                    strow += "o  "
                elif tale == 1:
                    strow += "x  "
                else:
                    strow += "_  "
            print(strow)
        print("=============================")

        self.current_player = 1
        time_left_0 = 60
        time_left_1 = 60
        for i in range(num_moves):
            if self.current_player == 1:
                time_amount = self.playingTurn(mode1, self.board, 1, time_left_0)
                time_left_0 -= time_amount
            else:
                time_amount = self.playingTurn(mode2, self.board, -1, time_left_1)
                time_left_1 -= time_amount
            self.current_player = -self.current_player

        print("=============================")
        print("Result: ", count_elements(self.board))
        

    def play(self, x, y):

        if self.has_legal_move():
            self.get_coord(x, y)
            if self.is_legal_move(self.move):
                self.make_move()
            else:
                return

        while True:
            self.current_player = -1
            if self.has_legal_move():
                print('Computer\'s turn.')
                self.move = rand(self.board, -1)
                self.make_move()
                self.current_player = 1
                if self.has_legal_move():
                    break
            else:
                break

        self.current_player = 1

        if not self.has_legal_move() or sum(self.num_tiles) == self.n ** 2:
            turtle.onscreenclick(None)
            print('-----------')
            self.report_result()
            name = input('Enter your name for posterity\n')
            if not update_scores(name, self.num_tiles[1]):
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
            turtle.onscreenclick(self.play)

    def make_random_move(self):

        moves = self.get_legal_moves()
        print(moves)
        if moves:
            self.move = random.choice(moves)
            print(self.move)
            self.make_move()

    def report_result(self):
        print(count_elements(self.board))
        return
        print('GAME OVER!!')
        if self.num_tiles[1] > self.num_tiles[-1]:
            print('YOU WIN!!',
                  'You have %d tiles, but the computer only has %d!'
                  % (self.num_tiles[1], self.num_tiles[-1]))
        elif self.num_tiles[1] < self.num_tiles[-1]:
            print('YOU LOSE...',
                  'The computer has %d tiles, but you only have %d :('
                  % (self.num_tiles[-1], self.num_tiles[1]))
        else:
            print("IT'S A TIE!! There are %d of each!" % self.num_tiles[1])

    def __str__(self):

        player_str = 'Current player: ' + str(self.current_player + 1) + '\n'
        num_tiles_str = '# of black tiles -- 1: ' + str(self.num_tiles[1]) + \
                        '\n' + '# of white tiles -- 2: ' + \
                        str(self.num_tiles[-1]) + '\n'
        board_str = Board.__str__(self)
        printable_str = player_str + num_tiles_str + board_str

        return printable_str

    def __eq__(self, other):

        return Board.__eq__(self, other) and self.current_player == \
            other.current_player


def main():
    # method_choice = int(
    #     input("Nhap method (Tu choi: 0, Choi tay: 1): "))
    # algorithm = int(
    #     input("Nhap method (Rand: 0): "))

    game = Othello()
    #game.draw_board()
    game.initialize_board()
    print("Mode list:")
    print("1. Random algorithm")
    print("2. Simple table algorithm")
    print("3. Good and bad algorithm")
    print("4. Corner algorithm")
    print("---------------------")
    mode1 = int(input("Enter mode id for player 1: "))
    mode2 = int(input("Enter mode id for player 2: "))
    game.run1(mode1, mode2)

def count_elements(lst):
    count_1 = 0
    count_minus_1 = 0

    for row in lst:
        for num in row:
            if num == 1:
                count_1 += 1
            elif num == -1:
                count_minus_1 += 1

    return count_1, count_minus_1

main()
