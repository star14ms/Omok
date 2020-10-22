# 오목 룰 : 렌주룰 (흑만 3-3, 4-4, 장목(6목 이상) 모두 금지)

# 각주 종류
# (#: 설명 or 안 쓰거나 수정중인 코드, ##: 참고 코드, ###: 실수한 부분, #++: 개선할 부분, #**: 나중에 더 생각할 부분)

# 코드를 모두 접고나서, 하나씩 피면서 보는 것을 추천!

# 코드 순서 (밑의 목록들을 Ctrl + f 로 검색해서 한번에 이동!):
#1 금수 감지 code
#2 AI code
#3 pygame code
#4 main code

import numpy as np # 보드 만들기
import pygame # 게임 화면 만들기
import random # 점수가 같은 좌표들 중 하나 고르기
from datetime import datetime # 기보 날짜 기록

################################################################ 금수 감지 code

# 5목, 흑 장목 판정 (장목: 6목 이상)
def isFive(whose_turn, size, board, x, y, placed):
    if not placed: board[y][x] = whose_turn

    # ㅡ 가로로 이어진 돌 수
    num1 = 1 # 방금 둔 1개부터 세기 시작
    for x_l in range(x-1, x-6, -1): ### x -> x-1 # 6목도 감지하기 위해 (x-6)+1까지 셈
        if (x_l == -1): break
        if board[y][x_l] == whose_turn: ### 1 -> l
            num1 += 1
        else:
            break
    for x_r in range(x+1, x+6, +1): ### x -> x+1
        if (x_r == size): break
        if board[y][x_r] == whose_turn:
            num1 += 1
        else:
            break
    if num1 == 5:
        if not placed: board[y][x] = 0
        return True

    # ㅣ 세로로 이어진 돌 수
    num2 = 1
    for y_u in range(y-1, y-6, -1):  ### x-5 -> x-6(장목 검사) -> y-6 (복붙 주의)
        if (y_u == -1): break
        if board[y_u][x] == whose_turn:
            num2 += 1
        else:
            break
    for y_d in range(y+1, y+6, +1):
        if (y_d == size): break
        if board[y_d][x] == whose_turn:
            num2 += 1
        else:
            break
    if num2 == 5:
        if not placed: board[y][x] = 0
        return True

    # \ 대각선으로 이어진 돌 수 
    num3 = 1
    x_l = x
    y_u = y ### x -> y
    for i in range(5):
        if (x_l-1 == -1) or (y_u-1 == -1): break ### or -> and (while 안에 있었을 때)
        x_l -= 1
        y_u -= 1
        if board[y_u][x_l] == whose_turn:
            num3 += 1
        else: 
            break
    x_r = x
    y_d = y
    for i in range(5):
        if (x_r+1 == size) or (y_d+1 == size): break ### != -> == (while을 나오면서)
        x_r += 1
        y_d += 1
        if board[y_d][x_r] == whose_turn:
            num3 += 1
        else:
            break
    if num3 == 5:
        if not placed: board[y][x] = 0
        return True

    # / 대각선으로 이어진 돌 수
    num4 = 1
    x_l = x
    y_d = y
    for i in range(5):
        if (x_l-1 == -1) or (y_d+1 == size): break
        x_l -= 1
        y_d += 1
        if board[y_d][x_l] == whose_turn:
            num4 += 1
        else:
            break
    x_r = x
    y_u = y
    for i in range(5):
        if (x_r+1 == size) or (y_u-1 == -1): break
        x_r += 1
        y_u -= 1
        if board[y_u][x_r] == whose_turn:
            num4 += 1
        else:
            break
    if num4 == 5:
        if not placed: board[y][x] = 0
        return True
    
    if not placed: board[y][x] = 0

    if num1 > 5 or num2 > 5 or num3 > 5 or num4 > 5:
        if whose_turn == -1: ### 1 -> -1
            return True
        else:
            return None # 흑 6목 감지
    else:
        return False

# 4 개수 (4: 다음 차례에 5를 만들 수 있는 곳) (placed : xy에 돌이 두어져 있나, 안 두어져 있다면 둬보고 검사)
def num_Four(whose_turn, size, board, x, y, placed):
    four = 0
    if not placed: board[y][x] = whose_turn # 돌 두어보기

    # ㅡ 가로 4 검사
    one_pass = False # 열린 4는 두번 세지기 때문에 연속으로 나오면 패스
    for x_r in range(x-4, x+1, +1): ### x -> x+1
        if x_r > -1 and x_r+4 < size:
            line = board[y, x_r:x_r+5]

            if sum(line) == whose_turn*4:
                if one_pass == False and ( 
                    (x_r-1 > -1 and board[y][x_r-1] != whose_turn) and ### 아직 5가 아니여야 함
                    (x_r+5 < size and board[y][x_r+5] != whose_turn)):
                    four += 1
                    one_pass = True
            else:
                one_pass = False

    # ㅣ 세로 4 검사
    one_pass = False
    for y_d in range(y-4, y+1, +1):
        if y_d > -1 and y_d+4 < size:
            line = board[y_d:y_d+5, x] ### [y, y_d:y_d+5] -> [y_d:y_d+5, x]

            if sum(line) == whose_turn*4:
                if one_pass == False and (
                    (y_d-1 > -1 and board[y_d-1][x] != whose_turn) and 
                    (y_d+5 < size and board[y_d+5][x] != whose_turn)):
                    four += 1
                    one_pass = True
            else:
                one_pass = False
    
    line = [0, 0, 0, 0, 0] # 대각선 검사할 때 이용
    
    # \ 대각선 4 검사
    one_pass = False
    x_r = x-4
    y_d = y-4
    for i in range(5):
        if x_r > -1 and x_r+4 < size and y_d > -1 and y_d+4 < size:
            for k in range(5):
                line[k] = board[y_d+k][x_r+k]

            if sum(line) == whose_turn*4: ### line.sum() -> sum(line)
                if one_pass == False and (
                    (x_r-1 > -1 and y_d-1 > -1 and board[y_d-1][x_r-1] != whose_turn) and 
                    (x_r+5 < size and y_d+5 < size and board[y_d+5][x_r+5] != whose_turn)):
                    four += 1
                    one_pass = True
            else:
                one_pass = False
        
        x_r += 1
        y_d += 1
    
    # / 대각선 4 검사
    one_pass = False
    x_r = x-4
    y_u = y+4
    for i in range(5):
        if x_r > -1 and x_r+4 < size and y_u < size and y_u-4 > -1: ### (y_u < size), (y_u+4 > -1) <-> (y_u < -1) and (y_u+4 > size) 
            for k in range(5):
                line[k] = board[y_u-k][x_r+k]

            if sum(line) == whose_turn*4:
                if one_pass == False and (
                    (x_r-1 > -1 and y_u+1 < size and board[y_u+1][x_r-1] != whose_turn) and 
                    (x_r+5 < size and y_u-5 > -1 and board[y_u-5][x_r+5] != whose_turn)):
                    four += 1
                    one_pass = True
            else:
                one_pass = False
        
        x_r += 1
        y_u -= 1

    if not placed: board[y][x] = 0 # 돌 원상태로
    return four

