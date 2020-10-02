import numpy as np
import pygame


def print_board(size, board):
    n = size
    for y in board:
        if n <= 9:
            print(" " + str(n), end="") ## 띄어쓰기를 먼저 해서 자릿수 위치 맞추기, 이전 코드: print(n, end=" ")
        else:
            print(n, end="")
        m = 1
        for x in y:
            if x == 1:
                print("⚫", end="")
            elif x == 6:
                print("⚪", end="")
            elif ((size>=13)&((m==4)|(m==10)|(m==16))&((n==4)|(n==10)|(n==16))) | ((size==9)&((((m==3)|(m==7))&((n==3)|(n==7)))|((m==5)&(n==5)))) | ((size==13)&(m==7)&(n==7)):
                print("🟡", end="")
            else:
                print("🟤", end="")
            m += 1
        n -= 1
        print()
    if size > 13:
        print("   1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9\n")
    elif size > 9:
        print("   1 2 3 4 5 6 7 8 9 0 1 2 3\n")
    else:
        print("   1 2 3 4 5 6 7 8 9\n")


def is_five(value, size, board):  # 승리 판정

    for y in range(size):  # 가로 5줄
        for x in range(size - 4):
            line = board[y, x:x+5]
            if line.sum() == value * 5:
                return value
        
    for y in range(size - 4):  # 세로 5줄
        for x in range(size):
            line = board[y:y+5, x]
            if line.sum() == value * 5:
                return value

    for y in range(size - 4):  # 대각선 \ or / 5줄
        for x in range(size - 4):
            line[0] = board[y, x]
            line[1] = board[y+1, x+1]
            line[2] = board[y+2, x+2]
            line[3] = board[y+3, x+3]
            line[4] = board[y+4, x+4]
            if line.sum() == value * 5:
                return value
            line[0], line[1], line[2], line[3], line[4] = 0,0,0,0,0 ### 실수 : 초기화 필요 ###

            line[0] = board[y, x+4]
            line[1] = board[y+1, x+3]
            line[2] = board[y+2, x+2]
            line[3] = board[y+3, x+1]
            line[4] = board[y+4, x]
            if line.sum() == value * 5:
                return value
            line[0], line[1], line[2], line[3], line[4] = 0,0,0,0,0 ###


def is_samsam(size, board):  # 삼삼 검사
    three = 0

    for y in range(size):  # 방해 없이 가로 3줄
        for x in range(size - 4):
            line = board[y, x:x+5]
            if line.sum() == 3:
                three += 1;
                break;

    for y in range(size - 4):  # 방해 없이 세로 3줄
        for x in range(size):
            line = board[y:y+5, x]
            if line.sum() == 3:
                three += 1;
                if three >= 2: return True
                break;

    for y in range(size - 4):  # 방해 없이 대각선 \ or / 3줄
        for x in range(size - 4):
            line[0] = board[y, x]
            line[1] = board[y+1, x+1]
            line[2] = board[y+2, x+2]
            line[3] = board[y+3, x+3]
            line[4] = board[y+4, x+4]
            if line.sum() == 3:
                three += 1
                if three >= 2: return True
            line[0], line[1], line[2], line[3], line[4] = 0,0,0,0,0 ###

            line[0] = board[y, x+4]
            line[1] = board[y+1, x+3]
            line[2] = board[y+2, x+2]
            line[3] = board[y+3, x+1]
            line[4] = board[y+4, x]
            if line.sum() == 3:
                three += 1
                if three >= 2: return True
            line[0], line[1], line[2], line[3], line[4] = 0,0,0,0,0 ###

    return False


def omok(size):  # play

    board = np.zeros([size, size])
    turn = 1
    max_turn = size ** 2
    print()
    print_board(size, board)

    print("게임 시작!")
    while True:
        try:
            if turn % 2 == 1:
                index = input("⚫ 흑돌 차례 : ")
            else:
                index = input("⚪ 백돌 차례 : ")

            index = list(map(int, (index.split())))
            index[0], index[1] = index[0]-1, size-index[1]
            if index[0] == -1 or index[1] == -1: raise
            index.reverse()
            if board[index[0], index[1]] == 1 or board[index[0], index[1]] == 6:
                print("돌이 그 자리에 이미 놓임\n")
                continue

            if turn % 2 == 1:
                board[index[0], index[1]] = 1  # 흑돌 두기

                if is_samsam(size, board):
                    print("흑은 삼삼에 둘 수 없음")
                    board[index[0], index[1]] = 0 ### 실수 : 돌을 두어보기도 전에 삼삼을 검사함 ###
                    continue

                if is_five(1, size, board) == 1:
                    print_board(size, board)
                    print("💥 흑 승리!! 💥\n")
                    break
            else:
                board[index[0], index[1]] = 6  # 백돌 두기

                if is_five(6, size, board) == 6:
                    print_board(size, board)
                    print("💥 백 승리!! 💥\n")
                    break

            print_board(size, board)
            # print(board)
            turn += 1
            if turn > max_turn:
                print("둘 수 있는 곳이 없음, 무승부!\n")
                break

        except:
            if index == "break": 
                print("게임 중단")
                break
            print("잘못된 좌표\n")
            continue


print("\n나랑 같이...오목 할래?")
print("\nbreak : 나가기")
while True:
    try:
        size = input("바둑판 크기 : ")
        size = int(size)
    except:
        try: size = int(list(size.split())[0])
        except: 
            if size == "break": break
            print("잘못된 값")
            continue
    omok(size)
    if input("한판 더(1)/그만(other): ") != "1":
        break

print("프로그램 종료")