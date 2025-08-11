# Chess Streamlit App

This project is a chess game built from scratch using Streamlit. It provides an interactive interface for playing chess online.

## Project Structure


```
chess-streamlit-app
├── src
│   ├── app.py                # Entry point of the Streamlit application
│   ├── chess
│   │   ├── __init__.py       # Initializes the chess package
│   │   ├── board.py          # Contains the Board class for managing the chessboard
│   │   ├── pieces.py         # Defines classes for different chess pieces
│   │   ├── game.py           # Manages game logic and rules
│   │   └── utils.py          # Utility functions for the chess game
│   └── ui
│       ├── __init__.py       # Initializes the UI package
│       └── streamlit_ui.py   # Streamlit UI components for the chess game
├── requirements.txt           # Lists project dependencies
└── README.md                  # Documentation for the project
```

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

## Contributors

Mustapha Muhammad - [mustyog669@gmail.com](mailto:mustyog669@gmail.com)
