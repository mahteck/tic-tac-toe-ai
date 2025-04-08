import streamlit as st
import random
import numpy as np

# Minimax AI Logic
def minimax(board, depth, is_maximizing):
    if check_win(board, "O"):
        return 1
    elif check_win(board, "X"):
        return -1
    elif check_tie(board):
        return 0

    if is_maximizing:
        best_score = -float('inf')
        for r in range(3):
            for c in range(3):
                if board[r][c] == " ":
                    board[r][c] = "O"
                    score = minimax(board, depth + 1, False)
                    board[r][c] = " "
                    best_score = max(score, best_score)
        return best_score
    else:
        best_score = float('inf')
        for r in range(3):
            for c in range(3):
                if board[r][c] == " ":
                    board[r][c] = "X"
                    score = minimax(board, depth + 1, True)
                    board[r][c] = " "
                    best_score = min(score, best_score)
        return best_score

# AI move based on Minimax
def ai_move(board):
    best_score = -float('inf')
    best_move = None
    for r in range(3):
        for c in range(3):
            if board[r][c] == " ":
                board[r][c] = "O"
                score = minimax(board, 0, False)
                board[r][c] = " "
                if score > best_score:
                    best_score = score
                    best_move = (r, c)
    return best_move

# Function to check win
def check_win(board, player):
    for row in board:
        if all([cell == player for cell in row]):
            return True
    for col in range(3):
        if all([board[row][col] == player for row in range(3)]):
            return True
    if board[0][0] == player and board[1][1] == player and board[2][2] == player:
        return True
    if board[0][2] == player and board[1][1] == player and board[2][0] == player:
        return True
    return False

# Function to check for a tie
def check_tie(board):
    return all(cell != " " for row in board for cell in row)

# Streamlit UI for Tic-Tac-Toe
st.title("Tic-Tac-Toe with AI")
st.write("### Play against AI (Minimax Algorithm)")

# Initialize game state
if 'board' not in st.session_state:
    st.session_state.board = [[" " for _ in range(3)] for _ in range(3)]
if 'turn' not in st.session_state:
    st.session_state.turn = 0
if 'winner' not in st.session_state:
    st.session_state.winner = None
if 'ai_playing' not in st.session_state:
    st.session_state.ai_playing = True  # Start with AI as opponent

# Display the board as a grid of buttons
def display_board():
    board_display = ""
    for row in st.session_state.board:
        board_display += f"| {' | '.join(row)} |\n"
        board_display += "-"*15 + "\n"
    return board_display

# Handle user move with clickable buttons
def make_move(row, col):
    if st.session_state.board[row][col] == " ":
        player = "X" if st.session_state.turn % 2 == 0 else "O"
        st.session_state.board[row][col] = player
        if check_win(st.session_state.board, player):
            st.session_state.winner = player
            st.write(f"Player {player} wins!")
        elif check_tie(st.session_state.board):
            st.write("It's a tie!")
        else:
            st.session_state.turn += 1
            if st.session_state.ai_playing and st.session_state.turn % 2 != 0:
                ai_move_position = ai_move(st.session_state.board)
                st.session_state.board[ai_move_position[0]][ai_move_position[1]] = "O"
                if check_win(st.session_state.board, "O"):
                    st.session_state.winner = "O"
                    st.write(f"AI wins!")
                elif check_tie(st.session_state.board):
                    st.write("It's a tie!")
                else:
                    st.session_state.turn += 1
    else:
        st.write("This position is already taken. Try again.")

# Create buttons for each cell in the board
for row in range(3):
    cols = st.columns(3)
    for col in range(3):
        if st.session_state.board[row][col] == " ":
            button = cols[col].button(f"{row},{col}", key=f"button_{row}_{col}")
            if button:
                make_move(row, col)
        else:
            cols[col].button(st.session_state.board[row][col], key=f"button_{row}_{col}", disabled=True)

# Reset the game
if st.button("Reset Game"):
    st.session_state.board = [[" " for _ in range(3)] for _ in range(3)]
    st.session_state.turn = 0
    st.session_state.winner = None
