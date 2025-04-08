import streamlit as st
import numpy as np

# Set page layout
st.set_page_config(layout="centered")

# Custom CSS
st.markdown("""
    <style>
        .stButton>button {
            font-size: 32px !important;
            height: 80px;
            width: 100%;
            border-radius: 10px;
        }
        .winner-box {
            font-size: 24px;
            font-weight: bold;
            padding: 12px;
            border-radius: 10px;
            background-color: #e6ffe6;
            text-align: center;
            margin-top: 20px;
        }
        .tie-box {
            font-size: 24px;
            font-weight: bold;
            padding: 12px;
            border-radius: 10px;
            background-color: #f0f0f0;
            text-align: center;
            margin-top: 20px;
        }
    </style>
""", unsafe_allow_html=True)

# Game state
if 'board' not in st.session_state:
    st.session_state.board = [[" " for _ in range(3)] for _ in range(3)]
if 'turn' not in st.session_state:
    st.session_state.turn = 0
if 'winner' not in st.session_state:
    st.session_state.winner = None
if 'mode' not in st.session_state:
    st.session_state.mode = "Player vs AI"

# Title & Mode
st.title("🎮 Tic-Tac-Toe")
mode = st.radio("Select Game Mode:", ("Player vs AI", "Multiplayer (P1 vs P2)"), horizontal=True)

if st.session_state.mode != mode:
    st.session_state.board = [[" " for _ in range(3)] for _ in range(3)]
    st.session_state.turn = 0
    st.session_state.winner = None
    st.session_state.mode = mode

# Game logic
def check_win(board, player):
    for row in board:
        if all(cell == player for cell in row):
            return True
    for col in range(3):
        if all(board[row][col] == player for row in range(3)):
            return True
    if all(board[i][i] == player for i in range(3)) or all(board[i][2 - i] == player for i in range(3)):
        return True
    return False

def check_tie(board):
    return all(cell != " " for row in board for cell in row)

def minimax(board, depth, is_max):
    if check_win(board, "O"): return 1
    if check_win(board, "X"): return -1
    if check_tie(board): return 0

    if is_max:
        best = -np.inf
        for i in range(3):
            for j in range(3):
                if board[i][j] == " ":
                    board[i][j] = "O"
                    score = minimax(board, depth + 1, False)
                    board[i][j] = " "
                    best = max(score, best)
        return best
    else:
        best = np.inf
        for i in range(3):
            for j in range(3):
                if board[i][j] == " ":
                    board[i][j] = "X"
                    score = minimax(board, depth + 1, True)
                    board[i][j] = " "
                    best = min(score, best)
        return best

def ai_move(board):
    best_score = -np.inf
    move = None
    for i in range(3):
        for j in range(3):
            if board[i][j] == " ":
                board[i][j] = "O"
                score = minimax(board, 0, False)
                board[i][j] = " "
                if score > best_score:
                    best_score = score
                    move = (i, j)
    return move

def make_move(i, j):
    if st.session_state.board[i][j] == " " and not st.session_state.winner:
        player = "X" if st.session_state.turn % 2 == 0 else "O"
        st.session_state.board[i][j] = player
        if check_win(st.session_state.board, player):
            st.session_state.winner = player
        elif check_tie(st.session_state.board):
            st.session_state.winner = "Tie"
        else:
            st.session_state.turn += 1

        # AI move
        if st.session_state.mode == "Player vs AI" and st.session_state.turn % 2 != 0 and not st.session_state.winner:
            move = ai_move(st.session_state.board)
            if move:
                st.session_state.board[move[0]][move[1]] = "O"
                if check_win(st.session_state.board, "O"):
                    st.session_state.winner = "O"
                elif check_tie(st.session_state.board):
                    st.session_state.winner = "Tie"
                else:
                    st.session_state.turn += 1

# Display board with 3 boxes per row
for i in range(3):
    cols = st.columns(3)
    for j in range(3):
        symbol = st.session_state.board[i][j]
        display = "❌" if symbol == "X" else "⭕" if symbol == "O" else " "
        if symbol == " " and not st.session_state.winner:
            if cols[j].button(display, key=f"{i}_{j}"):
                make_move(i, j)
        else:
            cols[j].button(display, key=f"{i}_{j}", disabled=True)

# Winner or tie message
if st.session_state.winner:
    if st.session_state.winner == "Tie":
        st.markdown('<div class="tie-box">🤝 It\'s a tie!</div>', unsafe_allow_html=True)
    else:
        name = "AI" if st.session_state.mode == "Player vs AI" and st.session_state.winner == "O" else f"Player {st.session_state.winner}"
        st.markdown(f'<div class="winner-box">🎉 {name} wins!</div>', unsafe_allow_html=True)

# Reset button
if st.button("🔄 Reset Game"):
    st.session_state.board = [[" " for _ in range(3)] for _ in range(3)]
    st.session_state.turn = 0
    st.session_state.winner = None
