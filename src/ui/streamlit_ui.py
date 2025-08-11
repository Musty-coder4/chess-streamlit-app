import streamlit as st
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

def draw_chessboard(board):
    square_size = 60
    board_size = 8 * square_size
    colors = [(240, 217, 181), (181, 136, 99)]  # light, dark
    img = Image.new("RGB", (board_size, board_size), colors[0])
    draw = ImageDraw.Draw(img)

    # Try to use a system font that supports chess symbols
    font = None
    for font_name in ["DejaVuSans.ttf", "Arial Unicode MS.ttf", "Segoe UI Symbol.ttf"]:
        try:
            font = ImageFont.truetype(font_name, 44)
            # Test if font supports chess symbols by checking a sample character
            if not font.getmask("♔").getbbox():
                # If no bounding box, font does not support chess symbols, continue to next font
                font = None
                continue
            break
        except:
            continue
    if font is None:
        font = ImageFont.load_default()

    for i in range(8):
        for j in range(8):
            x0 = j * square_size
            y0 = i * square_size
            color = colors[(i + j) % 2]
            draw.rectangle([x0, y0, x0 + square_size, y0 + square_size], fill=color)
            symbol = board[i][j]
            if symbol in PIECE_SYMBOLS and PIECE_SYMBOLS[symbol]:
                bbox = draw.textbbox((0, 0), PIECE_SYMBOLS[symbol], font=font)
                w, h = bbox[2] - bbox[0], bbox[3] - bbox[1]
                draw.text(
                    (x0 + (square_size - w) / 2, y0 + (square_size - h) / 2 - 4),
                    PIECE_SYMBOLS[symbol],
                    fill=(0, 0, 0),
                    font=font
                )
    # Draw coordinates
    for i in range(8):
        # Ranks
        draw.text((2, i * square_size + 2), str(8 - i), fill=(0, 0, 0), font=font)
        # Files
        draw.text((i * square_size + square_size - 18, board_size - 22), "abcdefgh"[i], fill=(0, 0, 0), font=font)

    return img

def main():
    st.title("Chess Game (Streamlit)")
    if "game" not in st.session_state:
        st.session_state.game = Game()

    game = st.session_state.game

    st.write(f"Turn: {game.current_turn.capitalize()}")

    # Draw the chessboard as an image
    board = game.get_board_symbols()
    img = draw_chessboard(board)
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    st.image(buf.getvalue(), use_container_width=False)

    st.write(game.status)

    # Display castling rights
    cr = game.castling_rights
    st.info(
        f"Castling rights - White: "
        f"{'K' if cr['white']['kingside'] else ''}{'Q' if cr['white']['queenside'] else ''} | "
        f"Black: {'K' if cr['black']['kingside'] else ''}{'Q' if cr['black']['queenside'] else ''}"
    )

    # Display en passant target
    if game.en_passant_target:
        files = "abcdefgh"
        x, y = game.en_passant_target
        ep_square = f"{files[y]}{8-x}"
        st.info(f"En passant available at: {ep_square}")

    if game.promoting:
        piece_type = st.selectbox("Promote pawn to:", ["Q", "R", "B", "N"])
        if st.button("Promote"):
            game.promote(piece_type)
    else:
        with st.form("move_form"):
            from_square = st.text_input("From (e.g. e2):")
            to_square = st.text_input("To (e.g. e4):")
            submitted = st.form_submit_button("Move")
            if submitted:
                from_pos = parse_position(from_square.strip())
                to_pos = parse_position(to_square.strip())
                if from_pos and to_pos:
                    game.move(from_pos, to_pos)
                else:
                    game.status = "Invalid input. Use format like e2, e4."

    if st.button("Restart Game"):
        st.session_state.game = Game()

if __name__ == "__main__":
    main()
