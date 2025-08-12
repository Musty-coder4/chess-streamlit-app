"""
A compact chess engine with move validation, pathControl, check and checkmate detection,
and two simple UI entrypoints: Streamlit (web) and Tkinter (desktop).

How to run:
- Streamlit UI: `streamlit run chess_engine_streamlit_tk.py -- --ui streamlit`
- Tkinter UI: `python chess_engine_streamlit_tk.py --ui tk`

This file is intentionally self-contained and designed for education and prototyping.
"""

from __future__ import annotations
import copy
import sys
import argparse
from typing import List, Tuple, Optional, Dict

# ----------------------------- Chess Engine Core -----------------------------

Position = Tuple[int, int]  # row, col  (0..7)

def in_bounds(pos: Position) -> bool:
    r, c = pos
    return 0 <= r < 8 and 0 <= c < 8

class Piece:
    def __init__(self, color: str):
        assert color in ("w","b")
        self.color = color
        self.symbol = "?"

    def moves_from(self, pos: Position, board: 'Board') -> List[Position]:
        """Return pseudo-legal moves (ignoring checks)."""
        return []

    def __repr__(self):
        return f"{self.symbol if self.color=='w' else self.symbol.lower()}"

class King(Piece):
    def __init__(self, color):
        super().__init__(color)
        self.symbol = "K"

    def moves_from(self, pos, board):
        r,c = pos
        deltas = [(dr,dc) for dr in (-1,0,1) for dc in (-1,0,1) if not (dr==0 and dc==0)]
        moves = []
        for dr,dc in deltas:
            np = (r+dr, c+dc)
            if in_bounds(np):
                target = board.piece_at(np)
                if target is None or target.color != self.color:
                    moves.append(np)
        return moves

class Queen(Piece):
    def __init__(self, color):
        super().__init__(color)
        self.symbol = "Q"
    def moves_from(self,pos,board):
        return sliding_moves(pos, board, self.color, [(1,0),(-1,0),(0,1),(0,-1),(1,1),(1,-1),(-1,1),(-1,-1)])

class Rook(Piece):
    def __init__(self,color):
        super().__init__(color)
        self.symbol = "R"
    def moves_from(self,pos,board):
        return sliding_moves(pos, board, self.color, [(1,0),(-1,0),(0,1),(0,-1)])

class Bishop(Piece):
    def __init__(self,color):
        super().__init__(color)
        self.symbol = "B"
    def moves_from(self,pos,board):
        return sliding_moves(pos, board, self.color, [(1,1),(1,-1),(-1,1),(-1,-1)])

class Knight(Piece):
    def __init__(self,color):
        super().__init__(color)
        self.symbol = "N"
    def moves_from(self,pos,board):
        r,c = pos
        deltas = [(2,1),(2,-1),(-2,1),(-2,-1),(1,2),(1,-2),(-1,2),(-1,-2)]
        moves = []
        for dr,dc in deltas:
            np = (r+dr,c+dc)
            if in_bounds(np):
                t = board.piece_at(np)
                if t is None or t.color!=self.color:
                    moves.append(np)
        return moves

class Pawn(Piece):
    def __init__(self,color):
        super().__init__(color)
        self.symbol = "P"
    def moves_from(self,pos,board):
        r,c = pos
        moves = []
        dir = -1 if self.color=='w' else 1
        # forward one
        one = (r+dir, c)
        if in_bounds(one) and board.piece_at(one) is None:
            moves.append(one)
            # forward two
            start_row = 6 if self.color=='w' else 1
            two = (r+2*dir, c)
            if r==start_row and board.piece_at(two) is None:
                moves.append(two)
        # captures
        for dc in (-1,1):
            cap = (r+dir, c+dc)
            if in_bounds(cap):
                t = board.piece_at(cap)
                if t is not None and t.color!=self.color:
                    moves.append(cap)
        # Note: en-passant and promotions omitted for brevity; can be added later
        return moves

# Sliding helper

def sliding_moves(pos, board, color, deltas):
    moves = []
    r,c = pos
    for dr,dc in deltas:
        nr, nc = r+dr, c+dc
        while in_bounds((nr,nc)):
            t = board.piece_at((nr,nc))
            if t is None:
                moves.append((nr,nc))
            else:
                if t.color!=color:
                    moves.append((nr,nc))
                break
            nr += dr; nc += dc
    return moves

# ----------------------------- Board & Rules -----------------------------

