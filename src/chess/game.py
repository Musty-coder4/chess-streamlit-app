from .board import Board
from .pieces import King, Queen, Rook, Bishop, Knight, Pawn

def is_in_check(board, color):
    king_pos = None
    for i in range(8):
        for j in range(8):
            piece = board[i][j]
            if piece and isinstance(piece, King) and piece.color == color:
                king_pos = (i, j)
                break
    for i in range(8):
        for j in range(8):
            piece = board[i][j]
            if piece and piece.color != color:
                if isinstance(piece, Pawn):
                    moves = piece.valid_moves((i, j), board, None)
                elif isinstance(piece, King):
                    moves = piece.valid_moves((i, j), board, False, False)
                else:
                    moves = piece.valid_moves((i, j), board)
                if king_pos in moves:
                    return True
    return False

class Game:
    def __init__(self):
        self.board = Board()
        self.current_turn = "white"
        self.status = "Game in Progress"
        self.promoting = False
        self.en_passant_target = None
        self.castling_rights = {
            "white": {"kingside": True, "queenside": True},
            "black": {"kingside": True, "queenside": True}
        }

    def move(self, from_pos, to_pos):
        fx, fy = from_pos
        tx, ty = to_pos
        piece = self.board.grid[fx][fy]
        if not piece:
            self.status = "No piece at source."
            return False
        if piece.color != self.current_turn:
            self.status = f"It's {self.current_turn}'s turn."
            return False

        # Determine valid moves with special rules
        valid = []
        special = None
        if isinstance(piece, Pawn):
            valid = piece.valid_moves((fx, fy), self.board.grid, self.en_passant_target)
            # En passant
            if self.en_passant_target and (tx, ty) == self.en_passant_target and fy != ty and self.board.grid[tx][ty] is None:
                special = "en_passant"
        elif isinstance(piece, King):
            can_castle_kingside = self.castling_rights[piece.color]["kingside"]
            can_castle_queenside = self.castling_rights[piece.color]["queenside"]
            valid = piece.valid_moves((fx, fy), self.board.grid, can_castle_kingside, can_castle_queenside)
            # Castling
            if (tx, ty) == (fx, 6):
                special = "castle_kingside"
            elif (tx, ty) == (fx, 2):
                special = "castle_queenside"
        else:
            valid = piece.valid_moves((fx, fy), self.board.grid)

        if (tx, ty) not in valid:
            self.status = "Invalid move for this piece."
            return False

        # Make a copy of the board to test for checks
        import copy
        test_board = copy.deepcopy(self.board.grid)
        if special == "en_passant":
            test_board[tx][ty] = piece
            test_board[fx][fy] = None
            test_board[fx][ty] = None
        elif special == "castle_kingside":
            test_board[fx][6] = piece
            test_board[fx][4] = None
            test_board[fx][5] = test_board[fx][7]
            test_board[fx][7] = None
        elif special == "castle_queenside":
            test_board[fx][2] = piece
            test_board[fx][4] = None
            test_board[fx][3] = test_board[fx][0]
            test_board[fx][0] = None
        else:
            test_board[tx][ty] = piece
            test_board[fx][fy] = None

        if is_in_check(test_board, self.current_turn):
            self.status = "Move would leave king in check."
            return False

        # Move is valid, update castling/en passant rights
        if isinstance(piece, King):
            self.castling_rights[piece.color]["kingside"] = False
            self.castling_rights[piece.color]["queenside"] = False
        if isinstance(piece, Rook):
            if fx == (7 if piece.color == "white" else 0) and fy == 0:
                self.castling_rights[piece.color]["queenside"] = False
            if fx == (7 if piece.color == "white" else 0) and fy == 7:
                self.castling_rights[piece.color]["kingside"] = False

        # Set en passant target
        self.en_passant_target = None
        if isinstance(piece, Pawn) and abs(tx - fx) == 2:
            self.en_passant_target = ((fx + tx) // 2, fy)

        self.board.move_piece(from_pos, to_pos, special)

        # Pawn promotion
        if isinstance(piece, Pawn) and (tx == 0 or tx == 7):
            self.promoting = (tx, ty)
            self.status = "Pawn promotion! Choose piece: Q, R, B, N."
            return True

        # Switch turn
        self.current_turn = "black" if self.current_turn == "white" else "white"
        # Check for checkmate or stalemate
        if self.is_checkmate(self.current_turn):
            self.status = f"Checkmate! {piece.color.capitalize()} wins."
        elif self.is_stalemate(self.current_turn):
            self.status = "Stalemate! Draw."
        else:
            self.status = "Move successful."
        return True

    def promote(self, piece_type):
        if not self.promoting:
            return
        x, y = self.promoting
        color = self.current_turn
        if piece_type == "Q":
            self.board.grid[x][y] = Queen(color)
        elif piece_type == "R":
            self.board.grid[x][y] = Rook(color)
        elif piece_type == "B":
            self.board.grid[x][y] = Bishop(color)
        elif piece_type == "N":
            self.board.grid[x][y] = Knight(color)
        self.promoting = False
        self.current_turn = "black" if self.current_turn == "white" else "white"
        self.status = "Promotion complete."

    def is_checkmate(self, color):
        if not is_in_check(self.board.grid, color):
            return False
        for i in range(8):
            for j in range(8):
                piece = self.board.grid[i][j]
                if piece and piece.color == color:
                    if isinstance(piece, Pawn):
                        moves = piece.valid_moves((i, j), self.board.grid, self.en_passant_target)
                    elif isinstance(piece, King):
                        can_castle_kingside = self.castling_rights[piece.color]["kingside"]
                        can_castle_queenside = self.castling_rights[piece.color]["queenside"]
                        moves = piece.valid_moves((i, j), self.board.grid, can_castle_kingside, can_castle_queenside)
                    else:
                        moves = piece.valid_moves((i, j), self.board.grid)
                    for move in moves:
                        import copy
                        test_board = copy.deepcopy(self.board.grid)
                        fx, fy = i, j
                        tx, ty = move
                        test_board[tx][ty] = piece
                        test_board[fx][fy] = None
                        if not is_in_check(test_board, color):
                            return False
        return True

    def is_stalemate(self, color):
        if is_in_check(self.board.grid, color):
            return False
        for i in range(8):
            for j in range(8):
                piece = self.board.grid[i][j]
                if piece and piece.color == color:
                    if isinstance(piece, Pawn):
                        moves = piece.valid_moves((i, j), self.board.grid, self.en_passant_target)
                    elif isinstance(piece, King):
                        can_castle_kingside = self.castling_rights[piece.color]["kingside"]
                        can_castle_queenside = self.castling_rights[piece.color]["queenside"]
                        moves = piece.valid_moves((i, j), self.board.grid, can_castle_kingside, can_castle_queenside)
                    else:
                        moves = piece.valid_moves((i, j), self.board.grid)
                    for move in moves:
                        import copy
                        test_board = copy.deepcopy(self.board.grid)
                        fx, fy = i, j
                        tx, ty = move
                        test_board[tx][ty] = piece
                        test_board[fx][fy] = None
                        if not is_in_check(test_board, color):
                            return False
        return True

    def get_board_symbols(self):
        return self.board.get_board_symbols()