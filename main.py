import numpy as np
import pygame


def did_win(value, size, board):  # 승리 판정

    for y_idx in range(size):  # 가로 5줄
        for x_idx in range(size - 4):
            line = board[y_idx, x_idx : x_idx + 5]
            if line.sum() == value * 5:
                return value

    for y_idx in range(size - 4):  # 세로 5줄
        for x_idx in range(size):
            line = board[y_idx : y_idx + 5, x_idx]
            if line.sum() == value * 5:
                return value

    for y_idx in range(size - 4):  # 대각선 \, / 5줄
        for x_idx in range(size - 4):
            line[0] = board[y_idx, x_idx]
            line[1] = board[y_idx + 1, x_idx + 1]
            line[2] = board[y_idx + 2, x_idx + 2]
            line[3] = board[y_idx + 3, x_idx + 3]
            line[4] = board[y_idx + 4, x_idx + 4]
            if line.sum() == value * 5:
                return value

            line[0] = board[y_idx, x_idx + 4]
            line[1] = board[y_idx + 1, x_idx + 3]
            line[2] = board[y_idx + 2, x_idx + 2]
            line[3] = board[y_idx + 3, x_idx + 1]
            line[4] = board[y_idx + 4, x_idx]
            if line.sum() == value * 5:
                return value


def omok(size):  # play

    board = np.zeros([size, size])
    turn = 1
    max_turn = size ** 2
    print("\n", board, "\n")

    while True:
        try:
            if turn % 2 == 1:
                index = list(map(int, input("흑돌 차례 : ").split())) # 흑돌 두기
                if board[index[0], index[1]] == 1 or board[index[0], index[1]] == 6:
                    print("돌이 그 자리에 이미 놓임\n")
                    continue
                board[index[0], index[1]] = 1

                if did_win(1, size, board) == 1: # 흑 승리 판정
                    print(board, "\n\n💥 흑 승리!! 💥\n")
                    break

            else:
                index = list(map(int, input("백돌 차례 : ").split())) # 백돌 두기
                if board[index[0], index[1]] == 1 or board[index[0], index[1]] == 6:
                    print("돌이 그 자리에 이미 놓임\n")
                    continue
                board[index[0], index[1]] = 6

                if did_win(6, size, board) == 6: # 백 승리 판정
                    print(board, "\n\n💥 백 승리!! 💥\n")
                    break

            print(board, "\n")
            turn += 1
            if turn > max_turn:
                print("둘 수 있는 곳이 없음, 무승부!")
                break

        except:
            print("잘못된 좌표\n")
            continue


print("\n나랑 같이...오목 할래?")
while True:
    omok(9)
    if input("한판 더(1)/그만(other): ") != "1":
        break
