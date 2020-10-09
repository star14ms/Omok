# 5목 판정 (전체 판을 훑는 AI에게 유용함)
def is_five(who_turn, size, board):  

    # 가로 5줄
    for y in range(size):
        for x in range(size - 4):
            line = board[y, x:x+5]
            if line.sum() == who_turn * 5:
                return who_turn
        
    # 세로 5줄
    for y in range(size - 4):
        for x in range(size):
            line = board[y:y+5, x]
            if line.sum() == who_turn * 5:
                return who_turn

    # 대각선 \ or / 5줄
    for y in range(size - 4):
        for x in range(size - 4):
            line[0] = board[y, x]
            line[1] = board[y+1, x+1]
            line[2] = board[y+2, x+2]
            line[3] = board[y+3, x+3]
            line[4] = board[y+4, x+4]
            if line.sum() == who_turn * 5:
                line[0], line[1], line[2], line[3], line[4] = 0,0,0,0,0 ### 
                return who_turn
            line[0], line[1], line[2], line[3], line[4] = 0,0,0,0,0 ### 초기화 필요 ###

            line[0] = board[y, x+4]
            line[1] = board[y+1, x+3]
            line[2] = board[y+2, x+2]
            line[3] = board[y+3, x+1]
            line[4] = board[y+4, x]
            if line.sum() == who_turn * 5:
                line[0], line[1], line[2], line[3], line[4] = 0,0,0,0,0 ###
                return who_turn
            line[0], line[1], line[2], line[3], line[4] = 0,0,0,0,0 ###

# 4목, 5목, 6목 판정 (떨어진4 감지 안 됌)
def how_long(who_turn, size, board, x, y):

    # 4-4 검사
    four = 0

    # ㅡ 가로로 이어진 돌 수
    num1 = 1
    for x_l in range(x-1, x-6, -1): ### x -> x-1 ### 
        if (x_l == -1): break
        if board[y, x_l] == who_turn: ## print(x_l) ### 1 -> l ###
            num1 += 1

            if num1 == 4:
                if x_l-1 > -1 and board[y, x_l-1] == 0:
                    four += 1
                elif x_l+4 < size and board[y, x_l+4] == 0:
                    four += 1
        else:
            break
    for x_r in range(x+1, x+6, +1): ### x -> x+1 ###
        if (x_r == size): break
        if board[y, x_r] == who_turn:
            num1 += 1

            if num1 == 4:
                if x_r+1 > -1 and board[y, x_r+1] == 0:
                    four += 1
                elif x_r-4 < size and board[y, x_r-4] == 0:
                    four += 1
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

            if num2 == 4:
                if y_u-1 > -1 and board[y_u-1, x] == 0:
                    four += 1
                elif y_u+4 < size and board[y_u+4, x] == 0:
                    four += 1
        else:
            break
    for y_d in range(y+1, y+6, +1):
        if (y_d == size): break
        if board[y_d, x] == who_turn:
            num2 += 1

            if num2 == 4:
                if y_d+1 > -1 and board[y_d+1, x] == 0:
                    four += 1
                elif y_d-4 < size and board[y_d-4, x] == 0:
                    four += 1
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

            if num3 == 4:
                if x_l-1 > -1 and y_u-1 > -1 and  board[y_u-1, x_l-1] == 0:
                    four += 1
                elif x_l+4 < size and y_u+4 < size and board[y_u+4, x_l+4] == 0:
                    four += 1
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

            if num3 == 4:
                if x_r+1 > -1 and y_d+1 > -1 and board[y_d+1, x_r+1] == 0:
                    four += 1
                elif x_r-4 < size and y_d-4 < size and board[y_d-4, x_r-4] == 0:
                    four += 1
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

            if num4 == 4:
                if x_l-1 > -1 and y_d+1 < size and  board[y_d+1, x_l-1] == 0:
                    four += 1
                elif x_l+4 < size and y_d-4 > -1 and board[y_d-4, x_l+4] == 0:
                    four += 1
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

            if num4 == 4:
                if x_r+1 < size and y_u-1 > -1 and board[y_u-1, x_r+1] == 0:
                    four += 1
                elif x_r-4 > -1 and y_u+4 < size and board[y_u+4, x_r-4] == 0:
                    four += 1
        else:
            break
    if num4 == 5:
        return True
    
    if num1 > 5 or num2 > 5 or num3 > 5 or num4 > 5:
        if who_turn == 1:
            return True
        else:
            return 6 # 흑 6목 감지
    else:
        if four >= 2 and who_turn == -1: 
            return 4 # 흑 4-4 감지
        else:
            return False

