import streamlit as st
import numpy as np
import math

st.title("Tic Tac Toe Game")
st.subheader("Made by Rishiraj")

# Initialize board
if 'board' not in st.session_state:
    st.session_state.board = np.array([[' ']*3]*3)

if 'current_player' not in st.session_state:
    st.session_state.current_player = 'X'

def check_winner(board):
    for row in board:
        if row[0] == row[1] == row[2] and row[0] != ' ':
            return row[0]
    
    for col in range(3):
        if board[0][col] == board[1][col] == board[2][col] and board[0][col] != ' ':
            return board[0][col]

    if board[0][0] == board[1][1] == board[2][2] and board[0][0] != ' ':
        return board[0][0]

    if board[0][2] == board[1][1] == board[2][0] and board[0][2] != ' ':
        return board[0][2]

    return None

def is_tie(board):
    for row in board:
        if ' ' in row:
            return False
    return True

def get_available_moves(board):
    moves = []
    for i in range(3):
        for j in range(3):
            if board[i][j] == ' ':
                moves.append((i, j))
    return moves

def minimax(board, depth, is_maximizing):
    winner = check_winner(board)
    if winner == 'O':
        return 1
    elif winner == 'X':
        return -1
    elif is_tie(board):
        return 0

    if is_maximizing:
        best_score = -math.inf
        for move in get_available_moves(board):
            board[move[0]][move[1]] = 'O'
            score = minimax(board, depth + 1, False)
            board[move[0]][move[1]] = ' '
            best_score = max(score, best_score)
        return best_score
    else:
        best_score = math.inf
        for move in get_available_moves(board):
            board[move[0]][move[1]] = 'X'
            score = minimax(board, depth + 1, True)
            board[move[0]][move[1]] = ' '
            best_score = min(score, best_score)
        return best_score

def computer_move(board):
    best_score = -math.inf
    best_move = None
    for move in get_available_moves(board):
        board[move[0]][move[1]] = 'O'
        score = minimax(board, 0, False)
        board[move[0]][move[1]] = ' '
        if score > best_score:
            best_score = score
            best_move = move
    board[best_move[0]][best_move[1]] = 'O'

def player_move(board, row, col):
    if board[row][col] == ' ':
        board[row][col] = 'X'
        return True
    return False

# Game logic
winner = check_winner(st.session_state.board)
if winner or is_tie(st.session_state.board):
    if winner:
        st.markdown(f"<h1 style='text-align: center; font-size: 50px;'>Game Over! Computer wins!</h1>", unsafe_allow_html=True)
    else:
        st.markdown("<h1 style='text-align: center; font-size: 50px;'>Game Over! It's a tie!</h1>", unsafe_allow_html=True)
else:
    st.write("Current Player: ", st.session_state.current_player)
    st.write(st.session_state.board)
    if st.session_state.current_player == 'X':
        st.write("Your move!")
    else:
        st.write("Computer is making a move...")
        computer_move(st.session_state.board)
        st.session_state.current_player = 'X'
        st.experimental_rerun()

# Create buttons for player move
for i in range(3):
    cols = st.columns(3)
    for j in range(3):
        if st.session_state.board[i][j] == ' ':
            if cols[j].button(" ", key=f"move_{i}_{j}"):
                if player_move(st.session_state.board, i, j):
                    st.session_state.current_player = 'O'
                    st.experimental_rerun()
        else:
            cols[j].button(st.session_state.board[i][j], disabled=True, key=f"move_{i}_{j}")
