# Chess Streamlit App

This project is a chess game built from scratch using Streamlit. It provides an interactive interface for playing chess online.

## Project Structure


> -chess-streamlit-app
>  -src
>    ─app.py                
>    ─ chess
>     ─ __init__.py       
>     ─ board.py          
>     ─ pieces.py
>     ─ game.py           
>     ─ utils.py          
>    ─ ui
>     ─ __init__.py       
>     ─ streamlit_ui.py   
>  ─ requirements.txt           
>  ─ README.md


## Setup Instructions

1. Clone the repository:
   ```
   git clone <repository-url>
   cd chess-streamlit-app
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Run the Streamlit application:
   ```
   streamlit run src/app.py
   ```
   or
   ```
   python -m streamlit run src/app.py
   ```

## Usage

Once the application is running, you can interact with the chessboard, make moves, and play against an opponent. The UI will display the current game status and allow you to reset the game as needed.

## Contributing

Contributions are welcome! Please feel free to submit a pull request or open an issue for any suggestions or improvements.