# 3 개수 (3: 다음 차례에 열린 4를 만들 수 있는 곳)
def num_Three(whose_turn, size, board, x, y, placed):
    three = 0
    if not placed: board[y][x] = whose_turn

    # ㅡ 가로 3 검사
    for x_r in range(x-3, x+1, +1): ### x -> x+1
        if x_r > -1 and x_r+3 < size:
            line = board[y, x_r:x_r+4]
            # 범위 4칸 중 3칸에 돌이 있을 때
            if sum(line) == whose_turn*3:
                if (x_r-1 > -1) and (x_r+4 < size):
                    # 4칸 양쪽이 열려 있고, 거짓금수가 아니면 3 한번 세기
                    if (board[y][x_r-1] == 0) and (board[y][x_r+4] == 0):
                        if (whose_turn == 1) and (x_r-2 > -1) and (x_r+5 < size): # 🟨,⬛ = x_r
                            if ((board[y][x_r-2]==whose_turn) and (x_r+6 < size) and (board[y][x_r+6]==whose_turn) or # ⚫🟡(🟨⚫⚫⚫)🟡🟡⚫
                                (board[y][x_r+5]==whose_turn) and (x_r-3 > -1) and (board[y][x_r-3]==whose_turn)):    # ⚫🟡🟡(⬛⚫⚫🟡)🟡⚫
                                continue # 양방향 장목
                            if (board[y][x_r]==0) and (board[y][x_r-2]==whose_turn) and (board[y][x_r+5]==whose_turn*-1):
                                continue # 한방향 장목 # ⚫🟡(🟨⚫⚫⚫)🟡⚪
                            if (board[y][x_r+3]==0) and (board[y][x_r-2]==whose_turn*-1) and (board[y][x_r+5]==whose_turn):
                                continue # 한방향 장목 # ⚪🟡(⬛⚫⚫🟡)🟡⚫
                        three += 1
                        break # 열린 3은 두번 세지기 때문에 라인 당 한번만 세기

    # ㅣ 세로 3 검사
    for y_d in range(y-3, y+1, +1):
        if y_d > -1 and y_d+3 < size:
            line = board[y_d:y_d+4, x]

            if sum(line) == whose_turn*3:
                if (y_d-1 > -1) and (y_d+4 < size):

                    if (board[y_d-1][x] == 0) and (board[y_d+4][x] == 0):
                        if (whose_turn == 1) and (y_d-2 > -1 and y_d+5 < size):
                            if ((board[y_d-2][x]==whose_turn) and (y_d+6 < size) and (board[y_d+6][x]==whose_turn) or
                                (board[y_d+5][x]==whose_turn) and (y_d-3 > -1) and (board[y_d-3][x]==whose_turn)):
                                continue
                            if (board[y_d][x]==0) and (board[y_d-2][x]==whose_turn) and (board[y_d+5][x]==whose_turn*-1): 
                                continue
                            if (board[y_d+3][x]==0) and (board[y_d-2][x]==whose_turn*-1) and (board[y_d+5][x]==whose_turn):
                                continue
                        three += 1
                        break

    line = [0, 0, 0, 0] # 대각선 검사할 때 이용

    # \ 대각선 3 검사
    x_r = x-3 ### -4 -> -3 (복붙주의)
    y_d = y-3
    for i in range(4):
        if x_r > -1 and x_r+3 < size and y_d > -1 and y_d+3 < size:
            for k in range(4):
                line[k] = board[y_d+k][x_r+k]

            if sum(line) == whose_turn*3:
                if (x_r-1 > -1) and (y_d-1 > -1) and (x_r+4 < size) and (y_d+4 < size):
                    
                    if (board[y_d-1][x_r] == 0) and (board[y_d+4][x_r] == 0):
                        if (whose_turn == 1) and (x_r-2 > -1) and (y_d-2 > -1) and (x_r+5 < size) and (y_d+5 < size):
                            if ((board[y_d-2][x_r-2]==whose_turn) and (x_r+6 < size) and (y_d+6 < size) and (board[y_d+6][x_r+6]==whose_turn) or
                                (board[y_d+5][x_r+5]==whose_turn) and (x_r-3 > -1) and (y_d-3 > -1) and (board[y_d-3][x_r-3]==whose_turn)):
                                continue
                            if (board[y_d][x_r]==0) and (board[y_d-2][x_r-2]==whose_turn) and (board[y_d+5][x_r+5]==whose_turn*-1): 
                                continue
                            if (board[y_d+3][x_r+3]==0) and (board[y_d-2][x_r-2]==whose_turn*-1) and (board[y_d+5][x_r+5]==whose_turn):
                                continue
                        three += 1
                        break
        x_r += 1
        y_d += 1

    # / 대각선 3 검사
    x_r = x-3
    y_u = y+3
    for i in range(4):
        if x_r > -1 and x_r+3 < size and y_u+1 < size and y_u-3 > -1: ### (y_u-1 > -1), (y_u+3 < size) -> (y_u+1 < size), (y_u-3 > -1)
            for k in range(4):
                line[k] = board[y_u-k][x_r+k]

            if sum(line) == whose_turn*3:
                if (x_r-1 > -1) and (x_r+4 < size) and (y_u+1 < size) and (y_u-4 > -1): ### y_u-1, y_u+4 -> y_u+1, y_u-4
                    
                    if (board[y_u+1][x_r-1] == 0) and (board[y_u-4][x_r+4] == 0):
                        if (whose_turn == 1) and (x_r-2 > -1) and (y_u+2 < size) and (x_r+5 < size) and (y_u-5 > -1):
                            if ((board[y_u+2][x_r-2]==whose_turn) and (x_r+6 < size) and (y_u-6 > -1) and (board[y_u-6][x_r+6]==whose_turn) or
                                (board[y_u-5][x_r+5]==whose_turn) and (x_r-3 > -1) and (y_u+3 < size) and (board[y_u+3][x_r-3]==whose_turn)):
                                continue
                            if (board[y_u][x_r]==0) and (board[y_u+2][x_r-2]==whose_turn) and (board[y_u-5][x_r+5]==whose_turn*-1): 
                                continue
                            if (board[y_u-3][x_r+3]==0) and (board[y_u+2][x_r-2]==whose_turn*-1) and (board[y_u-5][x_r+5]==whose_turn):
                                continue
                        three += 1
                        break
        x_r += 1
        y_u -= 1

    if not placed: board[y][x] = 0
    return three

################################################################ AI code1 (무조건 둬야하는 수 찾기)

