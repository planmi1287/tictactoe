import argparse


class Game:
    def __init__(self, length) -> None:
        self.result = []
        self.finished = False
        self.length = length
        self.marks_amount = 0
        self.max_marks = length**2
        self.board: list[list[str]] = [['']*length for i in range(length)]
        

    def place_mark(self, mark: str, row: int, column: int) -> int:
        # RETURN -1 == INVALID MOVE
        # RETURN  0 == GAME FINISHED
        # RETURN  1 == VALID MOVE
        
        # check if not out of bounds
        if not 0 <= row < self.length or not 0 <= column < self.length:
            return -1
        # you can't override a mark
        if not self.board[row][column] == '':
            return -1

        self.board[row][column] = mark
        self.marks_amount += 1
        if self.__check_win() is True:
            return 0
        return 1


    def draw_board(self) -> None:
        l = self.length
        # print coordinates
        print(' ', end=' ')
        for i in range(l):
            print(i, end=' ')
        print()

        for i in range(l):
            print(i, end=' ')
            for j in range(l):
                if self.board[i][j] == '':
                    print('-', end=' ')
                else:
                    print(self.board[i][j], end=' ')
            print()


    def __check_win(self) -> bool:
        # check for draw
        if self.marks_amount == self.max_marks:
            self.__set_result('draw', None, None)
            return True
        
        # check horizontal
        for row in self.board:
            if set(row) == {'X'}:
                self.__set_result('win', 'X', 'horizontal')
                return True
            elif set(row) == {'O'}:
                self.__set_result('win', 'O', 'horizontal')
                return True
        
        # check vertical
        for i in range(self.length):
            tmp = set()
            for j in range(self.length):
                tmp.add(self.board[j][i])
            if tmp == {'X'}:
                self.__set_result('win', 'X', 'vertical')
                return True
            elif tmp == {'O'}:
                self.__set_result('win', 'O', 'horizontal')
                return True
        
        # check diagonal
        # top left to bottom right
        tmp = set()
        for i in range(self.length):
            tmp.add(self.board[i][i])
        if tmp == {'X'}:
            self.__set_result('win', 'X', 'diagonal')
            return True
        elif tmp == {'O'}:
            self.__set_result('win', 'O', 'diagonal')
            return True
            
        # top right to bottom left
        tmp = set()
        for i in range(self.length):
            tmp.add(self.board[self.length-1-i][i])
        if tmp == {'X'}:
            self.__set_result('win', 'X', 'diagonal')
            return True
        elif tmp == {'O'}:
            self.__set_result('win', 'O', 'diagonal')
            return True

        return False

    
    def __set_result(self, res: str, winner: str|None, line_type: str|None) -> None:
        if res == 'draw':
            self.result = ['DRAW', None, None, self.marks_amount]
        elif res == 'win':
            self.result = ['WON', winner, line_type, self.marks_amount]

# clean console util
def cleancon():
    print('\n'*1000)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        prog='tictactoe',
        description='Play a game of Tic-tac-toe!'
    )
    parser.add_argument('-gs', '--gridsize', type=int, metavar='N',help='Specify the grid dimensions (NxN)', default=3)
    args = parser.parse_args()

    game = Game(args.gridsize)
    
    

    cm = 'X' # current move tracker, X begins
    while True:
        cleancon()
        game.draw_board()
        print(f'Player {cm} turn')
        while True:
            command = input(f'Type in \'place <row> <col>\' to place your mark or \'quit\' to exit: ')
            match command.rstrip().split():
                case ['quit']:
                    print('Quitting...')
                    exit()
                case ['place', row, col]:
                    valid_mark = game.place_mark(cm, int(row), int(col))
                    if valid_mark == 1:
                        break
                    elif valid_mark == 0:
                        cleancon()
                        game.draw_board()
                        
                        final_res = game.result
                        print('Game finished.')
                        if final_res[0] == 'DRAW':
                            print(f'Game has ended with a DRAW after {final_res[3]} moves.')
                        else:
                            print(f'Game has been WON by {final_res[1]} with a {final_res[2]} line, after {final_res[3]} moves')
                        quit()
                    else:
                        print('Invalid argument(s).')
                case _:
                    print('Invalid command.')
        if cm == 'X':
            cm = 'O'
        else:
            cm = 'X'
