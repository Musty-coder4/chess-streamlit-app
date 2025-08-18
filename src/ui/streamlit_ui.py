import streamlit as st
from typing import List, Dict, Any, Optional, Tuple
from chess.game import Game
from chess.utils import parse_position
from PIL import Image, ImageDraw, ImageFont
import io
import os

# Unicode symbols for pieces
PIECE_SYMBOLS = {
    "♔": "♔", "♕": "♕", "♖": "♖", "♗": "♗", "♘": "♘", "♙": "♙",
    "♚": "♚", "♛": "♛", "♜": "♜", "♝": "♝", "♞": "♞", "♟": "♟",
    ".": ""
}


def draw_chessboard(board: List[List[str]]) -> Image.Image:
    square_size = 50  # Reduced size to fit better
    board_size = 8 * square_size
    colors = [(240, 217, 181), (181, 136, 99)]  # light, dark
    img = Image.new("RGB", (board_size, board_size), colors[0])
    draw = ImageDraw.Draw(img)

    # Try to use a system font that supports chess symbols
    font = None
    font_paths = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "C:/Windows/Fonts/DejaVuSans.ttf",
        "C:/Windows/Fonts/Arial Unicode MS.ttf",
        "C:/Windows/Fonts/seguisym.ttf",
        "DejaVuSans.ttf",
        "Arial Unicode MS.ttf",
        "Segoe UI Symbol.ttf"
    ]
    for font_path in font_paths:
        try:
            font = ImageFont.truetype(font_path, 36)
            if not font.getmask("♔").getbbox():
                font = None
                continue
            break
        except:
            font = None
            continue
    if font is None:
        font = ImageFont.load_default()

    for i in range(8):
        for j in range(8):
            x0 = j * square_size
            y0 = i * square_size
            color = colors[(i + j) % 2]
            draw.rectangle([x0, y0, x0 + square_size,
                           y0 + square_size], fill=color)
            symbol = board[i][j]
            if symbol in PIECE_SYMBOLS and PIECE_SYMBOLS[symbol]:
                bbox = draw.textbbox((0, 0), PIECE_SYMBOLS[symbol], font=font)
                w, h = bbox[2] - bbox[0], bbox[3] - bbox[1]
                draw.text(
                    (x0 + (square_size - w) / 2, y0 + (square_size - h) / 2 - 2),
                    PIECE_SYMBOLS[symbol],
                    fill=(0, 0, 0),
                    font=font
                )

    # Draw coordinates
    coord_font = None
    for font_path in font_paths:
        try:
            coord_font = ImageFont.truetype(font_path, 12)
            if not coord_font.getmask("8").getbbox():
                coord_font = None
                continue
            break
        except:
            coord_font = None
            continue
    if coord_font is None:
        coord_font = ImageFont.load_default()

    for i in range(8):
        draw.text((1, i * square_size + 1), str(8 - i),
                  fill=(0, 0, 0), font=coord_font)
        draw.text((i * square_size + square_size - 10, board_size - 15),
                  "abcdefgh"[i], fill=(0, 0, 0), font=coord_font)

    return img


def main():
    st.set_page_config(layout="wide", page_title="Chess Game")

    if "game" not in st.session_state:
        st.session_state.game = Game()
        st.session_state.move_history = []

    game = st.session_state.game

    # Main layout in two columns with centering
    col_left, col1, col2, col_right1, col_right2 = st.columns([1, 3, 2, 1, 1])

    with col1:
        st.title("♟️ Chess Game")
        st.write(f"**Turn: {game.current_turn.capitalize()}**")

        # Draw the chessboard
        board = game.get_board_symbols()
        img = draw_chessboard(board)
        buf = io.BytesIO()
        img.save(buf, format="PNG")
        st.image(buf.getvalue(), use_container_width=False)

    with col2:
        st.subheader("Game Info")

        # Status and controls in a compact format
        st.write("**Status:**", game.status)

        # Move input section
        st.subheader("Make Move")

        if game.promoting:
            piece_type = st.selectbox("Promote pawn to:", ["Q", "R", "B", "N"])
            if st.button("Promote"):
                game.promote(piece_type)
        else:
            with st.form("move_form", clear_on_submit=True):
                from_square = st.text_input("From (e.g. e2):", max_chars=2)
                to_square = st.text_input("To (e.g. e4):", max_chars=2)
                submitted = st.form_submit_button(
                    "Move", use_container_width=True)
                if submitted:
                    from_pos = parse_position(from_square.strip())
                    to_pos = parse_position(to_square.strip())
                    if from_pos and to_pos:
                        success = game.move(from_pos, to_pos)
                        if success:
                            # Store move in history
                            st.session_state.move_history.append({
                                'from': from_pos,
                                'to': to_pos,
                                'piece': game.board.grid[to_pos[0]][to_pos[1]],
                                'captured': None,  # Simplified - would need to track captured pieces
                                'turn': game.current_turn
                            })
                            st.rerun()
                    else:
                        game.status = "Invalid input. Use format like e2, e4."

        # Reverse move button
        if st.button("↩️ Reverse Last Move", use_container_width=True, disabled=len(st.session_state.move_history) == 0):
            if st.session_state.move_history:
                # Remove last move from history
                last_move = st.session_state.move_history.pop()

                # Reset the game state
                st.session_state.game = Game()

                # Replay all moves except the last one
                for move in st.session_state.move_history:
                    st.session_state.game.move(move['from'], move['to'])

                st.rerun()

        # Restart button
        if st.button("Restart Game", use_container_width=True):
            st.session_state.game = Game()
            st.session_state.move_history = []
            st.rerun()


if __name__ == "__main__":
    main()
