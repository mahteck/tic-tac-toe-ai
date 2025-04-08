import streamlit as st
import numpy as np

# Set wide layout
st.set_page_config(layout="centered")

# Custom CSS for styling
st.markdown("""
    <style>
        .stButton>button {
            font-size: 40px !important;
            height: 80px;
            width: 80px;
            border-radius: 10px;
        }
        .winner-box {
            font-size: 28px;
            font-weight: bold;
            padding: 10px;
            border: 2px solid #4CAF50;
            border-radius: 10px;
            background-color: #eaffea;
            text-align: center;
        }
        .tie-box {
            font-size: 28px;
            font-weight: bold;
            padding: 10px;
            border: 2px solid #999;
            border-radius: 10px;
            background-color: #f0f0f0;
            text-align: center;
        }
    </style>
""", unsafe_allow_html=True)

# Title and Mode
st.title("🎮 Tic-Tac-Toe")
mode = st.radio("Select Game Mode:", ("Player vs AI", "Multiplayer (P1 vs P2)"), horizontal=True)

# Initialize game state
if 'board' not in st.session_state:
    st.session_state.board = [[" " for _ in range(3)] for _ in range(3)]
if 'turn' not in st.session_state:
    st.session_state.turn = 0
if 'winner' not in st.session_state:
    st.session_state.winner = None
if 'mode' not in st.session_state:
    st.session_state.mode = mode

# Reset if mode changes
if st.session_state.mode != mode:
    st.session_state.board = [[" " for _ in range(3)] for _ in range(3)]
    st.session_state.turn = 0
    st.session_state.winner = None
    st.session_state.mode = mode

# --- Game logic functions ---
def check_win(board, player):
    for row in board:
        if all([cell == player for cell in row]):
            return True
    for col in range(3):
        if all([board[row][col] == player for row in range(3)]):
            return True
    if all([board[i][i] == player for i in range(3)]) or all([board[i][2 - i] == player for i in range(3)]):
        return True
    return False

def check_tie(board):
    return all(cell != " " for row in board for cell in row)

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

def make_move(row, col):
    if st.session_state.board[row][col] == " " and not st.session_state.winner:
        player = "X" if st.session_state.turn % 2 == 0 else "O"
        st.session_state.board[row][col] = player

        if check_win(st.session_state.board, player):
            st.session_state.winner = player
        elif check_tie(st.session_state.board):
            st.session_state.winner = "Tie"
        else:
            st.session_state.turn += 1

        # AI move if needed
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

# Display the board
for r in range(3):
    cols = st.columns(3)
    for c in range(3):
        symbol = st.session_state.board[r][c]
        display = "❌" if symbol == "X" else "⭕" if symbol == "O" else "⬜"
        if symbol == " " and not st.session_state.winner:
            if cols[c].button(display, key=f"{r}_{c}"):
                make_move(r, c)
        else:
            cols[c].button(display, key=f"{r}_{c}", disabled=True)

# Show winner or tie
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