# 제일 높은 연결 기대점수를 가지면서 중앙과 가까운 좌표를 줌 #++ 중앙과 가까운가 대신 주변에 돌이 많이 분포해 있는가로
def most_high_value(value_board):
    
    select_xy = [None, None] # 선택된 좌표
    select_xy_value = 0 # 선택된 좌표의 점수
    
    for focus_y in range(size):
        for focus_x in range(size):
            # (선택된 좌표의 점수 < 현재 좌표의 점수)일 때 현재 좌표를 선택
            if select_xy_value < value_board[focus_y, focus_x]:

                select_xy_value = value_board[focus_y, focus_x]
                select_xy = [focus_x, focus_y]
            # (선택된 좌표의 점수 = 현재 좌표의 점수)일 때
            elif select_xy_value == value_board[focus_y, focus_x]:
                # 놓여 있는 돌들의 평균 좌표를 구함 (주변에 돌이 가장 많은 곳: 그 돌들에게 영향을 주기 위해)
                sum_x, sum_y = 0, 0
                stone_num = 0
                for focus_y in range(size): # 위랑 똑같은 반복문: 당장 모든 좌표를 감지해야하기 때문
                    for focus_x in range(size):
                        if value_board[focus_y, focus_x] == 0:
                            stone_num += 1
                            sum_x += focus_x
                            sum_y += focus_y
                Average_x, Average_y = (round(sum_x/stone_num)), (round(sum_y/stone_num))

                # 중앙에 더 가까우면 현재 좌표를 선택 ##++ 거리가 같으면 이전 값을 선택 ##++ 중앙에 더 가까우면 -> 주변이 채워져있는 곳
                if (7-focus_x)**2 + (7-focus_y)**2 < (7-select_xy[0])**2 + (7-select_xy[1]):
                    
                    select_xy_value = value_board[focus_y, focus_x]
                    select_xy = [focus_x, focus_y]
    
    return select_xy

import random
size = 15