# 5목 만드는 좌표가 있으면 줌 (흑 차례고 금수일 땐 주지 않음, 범위: 바둑판 전체)
def canFive(whose_think, whose_turn, size, board):
    
    # 가로 감지
    for y in range(size):
        for x in range(size - 4):
            # 연속된 5칸을 잡아 그 중 4칸이 자기 돌로 차 있으면
            line = board[y, x:x+5]
            if sum(line) == whose_turn * 4:
                #  흑 금수는 제외하고, 나머지 한 칸 반환
                for i in range(5):
                    if board[y][x+i] == 0:
                        if (whose_think == 1) and ( ### 먼저 빈자리를 찾고, 그곳을 검사해야 함
                            isFive(whose_think, size, board, x+i, y, placed=False) == None or ### 백이 둘 때, 흑 장목검사는 다른 라인들을 해야 함
                            num_Four(whose_think, size, board, x+i, y, placed=False) >= 2 or ### x -> x+i
                            num_Three(whose_think, size, board, x+i, y, placed=False) >= 2):
                            continue
                        return [y, x+i]

    # 세로 감지
    for y in range(size - 4):
        for x in range(size):

            line = board[y:y+5, x]
            if sum(line) == whose_turn * 4:

                for i in range(5):
                    if board[y+i][x] == 0:
                        if (whose_think == 1) and (
                            isFive(whose_think, size, board, x, y+i, placed=False) == None or
                            num_Four(whose_think, size, board, x, y+i, placed=False) >= 2 or
                            num_Three(whose_think, size, board, x, y+i, placed=False) >= 2):
                            continue
                        return [y+i, x]
    
    # 대각선 감지
    line = [0, 0, 0, 0, 0] # 대각선 감지할 때 이용
    for y in range(size - 4):
        for x in range(size - 4):

            # \ 검사
            for i in range(5):
                line[i] = board[y+i][x+i]
            if sum(line) == whose_turn * 4:

                for i in range(5):
                    if board[y+i][x+i] == 0:
                        if (whose_think == 1) and (
                            isFive(whose_think, size, board, x+i, y+i, placed=False) == None or
                            num_Four(whose_think, size, board, x+i, y+i, placed=False) >= 2 or
                            num_Three(whose_think, size, board, x+i, y+i, placed=False) >= 2):
                            continue
                        return [y+i, x+i]

            # / 검사
            for i in range(5):
                line[i] = board[y+4-i][x+i]
            if sum(line) == whose_turn * 4:

                for i in range(5):
                    if board[y+4-i][x+i] == 0:
                        if (whose_think == 1) and (
                            isFive(whose_think, size, board, x+i, y+4-i, placed=False) == None or
                            num_Four(whose_think, size, board, x+i, y+4-i, placed=False) >= 2 or
                            num_Three(whose_think, size, board, x+i, y+4-i, placed=False) >= 2):
                            continue
                        return [y+4-i, x+i]
    
    return [None]

# 열린 4목 만드는 좌표가 있으면 줌 (흑 차례고 금수일 땐 주지 않음, 범위: 바둑판 전체)
def canFour(whose_think, whose_turn, size, board):

    canFour_xy_list = []

    # 가로 감지
    for y in range(size):
        for x in range(size - 3):
            # 연속된 4칸을 잡아 그 중 3칸이 자기 돌로 차 있으면
            line = board[y, x:x+4]
            if sum(line) == whose_turn * 3:
                # 나머지 한 칸을 채웠을 때 열린 4가 되면
                if x-1 > -1 and x+4 < size:
                    if board[y][x-1] == 0 and board[y][x+4] == 0:
                        # 흑 금수는 제외하고, 나머지 한 칸 반환
                        for i in range(4):
                            if board[y][x+i] == 0:
                                if (whose_think == 1) and (
                                    isFive(whose_think, size, board, x+i, y, placed=False) == None or
                                    num_Four(whose_think, size, board, x+i, y, placed=False) >= 2 or ### x -> x+i
                                    num_Three(whose_think, size, board, x+i, y, placed=False) >= 2):
                                    continue
                                canFour_xy_list.append([x+i, y])
    
    if len(canFour_xy_list) == 2: # 같은 라인에서 4칸 차이나는 두 좌표가 생기면 바로 반환
        return canFour_xy_list 
    horizontal_four_num = len(canFour_xy_list)

    # 세로 감지
    for y in range(size - 3):
        for x in range(size):

            line = board[y:y+4, x]
            if sum(line) == whose_turn * 3:

                if y-1 > -1 and y+4 < size:
                    if board[y-1][x] == 0 and board[y+4][x] == 0:

                        for i in range(4):
                            if board[y+i][x] == 0:
                                if (whose_think == 1) and (
                                    isFive(whose_think, size, board, x, y+i, placed=False) == None or
                                    num_Four(whose_think, size, board, x, y+i, placed=False) >= 2 or
                                    num_Three(whose_think, size, board, x, y+i, placed=False) >= 2):
                                    continue
                                canFour_xy_list.append([x, y+i])
    
    if len(canFour_xy_list) == horizontal_four_num + 2:
        return canFour_xy_list[-2:]
    vertical_four_num = len(canFour_xy_list)
        
    # 대각선 \ 감지
    line = [0, 0, 0, 0] # 대각선 감지할 때 이용
    for y in range(size - 3):
        for x in range(size - 3):
            
            for i in range(4):
                line[i] = board[y+i][x+i]
            if sum(line) == whose_turn * 3:

                if x-1 > -1 and x+4 < size and y-1 > -1 and y+4 < size:
                    if board[y-1][x-1] == 0 and board[y+4][x+4] == 0:

                        for k in range(4):
                            if board[y+k][x+k] == 0:
                                if (whose_think == 1) and (
                                    isFive(whose_think, size, board, x+i, y+i, placed=False) == None or
                                    num_Four(whose_think, size, board, x+i, y+i, placed=False) >= 2 or
                                    num_Three(whose_think, size, board, x+i, y+i, placed=False) >= 2):
                                    continue
                                canFour_xy_list.append([x+k, y+k])
    
    if len(canFour_xy_list) == vertical_four_num + 2:
        return canFour_xy_list[-2:]
    diagonal_four_num1 = len(canFour_xy_list)
    
    # 대각선 / 감지        
    for y in range(size - 3):
        for x in range(size - 3):        
        
            for i in range(4):
                line[i] = board[y+i][x+3-i]
            if sum(line) == whose_turn * 3: ### 4 -> 3 복붙

                if x+3+1 < size and x+3-4 > -1 and y-1 > -1 and y+4 < size: ### x+1 > size -> x+1 < size
                    if board[y-1][x+3+1] == 0 and board[y+4][x+3-4] == 0: ### x+1, x-4 -> x+3+1, x+3-4 (현재 x의 +3이 기준)
                        
                        for k in range(4):
                            if board[y+k][x+3-k] == 0:
                                if (whose_think == 1) and (
                                    isFive(whose_think, size, board, x+i, y+4-i, placed=False) == None or
                                    num_Four(whose_think, size, board, x+i, y+4-i, placed=False) >= 2 or
                                    num_Three(whose_think, size, board, x+i, y+4-i, placed=False) >= 2):
                                    continue
                                canFour_xy_list.append([x+3-k, y+k])
    
    if len(canFour_xy_list) == diagonal_four_num1 + 2:
        return canFour_xy_list[-2:]
    
    if len(canFour_xy_list) == 0:
        canFour_xy_list.append(None)
    return canFour_xy_list

################################################################ AI code2 (각 좌표의 가치 보드 만들기)

