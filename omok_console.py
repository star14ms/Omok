#: 설명, ##: 참고 코드 ###: 실수 체크

import numpy as np
import pygame


# 바둑판 콘솔창에 출력
def print_board(size, board):
    n = size
    for y in board:
        if n <= 9:
            print(" " + str(n), end="") ## print(n, end=" ") 띄어쓰기를 먼저 해서 자릿수 위치 맞추기 
        else:
            print(n, end="")
        m = 1
        for x in y:
            if x == -1:
                print("⚫", end="")
            elif x == 1:
                print("⚪", end="")
            elif ((size>=13)&((m==4)|(m==10)|(m==16))&((n==4)|(n==10)|(n==16))) | ((size==9)&((((m==3)|(m==7))&((n==3)|(n==7)))|((m==5)&(n==5)))) | ((size==13)&(m==7)&(n==7)):
                print("🔶", end="")
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


# 5줄 판정
def isFive(who_turn, size, board, x, y):
    
    # ㅡ 가로로 이어진 돌 수
    num1 = 1
    for x_l in range(x-1, x-6, -1): ### x -> x-1 ### 
        if (x_l == -1): break
        if board[y, x_l] == who_turn: ## print(x_l) ### 1 -> l ###
            num1 += 1
        else:
            break
    for x_r in range(x+1, x+6, +1): ### x -> x+1 ###
        if (x_r == size): break
        if board[y, x_r] == who_turn:
            num1 += 1
        else:
            break
    if num1 == 5:
        return True

    # ㅣ 세로로 이어진 돌 수
    num2 = 1
    for y_u in range(y-1, y-6, -1):  ### x-5 -> x-6(장목 검사) -> y-6 (복붙 주의)###
        if (y_u == -1): break
        if board[y_u, x] == who_turn:
            num2 += 1
        else:
            break
    for y_d in range(y+1, y+6, +1):
        if (y_d == size): break
        if board[y_d, x] == who_turn:
            num2 += 1
        else:
            break
    if num2 == 5:
        return True

    # \ 대각선으로 이어진 돌 수 
    num3 = 1
    x_l = x
    y_u = y ### y -> x ###
    for i in range(5):
        if (x_l-1 == -1) or (y_u-1 == -1): break ### or -> and ### while 안에 있었을 때 
        x_l -= 1
        y_u -= 1
        if board[y_u, x_l] == who_turn:
            num3 += 1
        else: 
            break
    x_r = x
    y_d = y
    for i in range(5):
        if (x_r+1 == size) or (y_d+1 == size): break ### != -> == ### while을 나오면서
        x_r += 1
        y_d += 1
        if board[y_d, x_r] == who_turn:
            num3 += 1
        else:
            break
    if num3 == 5:
        return True

    # / 대각선으로 이어진 돌 수
    num4 = 1
    x_l = x
    y_d = y
    for i in range(5):
        if (x_l-1 == -1) or (y_d+1 == size): break
        x_l -= 1
        y_d += 1
        if board[y_d, x_l] == who_turn:
            num4 += 1
        else:
            break
    x_r = x
    y_u = y
    for i in range(5):
        if (x_r+1 == size) or (y_u-1 == -1): break
        x_r += 1
        y_u -= 1
        if board[y_u, x_r] == who_turn:
            num4 += 1
        else:
            break
    if num4 == 5:
        return True
    
    if num1 > 5 or num2 > 5 or num3 > 5 or num4 > 5:
        if who_turn == 1:
            return True
        else:
            return None
    else:
        return False


def paly_omok(size):

    board = np.zeros([size, size])
    who_turn = -1
    turn = 1
    max_turn = size ** 2
    print()
    print_board(size, board)

    print("게임 시작!")
    while True:
        try:
            if who_turn == -1:
                index = input("⚫ 흑돌 차례 : ")
            else:
                index = input("⚪ 백돌 차례 : ")

            index = list(map(int, (index.split())))
            index[0], index[1] = index[0]-1, size-index[1]
            if index[0] == -1 or index[1] == -1: raise
            index.reverse()
            if board[index[0], index[1]] == -1 or board[index[0], index[1]] == 1:
                print("돌이 그 자리에 이미 놓임\n")
                continue

            if who_turn == -1:
                board[index[0], index[1]] = -1  # 흑돌 두기


                five = isFive(who_turn, size, board, index[0], index[1])
                if five == True:
                    print_board(size, board)
                    print("💥 흑 승리!! 💥\n")
                    break
                else:
                    if five == None:
                        print_board(size, board)
                        print("흑은 장목을 두면 반칙패")
                        print("💥 백 승리!! 💥\n")
                        break

                    # elif is_three_three(): # 3-3이면 무르고 다시
                    #     print("흑은 삼삼에 둘 수 없음") 
                    #     board[x_1][y_1] = 0  ### 돌을 두어보기도 전에 삼삼을 검사함 ###
                    #     continue
                    # elif is_four_four(): # 4-4여도 무르고 다시
                    #     print("흑은 사사에 둘 수 없음")
                    #     board[x_1][y_1] = 0
                    #     continue
            else:
                board[index[0], index[1]] = 1  # 백돌 두기

                if isFive(who_turn, size, board, index[0], index[1]) == True:
                    print_board(size, board)
                    print("💥 백 승리!! 💥\n")
                    break

            print_board(size, board) ## print(board)
            who_turn *= -1
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
print("띄어쓰기로 가로 세로 구분 ex) 5 7 : 가로5 세로7에 두기")
print("break : 나가기\n")

while True:

    # 바둑판 크기 정하기
    try:
        size = input("바둑판 크기 : ")
        size = int(size)
    except:
        try: size = int(list(size.split())[0])
        except: 
            if size == "break": break
            print("잘못된 값")
            continue

    # 게임 진행
    paly_omok(size)

    # 게임을 다시 시작할 건지 묻기
    if input("한판 더(1)/그만(other): ") != "1":
        break

print("프로그램 종료")
