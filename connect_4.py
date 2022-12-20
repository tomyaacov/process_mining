import random

import numpy as np

import sys
import math

ROW_COUNT = 6
COLUMN_COUNT = 7


def create_board():
    board = np.zeros((ROW_COUNT, COLUMN_COUNT))
    return board


def drop_piece(board, row, col, piece):
    board[row][col] = piece


def is_valid_location(board, col):
    return board[ROW_COUNT - 1][col] == 0


def get_next_open_row(board, col):
    for r in range(ROW_COUNT):
        if board[r][col] == 0:
            return r


def print_board(board):
    print(np.flip(board, 0))


def is_game_over(board):
    for c in range(COLUMN_COUNT):
        if is_valid_location(board, c):
            return False
    return True



def winning_move(board, piece):
    # Check horizontal locations for win
    for c in range(COLUMN_COUNT - 3):
        for r in range(ROW_COUNT):
            if board[r][c] == piece and board[r][c + 1] == piece and board[r][c + 2] == piece and board[r][c + 3] == piece:
                return True

    # Check vertical locations for win
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT - 3):
            if board[r][c] == piece and board[r + 1][c] == piece and board[r + 2][c] == piece and board[r + 3][c] == piece:
                return True

    # Check positively sloped diaganols
    for c in range(COLUMN_COUNT - 3):
        for r in range(ROW_COUNT - 3):
            if board[r][c] == piece and board[r + 1][c + 1] == piece and board[r + 2][c + 2] == piece and board[r + 3][c + 3] == piece:
                return True

    # Check negatively sloped diaganols
    for c in range(COLUMN_COUNT - 3):
        for r in range(3, ROW_COUNT):
            if board[r][c] == piece and board[r - 1][c + 1] == piece and board[r - 2][c + 2] == piece and board[r - 3][c + 3] == piece:
                return True

TRACES = set()

while len(TRACES) < 300000:
    t = []
    board = create_board()
    #print_board(board)
    game_over = False
    turn = 1

    player_map = {1: "A", 2: "B"}
    column_options = list(range(COLUMN_COUNT))

    while not game_over:
        while True:
            col = random.choice(column_options)
            if is_valid_location(board, col):
                row = get_next_open_row(board, col)
                drop_piece(board, row, col, turn)
                t.append(player_map[turn] + str(row) + str(col))
                if not is_valid_location(board, col):
                    column_options.remove(col)
                if winning_move(board, turn):
                    game_over = True
                if is_game_over(board):
                    game_over = True
                break
        #print_board(board)
        turn = 1 + (turn % 2)

    TRACES.add(tuple(t))
    if len(TRACES) % 10000 == 0:
        print(len(TRACES))

import csv
with open("data/connect4/connect4_traces.csv", "w") as file:
    writer = csv.writer(file)
    writer.writerows(TRACES)