# 각 좌표의 가치를 보드로 줌 (현재 보드의 상태 뿐만 아니라, 각 좌표마다 돌을 뒀다 가정하고도 계산 가능) (placed : 돌을 두기 전/후 구별)
def whose_score_board(whose_turn, size, board, placed):
    
    whose_omok_score_board = np.zeros([size, size])
    mok_value_1_2 = 1.2 # 1목 당 제곱할 인자
    
    for y in range(size):
        for x in range(size):
            # 돌이 이미 놓인 자리는 0점
            if board[y][x] != 0:
                continue
            # 각 좌표에 돌을 놓아볼 때 금수 검사
            if placed:
                board[y][x] = whose_turn ### == -> =

                # 흑 금수 자리면 -2점 #** -1점으로 했더니 16진수로 표기될 때 있음
                if num_Four(1, size, board, x, y, placed=True) >= 2:
                    whose_omok_score_board[y][x] = -2
                    board[y][x] = 0 ### continue 전에도 바둑돌을 다시 물러야 함
                    continue
                if num_Three(1, size, board, x, y, placed=True) >= 2:
                    whose_omok_score_board[y][x] = -2
                    board[y][x] = 0
                    continue
                if isFive(1, size, board, x, y, placed=True) == None: 
                    whose_omok_score_board[y][x] = -2
                    board[y][x] = 0
                    continue

            value = 1
            
            # ㅡ 가로 검사
            for x_r in range(x-4, x+1, +1):
                if x_r > -1 and x_r+4 < size:
                    block = False ### 상대에게 막혔으면 그 범위는 0점
                    n_mok = 0
                    # 범위 5칸을 잡아 자기 돌의 개수를 셈 (상대편 돌이 있으면 넘어감)
                    line = board[y, x_r:x_r+5]
                    for k in range(5):
                        if line[k] == whose_turn*-1:
                            block = True
                            break
                        elif line[k] == whose_turn:
                            n_mok += 1
                    # 돌의 개수에 따라 일정 점수를 더함
                    if not block:
                        value *= mok_value_1_2**n_mok # 2**(-5+n_mok)*100 # 2**(n_mok)
                    # if x == 8 and y == 7: print(2**(-5+n_mok)*100, 2)
            
            # ㅣ 세로 검사
            for y_d in range(y-4, y+1, +1):
                if y_d > -1 and y_d+4 < size:
                    block = False
                    n_mok = 0
                    
                    line = board[y_d:y_d+5, x]
                    for k in range(5):
                        if line[k] == whose_turn*-1:
                            block = True
                            break
                        elif line[k] == whose_turn:
                            n_mok += 1
                    
                    if not block:
                        value *= mok_value_1_2**n_mok
                    # if x == 8 and y == 7: print(2**(-5+n_mok)*100, 2)
            line = [0, 0, 0, 0, 0] # 대각선 검사할 때 이용
            
            # \ 대각선 검사
            x_r = x-4
            y_d = y-4
            for i in range(5):
                if x_r > -1 and x_r+4 < size and y_d > -1 and y_d+4 < size:
                    block = False
                    n_mok = 0
                    
                    for k in range(5):
                        line[k] = board[y_d+k][x_r+k]
                        if line[k] == whose_turn*-1:
                            block = True
                            break
                        elif line[k] == whose_turn:
                            n_mok += 1
                    
                    if not block:
                        value *= mok_value_1_2**n_mok
                    # if x == 8 and y == 7: print(2**(-5+n_mok)*100, 3)
                x_r += 1 ### 점수 좌우 대칭x 이유 ->  else: continue에도 x_r, y_d += 1을 추가해야함, 애초에 continue가 필요 없음
                y_d += 1
            
            # / 대각선 검사
            x_r = x-4
            y_u = y+4
            for i in range(5):
                if x_r > -1 and x_r+4 < size and y_u < size and y_u-4 > -1:
                    block = False
                    n_mok = 0
                    
                    for k in range(5):
                        line[k] = board[y_u-k][x_r+k]
                        if line[k] == whose_turn*-1:
                            block = True
                            break
                        elif line[k] == whose_turn:
                            n_mok += 1
                    
                    if not block:
                        value *= mok_value_1_2**n_mok
                    # if x == 8 and y == 7: print(2**(-5+n_mok)*100, 4)
                x_r += 1
                y_u -= 1
            
            whose_omok_score_board[y][x] = round(value, 1)
            board[y][x] = 0
    
    return whose_omok_score_board

# 각 좌표에 돌을 두었을 때 가치 변화량을 보드로 줌
def whose_difference_score_board(whose_turn, size, board):
    
    # 돌을 두기 전/후의 점수 보드 만들기
    before_placing_score_board = whose_score_board(whose_turn, size, board, placed=False) # 돌을 두기 전
    after_placing_score_board = whose_score_board(whose_turn, size, board, placed=True) # 돌을 둔 후
    # print(before_placing_score_board, "\n")
    # print(after_placing_score_board, "\n")
    
    # 돌을 두기 전/후의 점수 차이 보드 만들기
    difference_score_board = np.zeros([size, size])
    for y in range(size):
        for x in range(size): # 둔 후 가치 - 두기 전 가치
            difference_score_board[y][x] = after_placing_score_board[y][x] - before_placing_score_board[y][x] 
    return difference_score_board

# 흑/백 양쪽의 가치 변화량 보드를 합산한 보드를 줌 (각 좌표의 최종 가치 보드) # 신 버전 #++ whose_turn 불필요
def difference_score_board(whose_turn, size, board):
    
    # 각자의 점수 보드 만들기
    oneself_score_board = whose_difference_score_board(whose_turn, size, board)
    opponent_score_board = whose_difference_score_board(whose_turn*-1, size, board)
    # print(f"\n{'흑 점수 변화량' if whose_turn == 1 else '백 점수 변화량'}")
    # print(oneself_score_board, "\n")
    # print(f"{'백 점수 변화량' if whose_turn == 1 else '흑 점수 변화량'}")
    # print(opponent_score_board, "\n")
    # print("각 좌표의 최종 가치")

    # 합산한 보드 반환
    total_score_board = np.zeros([size, size]) ### np.zeros([size, size], "\n") 이렇게 하면 음수일 때 오류남
    for y in range(size):
        for x in range(size):
            total_score_board[y][x] = oneself_score_board[y][x] + opponent_score_board[y][x]
    return total_score_board

# 보드에서 제일 높은 점수를 가지는 좌표를 줌
def xy_most_high_value(size, board, value_board):
    
    xy_most_high = [[0, 0]] # 기대점수 1위 좌표(들)
    value_most_high = 0 # 1위 점수
    
    # 바둑판의 모든 좌표를 훑어서 기대점수 1위 좌표 찾기
    for focus_y in range(size):
        for focus_x in range(size):
            
            # (1위 점수 < 현재 좌표의 점수)일 때, 현재 좌표를 1위로 (1.더 높은 점수)
            if value_most_high < value_board[focus_y][focus_x]:
                
                value_most_high = value_board[focus_y][focus_x]
                xy_most_high = [[focus_x, focus_y]]
            
            # (1위 점수 = 현재 좌표의 점수)일 때
            elif value_most_high == value_board[focus_y][focus_x]:
                
                selected_xy = select_xy_more_close([focus_x, focus_y], xy_most_high[0], board, value_board)
                
                if selected_xy == 0: # 바둑판이 비어있을 때 중앙 반환
                    return[[7,7],[[7,7]]]
                elif selected_xy == 1: # 간접주형 사라지는거 방지 (초반 직접/간접주형 모두 가능)
                    xy_most_high.append([focus_x, focus_y])

                # 현재 좌표가 돌들의 평균 위치에 더 가까우면 현재 좌표를 1위로 (간접주형 사라짐) (2.주변에 돌이 더 많은 쪽)
                elif selected_xy == [focus_x, focus_y]: 
                    xy_most_high = [[focus_x, focus_y]]
                    
                # 평균 좌표까지의 거리가 같으면 중앙에 더 가까운 쪽을 1위로 (3.중앙에 가까운 쪽)
                elif selected_xy == None:
                    select_xy = select_xy_more_center([focus_x, focus_y], xy_most_high[0], value_board)

                    if select_xy == [focus_x, focus_y]:
                        xy_most_high = [[focus_x, focus_y]]
                    
                    # 중앙까지의 거리가 같으면 현재 좌표를 1위 리스트에 추가 (4.랜덤으로 뽑기)
                    elif select_xy == None:
                        xy_most_high.append([focus_x, focus_y])

    # 공동 1위가 있을 때 랜덤으로 하나 고르기
    ran_num = random.randrange(0, len(xy_most_high))
    xy_win = xy_most_high[ran_num]
    return [xy_win, xy_most_high]