# 제일 높은 연결 기대점수를 가지는 좌표를 줌
def xy_most_high_value(value_board):
    
    xy_most_high = [] # 기대점수 1위 좌표
    value_most_high = 0 # 1위 점수
    
    # 바둑판의 모든 좌표를 훑어서 기대점수 1위 좌표 찾기
    for focus_y in range(size):
        for focus_x in range(size):
            
            # (1위 점수 < 현재 좌표의 점수)일 때, 현재 좌표를 1위로 (1.더 높은 점수)
            if value_most_high < value_board[focus_y, focus_x]:
                
                value_most_high = value_board[focus_y, focus_x]
                xy_most_high = [[focus_x, focus_y]]

            
            elif value_most_high == value_board[focus_y, focus_x]:

                # (1위 점수 = 현재 좌표의 점수)일 때, 주위 날일자 8곳에 채워진 돌이 더 많은 좌표를 1위로 (2.주변에 돌이 많이 분포)
                two_xys = [[focus_x, focus_y], xy_most_high[0]]  
                difference_num_stones = 0
                
                for xy in two_xys:
                    knight_stones = 0
                    if xy[1]-2 > -1 and xy[0]-1 > -1 and value_board[xy[1]-2, xy[0]-1] == 0: knight_stones += 1
                    if xy[1]-2 > -1 and xy[0]+1 < size and value_board[xy[1]-2, xy[0]+1] == 0: knight_stones += 1
                    if xy[1]+2 < size and xy[0]-1 > -1 and value_board[xy[1]+2, xy[0]-1] == 0: knight_stones += 1
                    if xy[1]+2 < size and xy[0]+1 < size and value_board[xy[1]+2, xy[0]+1] == 0: knight_stones += 1
                    if xy[1]-1 > -1 and xy[0]-2 > -1 and value_board[xy[1]-1, xy[0]-2] == 0: knight_stones += 1
                    if xy[1]+1 < size and xy[0]-2 > -1 and value_board[xy[1]+1, xy[0]-2] == 0: knight_stones += 1
                    if xy[1]-1 > -1 and xy[0]+2 < size and value_board[xy[1]-1, xy[0]+2] == 0: knight_stones += 1
                    if xy[1]+1 < size and xy[0]+2 < size and value_board[xy[1]+1, xy[0]+2] == 0: knight_stones += 1
                    
                    if xy != xy_most_high: difference_num_stones += knight_stones
                    else: difference_num_stones -= knight_stones
                
                if difference_num_stones > 0:
                    xy_most_high = [[focus_x, focus_y]] 
                
                # 주위 날일자에 채워진 돌의 개수가 같을 때 #** 주변의 더 먼 돌은 고려 못함
                elif difference_num_stones == 0: 
                    
                    # 중앙에 더 가까우면 현재 좌표를 1위로 (초반 포월주형 제외) (3.중앙에 가까움)
                    if (7-focus_x)**2 + (7-focus_y)**2 < (7-xy_most_high[0])**2 + (7-xy_most_high[1]):
                        value_most_high = value_board[focus_y, focus_x]
                        xy_most_high = [focus_x, focus_y]
                    
                    # 중앙까지의 거리가 같으면 현재 좌표를 1위 리스트에 추가 (초반 화월주형만) (4.랜덤으로 뽑기)
                    elif (7-focus_x)**2 + (7-focus_y)**2 == (7-xy_most_high[0])**2 + (7-xy_most_high[1]):
                        xy_most_high.append([focus_x, focus_y])
     
    # 공동 1위가 있을 때
    if len(xy_most_high) > 0:
        
        # 랜덤으로 하나 고르기
        ran_num = random.randrange(0, len(xy_most_high))
        xy_win = xy_most_high[ran_num]
    
    return [xy_win, xy_most_high]

# AI가 두기
                        # else: # 우선순위에 속하지 않으면 x, y값 랜덤으로 잡기 (범위: 마지막 돌의 각 좌표의 +-2칸)
                        #     while True:
                        #         x = random.randrange(last_stone_xy[1]-2, last_stone_xy[1]+3)
                        #         y = random.randrange(last_stone_xy[0]-2, last_stone_xy[0]+3)
                        #         if x <= -1 or x >= size or y <= -1 or y >= size:
                        #             continue # 범위가 바둑판을 벗어나면
                        #         if board[y][x] == -1 or board[y][x] == 1:
                        #             continue # 이미 돌이 놓여 있으면 다시
                        #         if num_Four(who_turn, size, board, x, y) >= 2 or num_Three(who_turn, size, board, x, y) >= 2:
                        #             continue # 3-3이나 4-4면 다시 # 흑 전용
                        #         break

# 두 좌표의 기댓값, 중앙까지 거리 비교
                                # xy1_value = value_board[y1, x1]
                                # xy2_value = value_board[y2, x2]
                                # # 두 곳중 더 높은 기대점수를 가진 곳을 선택
                                # if xy1_value > xy2_value:
                                #     x, y = x1, y1
                                # elif xy1_value < xy2_value:
                                #     x, y = x2, y2
                                # else: # 기대점수가 같으면 중앙에 더 가까운 쪽을 선택
                                #     if (7-x1)**2 + (7-y1)**2 <= (7-x2)**2 + (7-y2)**2: # 중앙으로부터의 거리의 제곱
                                #         x, y = x1, y1
                                #     else:
                                #         x, y = x2, y2