class Board:
    def __init__(self):
        self.grid: List[List[Optional[Piece]]] = [[None]*8 for _ in range(8)]
        self.to_move = 'w'  # 'w' or 'b'
        self._place_starting_position()

    def _place_starting_position(self):
        # place pawns
        for c in range(8):
            self.grid[6][c] = Pawn('w')
            self.grid[1][c] = Pawn('b')
        order = [Rook, Knight, Bishop, Queen, King, Bishop, Knight, Rook]
        for c,cls in enumerate(order):
            self.grid[7][c] = cls('w')
            self.grid[0][c] = cls('b')

    def piece_at(self, pos: Position) -> Optional[Piece]:
        r,c = pos
        return self.grid[r][c]

    def set_piece(self, pos: Position, piece: Optional[Piece]):
        r,c = pos
        self.grid[r][c] = piece

    def find_king(self, color: str) -> Optional[Position]:
        for r in range(8):
            for c in range(8):
                p = self.grid[r][c]
                if isinstance(p, King) and p.color==color:
                    return (r,c)
        return None

    def all_pieces_of(self, color: str) -> List[Tuple[Position, Piece]]:
        out = []
        for r in range(8):
            for c in range(8):
                p = self.grid[r][c]
                if p is not None and p.color==color:
                    out.append(((r,c), p))
        return out

    def clone(self) -> 'Board':
        return copy.deepcopy(self)

    # ------------------- Path control and move legality -------------------
    def path_clear(self, src: Position, dst: Position) -> bool:
        """pathControl: True if path between src->dst is clear for sliding pieces (excludes endpoints)."""
        sr,sc = src; dr,dc = dst
        dr_diff = dr - sr
        dc_diff = dc - sc
        step_r = 0 if dr_diff==0 else (1 if dr_diff>0 else -1)
        step_c = 0 if dc_diff==0 else (1 if dc_diff>0 else -1)
        # ensure direction
        if step_r!=0 and step_c!=0 and abs(dr_diff)!=abs(dc_diff):
            return False
        if step_r==0 and step_c==0:
            return True
        cur_r, cur_c = sr+step_r, sc+step_c
        while (cur_r,cur_c) != (dr,dc):
            if not in_bounds((cur_r,cur_c)):
                return False
            if self.piece_at((cur_r,cur_c)) is not None:
                return False
            cur_r += step_r; cur_c += step_c
        return True

    def is_square_attacked_by(self, sq: Position, attacker_color: str) -> bool:
        """Return True if any piece of attacker_color can move to sq (pseudo-legal)."""
        for (pos,piece) in self.all_pieces_of(attacker_color):
            # For pawns, attack squares differ from move squares
            if isinstance(piece, Pawn):
                r,c = pos
                dir = -1 if piece.color=='w' else 1
                for dc in (-1,1):
                    cap = (r+dir, c+dc)
                    if cap==sq:
                        return True
                continue
            moves = piece.moves_from(pos, self)
            if sq in moves:
                # If sliding piece, ensure path clear
                if isinstance(piece, (Bishop, Rook, Queen)):
                    if self.path_clear(pos, sq):
                        return True
                else:
                    return True
        return False

    def in_check(self, color: str) -> bool:
        king_pos = self.find_king(color)
        if king_pos is None:
            return True
        return self.is_square_attacked_by(king_pos, 'b' if color=='w' else 'w')

    def legal_moves(self, color: str) -> List[Tuple[Position, Position]]:
        moves = []
        for (pos,piece) in self.all_pieces_of(color):
            for dst in piece.moves_from(pos, self):
                # sliding path check
                if isinstance(piece, (Bishop, Rook, Queen)) and not self.path_clear(pos,dst):
                    continue
                # Destination friendly piece?
                target = self.piece_at(dst)
                if target is not None and target.color==color:
                    continue
                # make move on clone and check for self-check
                b2 = self.clone()
                b2.set_piece(dst, copy.deepcopy(piece))
                b2.set_piece(pos, None)
                if not b2.in_check(color):
                    moves.append((pos,dst))
        return moves

    def is_checkmate(self, color: str) -> bool:
        if not self.in_check(color):
            return False
        lm = self.legal_moves(color)
        return len(lm)==0

    def make_move(self, src: Position, dst: Position) -> bool:
        """Attempt to make move; returns True if made, False if illegal."""
        piece = self.piece_at(src)
        if piece is None or piece.color!=self.to_move:
            return False
        # Check pseudo-legal
        possible = piece.moves_from(src, self)
        if dst not in possible:
            return False
        if isinstance(piece, (Bishop,Rook,Queen)) and not self.path_clear(src,dst):
            return False
        target = self.piece_at(dst)
        if target is not None and target.color==piece.color:
            return False
        # simulate and check for leaving king in check
        b2 = self.clone()
        b2.set_piece(dst, copy.deepcopy(piece))
        b2.set_piece(src, None)
        if b2.in_check(piece.color):
            return False
        # commit
        self.set_piece(dst, piece)
        self.set_piece(src, None)
        self.to_move = 'b' if self.to_move=='w' else 'w'
        return True

    # textual board for quick display
    def ascii(self) -> str:
        rows = []
        for r in range(8):
            row = []
            for c in range(8):
                p = self.grid[r][c]
                row.append(str(p) if p else '.')
            rows.append(str(8-r) + ' ' + ' '.join(row))
        rows.append('  a b c d e f g h')
        return '\n'.join(rows)

