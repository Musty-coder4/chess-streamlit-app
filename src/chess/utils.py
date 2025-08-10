def validate_move(start_pos, end_pos, board):
    """
    Validate a move from start_pos to end_pos on the given board.
    Assumes board is an 8x8 list of lists, with each piece represented as a string,
    e.g., 'wP' for white pawn, 'bK' for black king, or '' for empty.
    Returns True if the move is valid, False otherwise.
    """
    def in_bounds(pos):
        row, col = pos
        return 0 <= row < 8 and 0 <= col < 8

    if not (in_bounds(start_pos) and in_bounds(end_pos)):
        return False

    piece = board[start_pos[0]][start_pos[1]]
    if not piece:
        return False  # No piece at start

    color, ptype = piece[0], piece[1]
    target = board[end_pos[0]][end_pos[1]]
    if target and target[0] == color:
        return False  # Can't capture own piece

    dr, dc = end_pos[0] - start_pos[0], end_pos[1] - start_pos[1]

    if ptype == 'P':  # Pawn
        direction = -1 if color == 'w' else 1
        start_row = 6 if color == 'w' else 1
        # Move forward
        if dc == 0 and dr == direction and not target:
            return True
        # Double move from starting position
        if dc == 0 and dr == 2 * direction and start_pos[0] == start_row and not target and not board[start_pos[0] + direction][start_pos[1]]:
            return True
        # Capture
        if abs(dc) == 1 and dr == direction and target and target[0] != color:
            return True
        return False

    if ptype == 'R':  # Rook
        if dr == 0 or dc == 0:
            step_r = (dr > 0) - (dr < 0)
            step_c = (dc > 0) - (dc < 0)
            r, c = start_pos[0] + step_r, start_pos[1] + step_c
            while (r, c) != end_pos:
                if board[r][c]:
                    return False
                r += step_r
                c += step_c
            return True
        return False

    if ptype == 'N':  # Knight
        if (abs(dr), abs(dc)) in [(2, 1), (1, 2)]:
            return True
        return False

    if ptype == 'B':  # Bishop
        if abs(dr) == abs(dc):
            step_r = (dr > 0) - (dr < 0)
            step_c = (dc > 0) - (dc < 0)
            r, c = start_pos[0] + step_r, start_pos[1] + step_c
            while (r, c) != end_pos:
                if board[r][c]:
                    return False
                r += step_r
                c += step_c
            return True
        return False

    if ptype == 'Q':  # Queen
        if dr == 0 or dc == 0 or abs(dr) == abs(dc):
            step_r = (dr > 0) - (dr < 0) if dr != 0 else 0
            step_c = (dc > 0) - (dc < 0) if dc != 0 else 0
            r, c = start_pos[0] + step_r, start_pos[1] + step_c
            while (r, c) != end_pos:
                if board[r][c]:
                    return False
                r += step_r
                c += step_c
            return True
        return False

    if ptype == 'K':  # King
        if max(abs(dr), abs(dc)) == 1:
            return True
        # Castling not implemented
        return False

    return False

def convert_coordinates(coord):
    # Convert chessboard coordinates from algebraic notation to array indices
    # e.g., 'e2' -> (6, 4)
    if len(coord) != 2:
        raise ValueError("Invalid coordinate format")
    file, rank = coord[0], coord[1]
    if file not in 'abcdefgh' or rank not in '12345678':
        raise ValueError("Invalid coordinate")
    col = ord(file) - ord('a')
    row = 8 - int(rank)
    return (row, col)

def display_board(board):
    # Create a visual representation of the chessboard
    board_str = "  a b c d e f g h\n"
    for i, row in enumerate(board):
        board_str += str(8 - i) + " "
        for piece in row:
            board_str += (piece if piece else '.') + " "
        board_str += str(8 - i) + "\n"
    board_str += "  a b c d e f g h"
    return board_str

def is_valid_position(pos):
    # Check if the given position is within the bounds of the chessboard
    if not isinstance(pos, (tuple, list)) or len(pos) != 2:
        return False
    row, col = pos
    return 0 <= row < 8 and 0 <= col < 8

def get_piece_at_position(pos, board):
    # Retrieve the piece located at the specified position on the board
    row, col = pos
    if 0 <= row < 8 and 0 <= col < 8:
        return board[row][col]
    return None

def parse_position(pos_str):
    files = "abcdefgh"
    if len(pos_str) != 2:
        return None
    file, rank = pos_str[0], pos_str[1]
    if file in files and rank.isdigit():
        x = 8 - int(rank)
        y = files.index(file)
        if 0 <= x < 8 and 0 <= y < 8:
            return (x, y)
    return None