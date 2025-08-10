class Piece:
    def __init__(self, color):
        self.color = color

    def legal_moves(self, position, board):
        raise NotImplementedError("This method should be implemented by subclasses.")


class Pawn(Piece):
    def legal_moves(self, position, board):
        # Implement pawn-specific movement logic
        pass


class Rook(Piece):
    def legal_moves(self, position, board):
        # Implement rook-specific movement logic
        pass


class Knight(Piece):
    def legal_moves(self, position, board):
        # Implement knight-specific movement logic
        pass


class Bishop(Piece):
    def legal_moves(self, position, board):
        # Implement bishop-specific movement logic
        pass


class Queen(Piece):
    def legal_moves(self, position, board):
        # Implement queen-specific movement logic
        pass


class King(Piece):
    def legal_moves(self, position, board):
        # Implement king-specific movement logic
        pass