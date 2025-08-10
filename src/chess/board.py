from .pieces import King, Queen, Rook, Bishop, Knight, Pawn

class Board:
    def __init__(self):
        self.grid = self.create_initial_board()
        self.last_move = None  # For en passant

    def create_initial_board(self):
        # 8x8 grid, None for empty
        board = [[None for _ in range(8)] for _ in range(8)]
        # Place pieces for both sides
        # White
        board[7] = [
            Rook("white"), Knight("white"), Bishop("white"), Queen("white"),
            King("white"), Bishop("white"), Knight("white"), Rook("white")
        ]
        board[6] = [Pawn("white") for _ in range(8)]
        # Black
        board[0] = [
            Rook("black"), Knight("black"), Bishop("black"), Queen("black"),
            King("black"), Bishop("black"), Knight("black"), Rook("black")
        ]
        board[1] = [Pawn("black") for _ in range(8)]
        return board

    def move_piece(self, from_pos, to_pos, special=None):
        fx, fy = from_pos
        tx, ty = to_pos
        piece = self.grid[fx][fy]
        # Castling
        if special == "castle_kingside":
            self.grid[tx][ty] = piece
            self.grid[fx][fy] = None
            # Move rook
            self.grid[tx][5] = self.grid[tx][7]
            self.grid[tx][7] = None
            self.grid[tx][6].has_moved = True
            self.grid[tx][5].has_moved = True
        elif special == "castle_queenside":
            self.grid[tx][ty] = piece
            self.grid[fx][fy] = None
            # Move rook
            self.grid[tx][3] = self.grid[tx][0]
            self.grid[tx][0] = None
            self.grid[tx][2].has_moved = True
            self.grid[tx][3].has_moved = True
        elif special == "en_passant":
            self.grid[tx][ty] = piece
            self.grid[fx][fy] = None
            # Remove captured pawn
            self.grid[fx][ty] = None
        else:
            self.grid[tx][ty] = piece
            self.grid[fx][fy] = None
        # Mark as moved
        if hasattr(piece, "has_moved"):
            piece.has_moved = True
        self.last_move = (from_pos, to_pos)

    def get_board_symbols(self):
        symbols = []
        for row in self.grid:
            symbols.append([p.symbol() if p else "." for p in row])
        return symbols