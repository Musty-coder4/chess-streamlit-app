import streamlit as st
from chess.game import Game
from chess.utils import parse_position

def main():
    st.title("Chess Game (Streamlit)")
    if "game" not in st.session_state:
        st.session_state.game = Game()

    game = st.session_state.game

    st.write(f"Turn: {game.current_turn.capitalize()}")
    board = game.get_board_symbols()
    for i, row in enumerate(board):
        st.write(" ".join(row) + f"  {8-i}")
    st.write("a b c d e f g h")

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