################################################################ AI code3 (상대 3을 막을 때, 두 좌표중 하나를 선택)

# 두 좌표 중 돌들의 평균 위치에 더 가까운 좌표를 내보냄
def select_xy_more_close(xy1, xy2, board, value_board):
    
    sum_x, sum_y = 0, 0 # 모든 돌의 x, y좌표값의 합
    num_stones = 0 # 바둑판에 놓인 돌 개수
    
    for focus2_y in range(size): ### focus -> focus2 새로운 변수
        for focus2_x in range(size):
            if board[focus2_y][focus2_x] == -1 or board[focus2_y][focus2_x] == 1: 
                sum_x += focus2_x
                sum_y += focus2_y
                num_stones += 1 ### value_board로 돌의 유무를 확인하면 반올림 0이 생겼을 때 돌인줄 알음
    
    if num_stones == 0:
        return 0
    elif (num_stones == 1 and value_board[7][7] == 0): ## or num_stones == 3 (돌 두개 막기)
        return 1
    avrg_x, avrg_y = round(sum_x/num_stones, 2), round(sum_y/num_stones, 2) # 전체 바둑돌의 평균 좌표
    
    if (avrg_x-xy1[0])**2 + (avrg_y-xy1[1])**2 < (avrg_x-xy2[0])**2 + (avrg_y-xy2[1])**2:
        return xy1
    elif (avrg_x-xy1[0])**2 + (avrg_y-xy1[1])**2 > (avrg_x-xy2[0])**2 + (avrg_y-xy2[1])**2:
        return xy2
    else:
        return None

# 두 좌표 중 중앙에 더 가까운 좌표를 내보냄
def select_xy_more_center(xy1, xy2, value_board):
    
    if (7-xy1[0])**2 + (7-xy1[1])**2 < (7-xy2[0])**2 + (7-xy2[1])**2:
        return xy1
    elif (7-xy1[0])**2 + (7-xy1[1])**2 > (7-xy2[0])**2 + (7-xy2[1])**2:
        return xy2
    else:
        return None

################################################################ pygame code

pygame.init()

window_length=250*3
window_high=250*3
window_num=0
screen=pygame.display.set_mode((window_length,window_high))
pygame.display.set_caption("이걸 보다니 정말 대단해!") # 제목

board_img=pygame.image.load("img\game_board.png")
board_img=pygame.transform.scale(board_img,(window_high,window_high))
size=15 # 바둑판 좌표 범위
dis=47 # 바둑판 이미지에서 격자 사이의 거리

win_black=pygame.image.load("img\win_black.png")
win_black=pygame.transform.scale(win_black,(int(300*2.5),300))

win_white=pygame.image.load("img\win_white.png")
win_white=pygame.transform.scale(win_white,(int(300*2.5),300))

select=pygame.image.load("img\select2.png")
select=pygame.transform.scale(select,(int(45*5/6),int(45*5/6)))

last_sign1=pygame.image.load("img\last_sign1.png")
last_sign1=pygame.transform.scale(last_sign1,(int(45*5/6),int(45*5/6)))

# last_sign2=pygame.image.load("img\last_sign2.png")
# last_sign2=pygame.transform.scale(last_sign2,(int(45*5/6),int(45*5/6)))

black_stone=pygame.image.load("img\wblack_stone.png")
black_stone=pygame.transform.scale(black_stone,(int(45*5/6),int(45*5/6)))

white_stone=pygame.image.load("img\white_stone.png")
white_stone=pygame.transform.scale(white_stone,(int(45*5/6),int(45*5/6)))

# my_rect1 = pygame.Rect(0,0,window_num,window_high)
# your_rect1 =  pygame.Rect(window_length-window_num,0,window_length,window_high)

play_button=pygame.image.load("img\play_button.png")
play_button=pygame.transform.scale(play_button,(250*2+14,250*1))

play_button2=pygame.image.load("img\play_button2.png")
play_button2=pygame.transform.scale(play_button2,(250*2,250*1))

selected_button=pygame.image.load("img\selected_button.png")
selected_button=pygame.transform.scale(selected_button,(250*2+14,250*1))

selected_button2=pygame.image.load("img\selected_button2.png")
selected_button2=pygame.transform.scale(selected_button2,(250*2,250*1))

pygame.mixer.music.load('bgm\딥마인드챌린지 알파고 경기 시작전 브금1.wav') # 대전 BGM
selecting_sound = pygame.mixer.Sound("sound\넘기는효과음.wav") # 게임 모드 선택 중
sound1 = pygame.mixer.Sound("sound\othree.wav") # 게임 시작!
sound2 = pygame.mixer.Sound("sound\바둑알 놓기.wav")
sound3 = pygame.mixer.Sound("sound\바둑알 꺼내기.wav")
sound4 = pygame.mixer.Sound("sound\피싱.wav") # 최후의 수!
black_foul_sound = pygame.mixer.Sound("sound\디제이스탑.wav") # 거기 두면 안 돼! 금수야! 
lose_sound = pygame.mixer.Sound("sound\[효과음]BOING.wav") # 응 졌어
AI_lose = pygame.mixer.Sound('sound\알파고 쉣낏.wav') # AI를 이겼을 때

# pygame.font.init() # pygame.init()에서 자동으로 실행됨
myfont = pygame.font.SysFont('배달의민족 한나는열한살', 80)
threethree_text = myfont.render('응~ 쌍삼~', True, (255, 0, 0)) # True의 의미 : 글자 우둘투둘해지는거 막기 (안티 에일리어싱 여부)
fourfour_text = myfont.render('응~ 사사~', True, (255, 0, 0))
six_text = myfont.render('응~ 육목~', True, (255, 0, 0))

myfont2 = pygame.font.SysFont('배달의민족 한나는열한살', 70)
foul_lose = myfont2.render('그렇게 두고 싶으면 그냥 둬', True, (255, 0, 0))

myfont3 = pygame.font.SysFont('배달의민족 한나는열한살', 40)
AI_vs_AI_mode = myfont3.render('AI vs AI 모드', True, (255, 0, 0))

def make_board(board): # 바둑알 표시하기
    for a in range(size):
        for b in range(size):
            if board[a][b]!=0 and board[a][b]==1:
                screen.blit(black_stone,(625-18+(b-7)*dis-250,375-19+(a-7)*dis)) ## 18.75 -> 19 # 소수면 콘솔창에 경고 알림 뜸
            if board[a][b]!=0 and board[a][b]==-1:
                screen.blit(white_stone,(625-18+(b-7)*dis-250,375-19+(a-7)*dis)) ## 18.75 -> 19
                
def last_stone(xy): # 마지막 돌 위치 표시하기
    screen.blit(last_sign1,(625-18+(xy[0]-7)*dis-250,375-19+(xy[1]-7)*dis)) ## 18.75 -> 19

################################################################ main code

print("\n--Python 오목! (렌주룰)--")

exit=False # 프로그램 종료

