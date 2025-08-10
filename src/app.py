import streamlit as st
from chess.board import Board
from chess.game import Game

def main():
    st.title("Chess Game")
    
    game = Game()
    board = Board()

    if st.button("Start New Game"):
        game.start_new_game()
        board.setup_board()

    st.write("Current Board:")
    st.write(board.display())

    move = st.text_input("Enter your move (e.g., e2 to e4):")
    
    if st.button("Make Move"):
        if game.make_move(move):
            st.success("Move made successfully!")
        else:
            st.error("Invalid move. Please try again.")

    st.write("Game Status:")
    st.write(game.get_status())

if __name__ == "__main__":
    main()