# ----------------------------- Minimal CLI Demo -----------------------------

def parse_alg(s: str) -> Position:
    s = s.strip()
    if len(s)!=2:
        raise ValueError('invalid')
    file = ord(s[0].lower()) - ord('a')
    rank = 8 - int(s[1])
    return (rank,file)

# ----------------------------- Simple UIs -----------------------------

# Streamlit UI (very small): displays board and accepts algebraic coordinates to move

def run_streamlit_ui(board: Board):
    import streamlit as st
    st.title('Mini Chess — Engine + Streamlit UI')
    if 'board' not in st.session_state:
        st.session_state.board = board
    b: Board = st.session_state.board
    st.text(b.ascii())
    st.write(f"To move: {'White' if b.to_move=='w' else 'Black'}")
    col1, col2 = st.columns(2)
    with col1:
        src = st.text_input('From (e.g. e2)')
    with col2:
        dst = st.text_input('To (e.g. e4)')
    if st.button('Make Move'):
        try:
            s = parse_alg(src)
            d = parse_alg(dst)
            ok = b.make_move(s,d)
            if not ok:
                st.error('Illegal move or not your piece.')
            else:
                st.success('Move made')
        except Exception as e:
            st.error(f'Error: {e}')
    st.write('In check (white):', b.in_check('w'))
    st.write('In check (black):', b.in_check('b'))
    st.write('Checkmate (white):', b.is_checkmate('w'))
    st.write('Checkmate (black):', b.is_checkmate('b'))

# Tkinter UI: small board using labels and simple text entry for moves

def run_tk_ui(board: Board):
    import tkinter as tk
    from tkinter import messagebox

    root = tk.Tk()
    root.title('Mini Chess — Tkinter')
    b = board

    display = tk.Text(root, width=32, height=17, font=('Consolas',12))
    display.grid(row=0, column=0, columnspan=4)
    src_var = tk.StringVar()
    dst_var = tk.StringVar()
    tk.Entry(root, textvariable=src_var).grid(row=1,column=0)
    tk.Entry(root, textvariable=dst_var).grid(row=1,column=1)
    def refresh():
        display.delete('1.0', tk.END)
        display.insert(tk.END, b.ascii())
    def do_move():
        try:
            s = parse_alg(src_var.get())
            d = parse_alg(dst_var.get())
        except Exception:
            messagebox.showerror('Error','Invalid coords')
            return
        ok = b.make_move(s,d)
        if not ok:
            messagebox.showwarning('Illegal','Illegal move or not your piece')
        refresh()
    tk.Button(root, text='Move', command=do_move).grid(row=1,column=2)
    tk.Button(root, text='Quit', command=root.destroy).grid(row=1,column=3)
    refresh()
    root.mainloop()

# ----------------------------- Entrypoint -----------------------------

def main(args):
    board = Board()
    ui = args.ui if args.ui else 'cli'
    if ui=='streamlit':
        run_streamlit_ui(board)
    elif ui=='tk':
        run_tk_ui(board)
    else:
        print(board.ascii())
        print('To move:', board.to_move)
        print('Example move: e2 e4')
        while True:
            try:
                raw = input('move> ')
            except EOFError:
                break
            raw = raw.strip()
            if raw in ('quit','exit'):
                break
            if not raw:
                continue
            parts = raw.split()
            if len(parts)!=2:
                print('type: e2 e4')
                continue
            try:
                s = parse_alg(parts[0]); d = parse_alg(parts[1])
                ok = board.make_move(s,d)
                if not ok:
                    print('Illegal move')
                print(board.ascii())
                print('In check (w):', board.in_check('w'))
                print('In check (b):', board.in_check('b'))
                if board.is_checkmate('w'):
                    print('White is checkmated')
                    break
                if board.is_checkmate('b'):
                    print('Black is checkmated')
                    break
            except Exception as e:
                print('Error:', e)

if __name__=='__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--ui', choices=['cli','streamlit','tk'], default='cli')
    args = parser.parse_args()
    main(args)