while not exit:
    pygame.display.set_caption("오목이 좋아, 볼록이 좋아? 오목!")

    whose_turn = 1 # 누구 턴인지 알려줌 (1: 흑, -1: 백)
    turn = 0
    final_turn = None # 승패가 결정난 턴 (수순 다시보기 할 때 활용)
    max_turn = size * size

    game_selected = False # 게임 모드를 선택했나?
    select_AI = True # 게임 모드
    AI_vs_AI = False # AI vs AI 모드 #############################################################################

    game_end = False # 게임 후 수순 다시보기 모드까지 끝났나?
    black_win = None # 흑,백 승패 여부
    game_over = False # 게임이 끝났나?
    game_review = False # 수순 다시보기 모드인가?

    record = [] # 기보 기록할 곳

    black_foul = False # 금수를 뒀나?
    before_foul = False # 한 수 전에 금수를 뒀나?
    stubborn_foul = False # 방향키를 움직이지 않고 또 금수를 두었나? (금수자리를 연타했나)
    foul_n_mok = 0 # 연속 금수 횟수
    threethree_foul = False
    fourfour_foul = False
    six_foul = False

    x=7 # 커서 좌표
    y=7
    y_win=375-19 ## 18.75 -> 19 # 커서 실제 위치
    x_win=625-18-250

    board = np.zeros([size, size]) # 컴퓨터가 이용할 바둑판
    screen.blit(board_img,(window_num, 0)) # 바둑판 이미지 추가
    screen.blit(play_button,(125, 100))
    screen.blit(selected_button2,(125, 400))
    pygame.display.update()
    
    print("\n게임 모드 선택")
    while not game_selected:
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                exit=True
                game_selected = True
                game_end=True
            
            elif event.type == pygame.KEYDOWN:
                
                if event.key == pygame.K_UP or event.key == pygame.K_DOWN or event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    pygame.mixer.Sound.play(selecting_sound)
                    if select_AI:
                        select_AI = False
                    else:
                        select_AI = True

                elif event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                    # if select_AI:
                    #     print("준비중")
                    #     pygame.mixer.Sound.play(black_foul_sound)
                    #     continue
                    if select_AI:
                        pygame.display.set_caption("...인간 주제에? 미쳤습니까 휴먼?")
                        print('\nAI: "후후... 날 이겨보겠다고?"')
                    else:
                        pygame.display.set_caption("나랑 같이...오목 할래?")
                    pygame.mixer.Sound.play(sound1)
                    game_selected = True
                
                elif event.key == pygame.K_ESCAPE:
                    exit=True
                    game_selected = True
                    game_end=True
                    
                if not game_selected:
                    if select_AI:
                        screen.blit(play_button,(125, 100))
                        screen.blit(selected_button2,(125, 400))
                    else:
                        screen.blit(selected_button,(125, 100))
                        screen.blit(play_button2,(125, 400))
                else:
                    screen.blit(board_img,(window_num, 0))
                    screen.blit(select,(x_win,y_win))
                pygame.display.update()

    pygame.mixer.music.play(-1) # -1 : 반복 재생
    print("\n게임 시작!")
    print(difference_score_board(whose_turn, size, board), "\n") #print
    while not game_end:
        screen.blit(board_img,(window_num, 0)) ## screen.fill(0) : 검은 화면

        # 입력 받기
        for event in pygame.event.get():

            # 창 닫기(X) 버튼을 클릭했을 때
            if event.type == pygame.QUIT:
                exit=True
                game_end=True

            # 키보드를 누르고 땔 때
            elif event.type == pygame.KEYDOWN:

                # ↑ ↓ → ← 방향키
                if event.key == pygame.K_UP: 
                    if not game_review:
                        if y_win-dis > 0:
                            y_win -= dis
                            y -= 1
                    balck_stubborn = False
                elif event.key == pygame.K_DOWN:
                    if not game_review:
                        if y_win+dis < window_high-dis:
                            y_win += dis
                            y += 1
                        balck_stubborn = False
                elif event.key == pygame.K_LEFT:
                    if not game_review:
                        if x_win-dis > window_num:
                            x_win -= dis
                            x -= 1
                        balck_stubborn = False
                    
                    elif turn > 0:
                        pygame.mixer.Sound.play(sound3)
                        turn -= 1
                        board[record[turn][0], record[turn][1]] = 0
                        last_stone_xy = [record[turn-1][0], record[turn-1][1]] # last_stone_xy : 돌의 마지막 위치
                elif event.key == pygame.K_RIGHT:
                    if not game_review:
                        if x_win+dis < window_high + window_num - dis:
                            x_win += dis
                            x += 1
                        balck_stubborn = False
                    
                    elif turn < final_turn:
                        pygame.mixer.Sound.play(sound2)
                        turn += 1
                        board[record[turn-1][0], record[turn-1][1]] = record[turn-1][2]
                        last_stone_xy = [record[turn-1][0], record[turn-1][1]]

                # 기타 키
                elif event.key == pygame.K_F1: # 바둑돌 지우기
                    pygame.mixer.Sound.play(sound3)
                    board[y][x]=0
                elif event.key == pygame.K_F2: # 검은 바둑돌
                    board[y][x]=1
                    last_stone_xy = [y,x]
                    pygame.mixer.Sound.play(sound2)
                elif event.key == pygame.K_F3: # 흰 바둑돌
                    board[y][x]=-1
                    last_stone_xy = [y,x]
                    pygame.mixer.Sound.play(sound2)
                elif event.key == pygame.K_F4: # 커서 현재 위치 출력
                    print("커서 위치:", x+1, y+1) # 컴퓨터: 0부터 셈, 사람: 1부터 셈 -> +1 
                elif event.key == pygame.K_F5: # 바둑판 비우기
                    pygame.mixer.Sound.play(sound3)
                    board = np.zeros([size, size])
                elif event.key == pygame.K_F6: # 현재 턴 출력
                    print(str(turn)+"턴째")
                elif event.key == pygame.K_F7: # 기보 출력
                    print(record)
                elif event.key == pygame.K_F8: # AI vs AI mode on/off
                    if AI_vs_AI == False:
                        AI_vs_AI = True
                    else:
                        AI_vs_AI = False
                elif event.key == pygame.K_ESCAPE: # 창 닫기
                    exit=True
                    game_end=True

                # Enter, Space 키
                elif event.key == pygame.K_RETURN and game_over: # 게임 종료
                        game_end=True
                        game_over=False
                elif event.key == pygame.K_SPACE and game_over: # 금수 연타했을 때 패배 창 제대로 못 보는거 방지
                    continue
                elif event.key == pygame.K_SPACE and not game_over: # 돌 두기

                    # 플레이어가 두기
                    if AI_vs_AI == False and (not select_AI or whose_turn == 1):
                        
                        # 이미 돌이 놓여 있으면 다시
                        if board[y][x] == -1 or board[y][x] == 1: 
                            print("돌이 그 자리에 이미 놓임")
                            pygame.mixer.Sound.play(black_foul_sound)
                            continue
                        
                        # 흑 차례엔 흑돌, 백 차례엔 백돌 두기
                        if whose_turn == 1: 
                            board[y][x] = 1
                        else:
                            board[y][x] = -1
                        
                        # 오목 생겼나 확인
                        five = isFive(whose_turn, size, board, x, y, placed=True)
                        
                        # 오목이 생겼으면 게임 종료 신호 키기, 아니면 무르기
                        if five == True:
                            if select_AI:
                                pygame.display.set_caption("다시봤습니다 휴먼!")
                            else:
                                pygame.display.set_caption("게임 종료!")
                            
                            game_over=True
                        
                        # 오목이 아닌데, 흑이면 금수 확인
                        elif whose_turn == 1:
                            
                            # 장목(6목 이상), 3-3, 4-4 금수인지 확인
                            if stubborn_foul or five == None: # black_고집 센 : 금수자리를 연타하는 경우 연산 생략
                                print("흑은 장목을 둘 수 없음")
                                black_foul = True
                                screen.blit(six_text,(235, 660))
                                if before_foul:
                                    foul_n_mok += 1
                            elif stubborn_foul or num_Four(whose_turn, size, board, x, y, placed=True) >= 2:
                                print("흑은 사사에 둘 수 없음")
                                black_foul = True
                                screen.blit(fourfour_text,(235, 660))
                                if before_foul:
                                    foul_n_mok += 1
                            elif stubborn_foul or num_Three(whose_turn, size, board, x, y, placed=True) >= 2:
                                print("흑은 삼삼에 둘 수 없음")
                                black_foul = True
                                screen.blit(threethree_text,(235, 660))
                                if before_foul:
                                       foul_n_mok += 1
                             
                            # 금수를 두면 무르고 다시 (연속 금수 10번까지 봐주기)
                            if black_foul: 
                                if foul_n_mok < 10:
                                    balck_stubborn = True
                                    pygame.mixer.Sound.play(black_foul_sound)
                                    before_foul = True
                                    black_foul = False
                                    board[y][x] = 0

                                    # 바둑알, 커서 위치 표시, 마지막 돌 표시 화면에 추가
                                    make_board(board)
                                    screen.blit(select,(x_win,y_win))
                                    last_stone([last_stone_xy[1], last_stone_xy[0]])
                                    pygame.display.update()
                                    continue
                                else:
                                    print("그렇게 두고 싶으면 그냥 둬\n흑 반칙패!")
                                    screen.blit(board_img,(window_num, 0))
                                    screen.blit(foul_lose,(5, 670))
                                    pygame.display.set_caption("이건 몰랐지?ㅋㅋ")
                                    game_over=True
                        
                        # 돌 위치 확정
                        record.append([y, x, whose_turn]) # 기보 기록
                        last_stone_xy = [y, x] # 마지막 돌 위치 기록
                        turn += 1 # 턴 추가
                        
                        if whose_turn == 1:
                            before_foul = False
                            foul_n_mok = 0
                        
                        # 승부가 결정나지 않았으면 턴 교체, 바둑판이 가득 차면 초기화
                        if not game_over:
                            pygame.mixer.Sound.play(sound2) 
                            whose_turn *= -1

                            if turn < max_turn: ### <= -> <
                                last_stone_xy = [y,x] # 마지막 놓은 자리 표시
                            else:
                                turn = 0
                                board = np.zeros([size, size])
                        else:
                            pygame.mixer.music.stop()
                            pygame.mixer.Sound.play(sound4)
    
                            if whose_turn == 1 and not black_foul:
                                black_win=True
                                if select_AI:
                                    pygame.mixer.Sound.play(AI_lose)
                                print("흑 승리!")
                            else:
                                black_win=False
                                if not black_foul:
                                    print("백 승리!")
                        # print(difference_score_board(whose_turn, size, board), "\n") #print

                    # AI가 두기
                    if AI_vs_AI == True or (AI_vs_AI == False and select_AI and whose_turn == -1) and not game_over:

                        # 무조건 둬야 하는 좌표 감지 (우선순위 1~4위)
                        self_5_xy = canFive(whose_turn, whose_turn, size, board)     # 1.자신의 5자리
                        opon_5_xy = canFive(whose_turn, whose_turn*-1, size, board)  # 2.상대의 5자리
                        self_4_xys = canFour(whose_turn, whose_turn, size, board)    # 3.자신의 열린4 자리 (최대 2곳)
                        opon_4_xys = canFour(whose_turn, whose_turn*-1, size, board) # 4.상대의 열린4 자리 (최대 2곳)
                        print("4", self_5_xy, opon_5_xy, "3", self_4_xys, opon_4_xys)
                        self_5_xy, opon_5_xy, self_4_xys, opon_4_xys = [None], [None], [None], [None]
                        # 가장 높은 가치의 좌표 감지
                        value_board = difference_score_board(whose_turn, size, board)
                        xy_most_high_list = xy_most_high_value(size, board, value_board)
                        expect_xy = xy_most_high_list[0]

                        # 우선 순위가 가장 높은 좌표를 선택
                        if self_5_xy[0] != None:
                            x, y = self_5_xy[1], self_5_xy[0]
                        elif opon_5_xy[0] != None:
                            x, y = opon_5_xy[1], opon_5_xy[0]
                        elif self_4_xys[0] != None:
                            
                            x1, y1 = self_4_xys[0][0], self_4_xys[0][1] ### value_board는 [y, x] 형태

                            # 떨어진 3일 때
                            if len(self_4_xys) == 1:
                                x, y = x1, y1
                            else: # 열린 3일 때

                                # 열린 3은 열린 4를 만드는 곳이 2곳임 (비교 필요)
                                x2, y2 = self_4_xys[1][0], self_4_xys[1][1]

                                # 기대 점수가 가장 높은 좌표와 같은 좌표를 선택 # 우선순위 1위
                                if expect_xy == [x1, y1]:
                                    x, y = x1, y1
                                elif expect_xy == [x2, y2]:
                                    x, y = x2, y2
                                else: # 돌들의 평균 위치에 더 가까운 좌표를 선택 (주변에 돌이 더 많은 쪽) # 우선순위 2위
                                    selected_xy = select_xy_more_close([x1, y1], [x2, y2], board, value_board)
                                    if selected_xy:
                                        x, y = selected_xy[0], selected_xy[1]
                                    else: # 중앙에 더 가까운 좌표를 선택 # 우선순위 3위
                                        selected_xy = select_xy_more_center([x1, y1], [x2, y2], value_board)
                                        if selected_xy:
                                            x, y = selected_xy[0], selected_xy[1]
                                        else:
                                            x, y = x1, y1
                        elif opon_4_xys[0] != None:
                            
                            x1, y1 = opon_4_xys[0][0], opon_4_xys[0][1]
                            
                            if len(opon_4_xys) == 1: ### white -> black 복붙
                                x, y = x1, y1
                            else:
                                x2, y2 = opon_4_xys[1][0], opon_4_xys[1][1]
                                
                                if expect_xy == [x1, y1]:
                                    x, y = x1, y1
                                elif expect_xy == [x2, y2]:
                                    x, y = x2, y2
                                else:
                                    selected_xy = select_xy_more_close([x1, y1], [x2, y2], board, value_board)
                                    if selected_xy:
                                        x, y = selected_xy[0], selected_xy[1]
                                    else:
                                        selected_xy = select_xy_more_center([x1, y1], [x2, y2], value_board)
                                        if selected_xy:
                                            x, y = selected_xy[0], selected_xy[1]
                                        else:
                                            x, y = x1, y1
                        else: # 우선순위 5 ~ 7위
                            xy_selected = False

                            # 5. 4-4, 4-3, 3-3자리 선택 (우선순위 5위) 
                            for y_a in range(size):
                                for x_a in range(size):
                                    
                                    if board[y_a][x_a] == 0: ### 돌이 이미 두어진 곳은 검사할 필요 없는 데다, 검사 후 돌이 사라짐
                                        self_4 = num_Four(whose_turn, size, board, x_a, y_a, placed=False) # 자신의 4 개수
                                        opon_4 = num_Four(whose_turn*-1, size, board, x_a, y_a, placed=False) # 자신의 3 개수
                                        self_3 = num_Three(whose_turn, size, board, x_a, y_a, placed=False) # 상대의 4 개수
                                        opon_3 = num_Three(whose_turn*-1, size, board, x_a, y_a, placed=False) # 상대의 3 개수
                                        # print(isFive(whose_turn, size, board, x_a, y_a, placed=False),
                                        #     num_Four(whose_turn, size, board, x_a, y_a, placed=False),
                                        #     num_Three(whose_turn, size, board, x_a, y_a, placed=False))
                                        # print(x_a+1, y_a+1, self_4, self_3, opon_4, opon_3)
                                        ### opon_4 <-> self_3, whose_turn*-1 <-> whose_turn 바뀜
                                        if whose_turn == -1 and self_4 >= 2: # 백의 4-4 공격
                                            x, y = x_a, y_a
                                            xy_selected = True
                                            break
                                        elif whose_turn*-1 == -1 and opon_4 >= 2 and ( # 흑이 백의 4-4, 방어
                                            isFive(whose_turn, size, board, x_a, y_a, placed=False) != None and
                                            num_Four(whose_turn, size, board, x_a, y_a, placed=False) < 2 and
                                            num_Three(whose_turn, size, board, x_a, y_a, placed=False) < 2):
                                            x, y = x_a, y_a
                                            xy_selected = True
                                            break
                                        
                                        elif whose_turn == 1 and self_4 == 1 and self_3 == 1: # 흑의 4-3 공격
                                            x, y = x_a, y_a
                                            xy_selected = True
                                            break                                   
                                        elif whose_turn == -1 and self_4 == 1 and self_3 == 1: # 백의 4-3 공격
                                            x, y = x_a, y_a
                                            xy_selected = True
                                            break
                                        elif whose_turn*-1 == -1 and opon_4 == 1 and opon_3 == 1 and ( # 흑이 백의 4-3 방어
                                            isFive(whose_turn, size, board, x_a, y_a, placed=False) != None and
                                            num_Four(whose_turn, size, board, x_a, y_a, placed=False) < 2 and
                                            num_Three(whose_turn, size, board, x_a, y_a, placed=False) < 2):
                                            x, y = x_a, y_a
                                            xy_selected = True
                                            break
                                        elif whose_turn*-1 == 1 and opon_4 == 1 and opon_3 == 1: # 백이 흑의 4-3 방어
                                            x, y = x_a, y_a
                                            xy_selected = True
                                            break
                                        
                                        elif whose_turn == -1 and self_3 >= 2: # 백의 3-3 공격
                                            x, y = x_a, y_a
                                            xy_selected = True
                                            break
                                        elif whose_turn*-1 == -1 and opon_3 >= 2 and ( # 흑이 백의 3-3 방어 ### self_3 -> opon_3
                                            isFive(whose_turn, size, board, x_a, y_a, placed=False) != None and
                                            num_Four(whose_turn, size, board, x_a, y_a, placed=False) < 2 and
                                            num_Three(whose_turn, size, board, x_a, y_a, placed=False) < 2):
                                            x, y = x_a, y_a
                                            xy_selected = True
                                            break
                                
                                if xy_selected: 
                                    break

                            # 6. 가장 높은 가치를 가진 좌표를 선택 (우선순위 6위)
                            if not xy_selected and board[expect_xy[1], expect_xy[0]] == 0:
                                x, y = expect_xy[0], expect_xy[1]
                                xy_selected = True
                                # if (whose_turn == -1) or (isFive(whose_turn, size, board, expect_xy[0], expect_xy[1], placed=False) != None and
                                #     num_Four(whose_turn, size, board, expect_xy[0], expect_xy[1], placed=False) < 2 and
                                #     num_Three(whose_turn, size, board, expect_xy[0], expect_xy[1], placed=False) < 2):
                                #     x, y = expect_xy[0], expect_xy[1]

                            # 7. 둘 곳이 마땅히 없을 때 빈공간을 선택 (우선순위 7위)
                            if not xy_selected:
                                for y_b in range(size):
                                    for x_b in range(size):
                                        if board[y_b][x_b] == 0:
                                            x, y = x_b, y_b
                                            xy_selected = True
                                            break
                                    if xy_selected: break ### (x == x_b) and (y == y_b) x 맨 오른쪽 끝에선 맞을 수밖에 없음

                        # 연결 기대 점수판, 기대점수 1위, 최종 우선순위 1위 좌표 출력
                        print(value_board, "\n")

                        if len(xy_most_high_list[1]) > 1:
                            print("기대점수 공동 1위:", end=" ")
                            for xy in xy_most_high_list[1]:
                                print("["+str(xy[0]+1) +","+ str(xy[1]+1)+"]", end=" ")
                            print("랜덤 뽑기")

                        print("기대점수 1위: x="+str(expect_xy[0]+1) + " y="+str(expect_xy[1]+1), end=", ")
                        print(f"{round(value_board[expect_xy[1], expect_xy[0]], 3)}점")
                        print("우선순위 1위: x="+str(x+1) + " y="+str(y+1), end=", ")
                        print(f"{round(value_board[y][x], 3)}점\n")

                        # 선택한 좌표에 돌 두기
                        board[y][x] = whose_turn

                        record.append([y, x, whose_turn])
                        last_stone_xy = [y, x]
                        turn += 1

                        x_win = 28 + dis*x # 커서 이동
                        y_win = 27 + dis*y

                        # 오목이 생겼으면 게임 종료 신호 키기
                        if isFive(whose_turn, size, board, x, y, placed=True) == True:
                            pygame.display.set_caption("나에게 복종하라 인간.")
                            game_over=True

                        # 승부가 결정나지 않았으면 턴 교체, 바둑판이 가득 차면 초기화
                        if not game_over:
                            # time.sleep(0.08) ## 바둑돌 소리 겹치지 않게 -> AI계산 시간이 길어지면서 필요없어짐
                            pygame.mixer.Sound.play(sound2)
                            whose_turn *= -1

                            if turn < max_turn: 
                                last_stone_xy = [y, x] # 마지막 놓은 자리 표시
                            else:
                                turn = 0
                                board = np.zeros([size, size])
                        else:
                            pygame.mixer.music.stop()
                            pygame.mixer.Sound.play(lose_sound)
                            if not black_foul:
                                print("백 승리!")
                        # print(difference_score_board(whose_turn, size, board), "\n") #print

                # 바둑알, 커서 위치 표시, 마지막 돌 표시, AI vs AI 모드 화면에 추가
                if not exit:
                    make_board(board)
                    if not game_review:
                        screen.blit(select,(x_win,y_win))
                    if turn != 0: # or event.key == pygame.K_F2 or event.key == pygame.K_F3
                        last_stone([last_stone_xy[1], last_stone_xy[0]])
                    if AI_vs_AI:
                        screen.blit(AI_vs_AI_mode,(520, 705))

                # 흑,백 승리 이미지 화면에 추가, 수순 다시보기 모드로 전환, 기보 저장
                if game_over and not game_review:
                    game_review = True
                    final_turn = turn
                    if black_win: # 흑 승리/백 승리 표시
                        screen.blit(win_black,(0,250))
                    else:
                        screen.blit(win_white,(0,250))

                    # 기보 파일로 저장
                    with open('GiBo.txt', 'a', encoding='utf8') as file:
                        file.write(datetime.today().strftime("%Y/%m/%d %H:%M:%S") + "\n") # YYYY/mm/dd HH:MM:SS 형태로 출력
                        for i in range(len(record)):
                            turn_hangul = "흑" if record[i][2] == 1 else "백"
                            file.write(str(record[i][0]+1)+' '+str(record[i][1]+1)+' '+turn_hangul+'\n')
                        file.write("\n")

                # 화면 업데이트
                pygame.display.update()
                
print("\nGood Bye")
pygame.quit()