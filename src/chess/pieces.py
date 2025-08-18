from typing import List, Optional, Tuple, Union, Any


class Piece:
    def __init__(self, color: str) -> None:
        self.color: str = color

    def symbol(self) -> str:
        return "?"

    def valid_moves(self, pos: Tuple[int, int], board: List[List[Any]], *args: Any, **kwargs: Any) -> List[Tuple[int, int]]:
        return []


class King(Piece):
    def __init__(self, color: str) -> None:
        super().__init__(color)
        self.has_moved: bool = False

    def symbol(self) -> str:
        return "♔" if self.color == "white" else "♚"

    def valid_moves(self, pos: Tuple[int, int], board: List[List[Any]], can_castle_kingside: bool = True, can_castle_queenside: bool = True) -> List[Tuple[int, int]]:
        moves: List[Tuple[int, int]] = []
        x, y = pos
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if dx == 0 and dy == 0:
                    continue
                nx, ny = x + dx, y + dy
                if 0 <= nx < 8 and 0 <= ny < 8:
                    target = board[nx][ny]
                    if not target or target.color != self.color:
                        moves.append((nx, ny))
        # Castling
        if not self.has_moved and x in [0, 7] and y == 4:
            row = x
            # Kingside
            if can_castle_kingside and isinstance(board[row][7], Rook) and not board[row][7].has_moved:
                if all(board[row][col] is None for col in [5, 6]):
                    moves.append((row, 6))
            # Queenside
            if can_castle_queenside and isinstance(board[row][0], Rook) and not board[row][0].has_moved:
                if all(board[row][col] is None for col in [1, 2, 3]):
                    moves.append((row, 2))
        return moves


class Queen(Piece):
    def symbol(self) -> str:
        return "♕" if self.color == "white" else "♛"

    def valid_moves(self, pos: Tuple[int, int], board: List[List[Any]], *args: Any, **kwargs: Any) -> List[Tuple[int, int]]:
        return Rook(self.color).valid_moves(pos, board) + Bishop(self.color).valid_moves(pos, board)


class Rook(Piece):
    def __init__(self, color: str) -> None:
        super().__init__(color)
        self.has_moved: bool = False

    def symbol(self) -> str:
        return "♖" if self.color == "white" else "♜"

    def valid_moves(self, pos: Tuple[int, int], board: List[List[Any]], *args: Any, **kwargs: Any) -> List[Tuple[int, int]]:
        moves: List[Tuple[int, int]] = []
        x, y = pos
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = x, y
            while True:
                nx += dx
                ny += dy
                if 0 <= nx < 8 and 0 <= ny < 8:
                    target = board[nx][ny]
                    if not target:
                        moves.append((nx, ny))
                    elif target.color != self.color:
                        moves.append((nx, ny))
                        break
                    else:
                        break
                else:
                    break
        return moves


class Bishop(Piece):
    def symbol(self) -> str:
        return "♗" if self.color == "white" else "♝"

    def valid_moves(self, pos: Tuple[int, int], board: List[List[Any]], *args: Any, **kwargs: Any) -> List[Tuple[int, int]]:
        moves: List[Tuple[int, int]] = []
        x, y = pos
        for dx, dy in [(-1, -1), (-1, 1), (1, -1), (1, 1)]:
            nx, ny = x, y
            while True:
                nx += dx
                ny += dy
                if 0 <= nx < 8 and 0 <= ny < 8:
                    target = board[nx][ny]
                    if not target:
                        moves.append((nx, ny))
                    elif target.color != self.color:
                        moves.append((nx, ny))
                        break
                    else:
                        break
                else:
                    break
        return moves


class Knight(Piece):
    def symbol(self) -> str:
        return "♘" if self.color == "white" else "♞"

    def valid_moves(self, pos: Tuple[int, int], board: List[List[Any]], *args: Any, **kwargs: Any) -> List[Tuple[int, int]]:
        moves: List[Tuple[int, int]] = []
        x, y = pos
        for dx, dy in [(-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < 8 and 0 <= ny < 8:
                target = board[nx][ny]
                if not target or target.color != self.color:
                    moves.append((nx, ny))
        return moves


class Pawn(Piece):
    def symbol(self) -> str:
        return "♙" if self.color == "white" else "♟"

    def valid_moves(self, pos: Tuple[int, int], board: List[List[Any]], en_passant_target: Optional[Tuple[int, int]] = None, *args: Any, **kwargs: Any) -> List[Tuple[int, int]]:
        moves: List[Tuple[int, int]] = []
        x, y = pos
        direction = -1 if self.color == "white" else 1
        start_row = 6 if self.color == "white" else 1
        # Move forward
        if 0 <= x + direction < 8 and not board[x + direction][y]:
            moves.append((x + direction, y))
            # Double move from start
            if x == start_row and not board[x + 2 * direction][y]:
                moves.append((x + 2 * direction, y))
        # Captures
        for dy in [-1, 1]:
            nx, ny = x + direction, y + dy
            if 0 <= nx < 8 and 0 <= ny < 8:
                target = board[nx][ny]
                if target and target.color != self.color:
                    moves.append((nx, ny))
        # En passant
        if en_passant_target:
            ex, ey = en_passant_target
            if x == (3 if self.color == "white" else 4) and abs(ey - y) == 1 and ex == x + direction:
                moves.append((ex, ey))
        return moves
