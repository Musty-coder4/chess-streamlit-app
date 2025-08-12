import json
#R-rook N-knight B-bishop Q-queen K-king P-pawn
board= {
    'a8':'bR', 'b8':'bN', 'c8':'bB', 'd8':'bQ', 'e8':'bK', 'f8':'bB', 'g8':'bN', 'h8':'bR',

    'a7':'bP', 'b7':'bP', 'c7':'bP', 'd7':'bP', 'e7':'bP', 'f7':'bP', 'g7':'bP', 'h7':'bP',

    'a6':None, 'b6':None, 'c6':None, 'd6':None, 'e6':None, 'f6':None, 'g6':None, 'h6':None,

    'a5':None, 'b5':None, 'c5':None, 'd5':None, 'e5':None, 'f5':None, 'g5':None, 'h5':None,

    'a4':None, 'b4':None, 'c4':None, 'd4':None, 'e4':None, 'f4':None, 'g4':None, 'h4':None,

    'a3':None, 'b3':None, 'c3':None, 'd3':None, 'e3':None, 'f3':None, 'g3':None, 'h3':None,

    'a2':'wP', 'b2':'wP', 'c2':'wP', 'd2':'wP', 'e2':'wP', 'f2':'wP', 'g2':'wP', 'h2':'wP',

    'a1':'wR', 'b1':'wN', 'c1':'wB', 'd1':'wQ', 'e1':'wK', 'f1':'wB', 'g1':'wN', 'h1':'wR',
}

def create_empty_board(): #function to create an empty board
    files= ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
    ranks= ['1', '2', '3', '4', '5', '6', '7', '8']
    board= {}
    for rank in ranks:
        for file in files:
            board[file + rank] = None
    return board


def board_setup(): #Function to set the board up for a game
    board= create_empty_board() #call the 'create_empty_board()' function
    files = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']

    board.update({
        'a1': 'wR', 'b1': 'wN', 'c1': 'wB', 'd1': 'wQ', 'e1': 'wK', 'f1': 'wB', 'g1': 'wN', 'h1': 'wR'
    }) #The first row

    for f in files:
        board[f + '2']= 'wP' #For the 7th row filled with white pawns

    board.update({
        'a8': 'bR', 'b8': 'bN', 'c8': 'bB', 'd8': 'bQ', 'e8': 'bK', 'f8': 'bB', 'g8': 'bN', 'h8': 'bR'
    }) #The 8th row
    for f in files:
        board[f + '7']= 'bP' #For the 7th row filled with black pawns

game_data= {
    'board': board_setup(),
    'move_count': 0,
    'w_timer': 0,
    'b_timer': 0
}

def save_game(game_data, filename= 'save.json'):
    with open(filename, 'w') as f:
        json.dump(game_data, f)

def load_game(filename='save.json'):
    with open(filename, 'r') as f:
        return json.load(f)

def reset_game():
    return board_setup()



