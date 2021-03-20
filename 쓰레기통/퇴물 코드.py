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

# AI 랜덤으로 두기
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

# 전체 좌표에서 가로나 세로, 대각선으로 4칸 차이나는 두 좌표만 고르기
    # 만약 3을 3개 이상 감지한다면
    # if len(canFour_xy_list) > 2:
    #     for i in range(len(canFour_xy_list)):
    #         for k in range(i+1, len(canFour_xy_list)):
    #             # 한 라인의 양쪽인 3만 출력
    #             if (((canFour_xy_list[i][0]+4 == canFour_xy_list[k][0]) and (canFour_xy_list[i][1] == canFour_xy_list[k][1])) or 
    #                 ((canFour_xy_list[i][1]+4 == canFour_xy_list[k][1]) and (canFour_xy_list[i][0] == canFour_xy_list[k][0])) or
    #                 ((canFour_xy_list[i][0]+4 == canFour_xy_list[k][0]) and (canFour_xy_list[i][1]+4 == canFour_xy_list[k][1])) or
    #                 ((canFour_xy_list[i][0]-4 == canFour_xy_list[k][0]) and (canFour_xy_list[i][1]+4 == canFour_xy_list[k][1]))):
                    
    #                 canFour_xy_list = [[canFour_xy_list[i]],[canFour_xy_list[k]]]
    #                 break

# 오목이 가능한 경우의 수 보드 만들기
def omok_cases_board(who_turn, size, board, x, y):
    
    # ㅡ 가로 4 검사
    for x_r in range(x-4, x+1, +1):
        if x_r > -1 and x_r+5 < size:
            line = board[y, x_r:x_r+6]
            
        else:
            continue
    
    # ㅣ 세로 4 검사
    for y_d in range(y-4, y+1, +1):
        if y_d > -1 and y_d+5 < size:
            line = board[y_d:y_d+6, x]

        
        else:
            continue
    
    line = [0, 0, 0, 0, 0] # 대각선 검사할 때 이용
    
    # \ 대각선 4 검사
    x_r = x-4
    y_d = y-4
    for i in range(5):
        if x_r > -1 and x_r+5 < size and y_d > -1 and y_d+5 < size:
            for k in range(5):
                line[k] = board[y_d+k, x_r+k]
        
            x_r += 1
            y_d += 1
        else:
            continue
    
    # / 대각선 4 검사
    x_r = x-4
    y_u = y+4
    for i in range(5):
        if x_r > -1 and x_r+5 < size and y_u < size and y_u-5 > -1:
            for k in range(5):
                line[k] = board[y_u-k, x_r+k]

            x_r += 1
            y_u -= 1
        else:
            continue
    
    return

# 두 좌표 중 주변 8곳의 점수의 합이 더 높은 좌표를 내보냄
def select_xy_more_potential_valuable(xy1, xy2, value_board):
    
    if forbid_xy1 and forbid_xy2: return None
    xys = [xy1, xy2]
    sum_value = 0
    xy1_surrounding_8_value = 0
    xy2_surrounding_8_value = 0
    
    for xy in xys:
        if xy[0]-1 > -1   and xy[1]-1 > -1:   sum_value += value_board[xy[1]-1, xy[0]-1]
        if xy[0]          and xy[1]-1 > -1:   sum_value += value_board[xy[1]-1, xy[0]]
        if xy[0]+1 < size and xy[1]-1 > -1:   sum_value += value_board[xy[1]-1, xy[0]+1]
        if xy[0]-1 > -1   and xy[1]:          sum_value += value_board[xy[1], xy[0]-1]
        if xy[0]+1 < size and xy[1]:          sum_value += value_board[xy[1], xy[0]+1]
        if xy[0]-1 > -1   and xy[1]+1 < size: sum_value += value_board[xy[1]+1, xy[0]-1]
        if xy[0]          and xy[1]+1 < size: sum_value += value_board[xy[1]+1, xy[0]]
        if xy[0]+1 < size and xy[1]+1 < size: sum_value += value_board[xy[1]+1, xy[0]-1]
        
        if xy == xy1:
            xy1_surrounding_8_value = sum_value
        else:
            xy2_surrounding_8_value = sum_value
        sum_value = 0 ### 초기화
    
    if xy1_surrounding_8_value > xy2_surrounding_8_value and not forbid_xy1:
        return xy1
    elif xy1_surrounding_8_value < xy2_surrounding_8_value and not forbid_xy2:
        return xy2
    else:
        return None

# "제일 높은 연결 기대점수를 가지는 좌표를 줌" 코드 정리 전
                # sum_x, sum_y = 0, 0 # 모든 돌의 x, y좌표값의 합
                # num_stones = 0 # 바둑판에 놓인 돌 개수
                
                # for focus2_y in range(size): ### focus -> focus2 새로운 변수
                #     for focus2_x in range(size):
                #         if board[focus2_y, focus2_x] == -1 or board[focus2_y, focus2_x] == 1: 
                #             sum_x += focus2_x
                #             sum_y += focus2_y
                #             num_stones += 1 ### value_board로 돌의 유무를 확인하면 반올림 0이 생겼을 때 돌인줄 알음
                
                # if num_stones != 0:
                #     avrg_x, avrg_y = round(sum_x/num_stones, 1), round(sum_y/num_stones, 1) # 전체 바둑돌의 평균 좌표
                # else:
                #     return[[7,7],[[7,7]]]
                
                # # 간접주형 사라지는거 방지 (초반 직접/간접주형 모두 가능)
                # if (num_stones == 1 and value_board[7, 7] == 0): ## or num_stones == 3 (돌 두개 막기)
                #     xy_most_high.append([focus_x, focus_y])
                
                # # 현재 좌표가 돌들의 평균 위치에 더 가까우면 현재 좌표를 1위로 (간접주형 사라짐) (2.주변에 돌이 더 많은 쪽)
                # elif (avrg_x-focus_x)**2 + (avrg_y-focus_y)**2 < (avrg_x-xy_most_high[0][0])**2 + (avrg_y-xy_most_high[0][1])**2:
                #     xy_most_high = [[focus_x, focus_y]]
                
                # # 평균 좌표까지의 거리가 같으면 중앙에 더 가까운 쪽을 1위로 (3.중앙에 가까운 쪽)
                # elif (avrg_x-focus_x)**2 + (avrg_y-focus_y)**2 == (avrg_x-xy_most_high[0][0])**2 + (avrg_y-xy_most_high[0][1]):
                    
                #     select_xy = select_xy_more_center([focus_x, focus_y], xy_most_high[0], value_board)

                #     if select_xy == [focus_x, focus_y]:
                #         xy_most_high = [[focus_x, focus_y]]
                    
                #     # 중앙까지의 거리가 같으면 현재 좌표를 1위 리스트에 추가 (4.랜덤으로 뽑기)
                #     elif select_xy == None:
                #         xy_most_high.append([focus_x, focus_y])

# 연결된 N목 판정 (백 전용(금수무시), 범위: 바둑판 전체)
def is_n_mok(n_mok, whose_turn, size, board):

    # 가로
    for y in range(size):
        for x in range(size - 4):

            line = board[y, x:x+n_mok]
            if sum(line) == whose_turn * n_mok:
                return True

    # 세로
    for y in range(size - 4):
        for x in range(size):

            line = board[y:y+n_mok, x]
            if sum(line) == whose_turn * n_mok:
                return True

    # 대각선
    line = [0, 0, 0, 0, 0] # 대각선 검사할 때 이용
    for y in range(size - 4):
        for x in range(size - 4):

            # \ 검사
            for i in range(n_mok):
                line[i] = board[y+i, x+i]
            if sum(line) == whose_turn * n_mok:
                return True
   
            # / 검사
            for i in range(n_mok):
                line[i] = board[y+i, x+(n_mok-1)-i]
            if sum(line) == whose_turn * n_mok:
                return True

    return False

# 각 좌표의 연결 기대점수 보드를 줌 # 구 버전
def win_value_board(size, board):
    
    value_board = np.zeros([size, size])
    
    # 기대점수 계산 인자 (좌표 주변의 상태)
    start_value = 1 # 초기 점수
    next_to_value = 2 # 주변 돌의 영향력 ⚪⚪
    blank_value = 1.25 # 주변 돌까지의 공백의 영향력 ⚪🟡⚪ (각 라인의 기댓값을 곱한다면 1.25, 더한다면 1.8)
    blank_bfcls_value = 2 # 주변 돌 너머 막히기 전까지 공백의 영향력 ⚪🟡⚪🟡⚫ # bfcls : blank before close
    #++ 추가 필요? : 주변 돌이 아군인지 적군인지 -> 현재 턴과 상관없이 바둑판의 상태만 봐야함?
    
    for focus_y in range(size):
        for focus_x in range(size):
            
            # 자리가 비어있을 때만 계산하고 채워져있으면 0점
            if board[focus_y, focus_x] == 0: ### x, y -> y, x board에선 바뀜
                
                # 금수 자리면 -1점
                if num_Four(1, size, board, focus_x, focus_y, placed=False) >= 2:
                    value_board[focus_y, focus_x] = -1
                    board[focus_y, focus_x] = 0 ### continue 전에도 바둑돌을 다시 물러야 함
                    continue
                if num_Three(1, size, board, focus_x, focus_y, placed=False) >= 2:
                    value_board[focus_y, focus_x] = -1
                    board[focus_y, focus_x] = 0
                    continue
                if isFive(1, size, board, focus_x, focus_y, placed=False) == None: 
                    value_board[focus_y, focus_x] = -1
                    board[focus_y, focus_x] = 0
                    continue
                
                value = 0 # 가로, 세로, 양 대각선 연결 기대점수의 총합
                
                # 가로 ㅡ쪽 점수
                horizontal_value = start_value # 가로 방향 점수
                blank1, blank2 = 0, 0 # 처음 만난 돌까지의 공백 수 (좌우 각각)
                next_to_color = None # 처음 만난 색깔 (좌1, 우1, 좌2, 우2,...)
                find_stone1, find_stone2 = False, False # 바둑판 끝에 도달하기 전 돌을 만났는지 여부 (좌우 각각)
                blank_before_close1, blank_before_close2 = 0, 0 # 처음 만난 돌 색깔 기준 그 너머 상대 색깔로 막힌 곳까지의 공백 (좌우 각각)
                close1, close2 = False, False # 좌우 막혔는지 여부
                for i in range(1, 5): # 좌우 4칸 감지
                    if (focus_x-i > -1) and not close1:
                        if next_to_color == None and board[focus_y, focus_x-i] != 0:
                            next_to_color = board[focus_y, focus_x-i]
                            find_stone1 = True
                        if board[focus_y, focus_x-i] == 0:
                            if next_to_color == None: # 밑 코드에서 오류 -> 모두 elif로 -> 그 아래코드로 못 감 -> 0일때 조건문 안에서(근본)
                                blank1 += 1 # 돌이 멀리 떨어져 있을수록 기대점수가 줄음
                            else:
                                blank_before_close1 += 1
                        elif board[focus_y, focus_x-i] == next_to_color:
                            horizontal_value *= next_to_value/(blank_value**blank1) # 내 돌은 멀어질수록 덜 좋음
                        else:
                            close1 = True
                    else:
                        if not find_stone1: ### next_to_color로 검사하면 반대쪽 방향에선 돌을 만나지 않아도 통과할 수도 있음
                            blank_before_close1 = blank1
                        close1 = True
                    
                    if (focus_x+i < size) and not close2: # 반대 방향으로도 검사
                        if next_to_color == None and board[focus_y, focus_x+i] != 0:
                            next_to_color = board[focus_y, focus_x+i]
                            find_stone2 = True            
                        if board[focus_y, focus_x+i] == 0:
                            if next_to_color == None:
                                blank2 += 1
                            else:
                                blank_before_close2 += 1
                        elif board[focus_y, focus_x+i] == next_to_color:
                            horizontal_value *= next_to_value/(blank_value**blank2)
                        else:
                            close2 = True
                    else:
                        if not find_stone2:
                            blank_before_close2 = blank2
                        close2 = True
                
                half_horizontal_value = horizontal_value/2 ### (총 가로 점수 / 2)가 변하지 않도록 따로 만들어줌
                if close1: horizontal_value -= (half_horizontal_value/(blank_bfcls_value**blank_before_close1)) ### (()
                if close2: horizontal_value -= (half_horizontal_value/(blank_bfcls_value**blank_before_close2))
                
                # 세로 ㅣ쪽 점수
                vertical_value = start_value
                blank1, blank2 = 0, 0
                next_to_color = None
                find_stone1, find_stone2 = False, False
                blank_before_close1, blank_before_close2 = 0, 0
                close1, close2 = False, False
                for i in range(1, 5):
                    if (focus_y-i > -1) and not close1:
                        if next_to_color == None and board[focus_y-i, focus_x] != 0:
                            next_to_color = board[focus_y-i, focus_x]
                            find_stone1 = True
                        if board[focus_y-i, focus_x] == 0:
                            if next_to_color == None:
                                blank1 += 1
                            else:
                                blank_before_close1 += 1
                        elif board[focus_y-i, focus_x] == next_to_color:
                            vertical_value *= next_to_value/(blank_value**blank1) ### horizontal -> vertical 복붙
                        else:
                            close1 = True
                    else:
                        if not find_stone1:
                            blank_before_close1 = blank1
                        close1 = True

                    if (focus_y+i < size) and not close2:
                        if next_to_color == None and board[focus_y+i, focus_x] != 0:
                            next_to_color = board[focus_y+i, focus_x]
                            find_stone2 = True
                        if board[focus_y+i, focus_x] == 0:
                            if next_to_color == None:
                                blank2 += 1
                            else:
                                blank_before_close2 += 1
                        elif board[focus_y+i, focus_x] == next_to_color:
                            vertical_value *= next_to_value/(blank_value**blank2)
                        else:
                            close2 = True
                    else:
                        if not find_stone2:
                            blank_before_close2 = blank2
                        close2 = True
                
                half_vertical_value = vertical_value/2
                if close1: vertical_value -= (half_vertical_value/(blank_bfcls_value**blank_before_close1))
                if close2: vertical_value -= (half_vertical_value/(blank_bfcls_value**blank_before_close2))
                
                # 대각선 \쪽 점수
                diagonal_value1 = start_value
                blank1, blank2 = 0, 0
                next_to_color = None
                find_stone1, find_stone2 = False, False
                blank_before_close1, blank_before_close2 = 0, 0
                close1, close2 = False, False
                for i in range(1, 5):
                    if (focus_x-i > -1) and (focus_y-i > -1) and not close1:
                        if next_to_color == None and board[focus_y-i, focus_x-i] != 0:
                            next_to_color = board[focus_y-i, focus_x-i]
                            find_stone1 = True            
                        if board[focus_y-i, focus_x-i] == 0:
                            if next_to_color == None:
                                blank1 += 1
                            else:
                                blank_before_close1 += 1
                        elif board[focus_y-i, focus_x-i] == next_to_color:
                            diagonal_value1 *= next_to_value/(blank_value**blank1)
                        else:
                            close1 = True
                    else:
                        if not find_stone1:
                            blank_before_close1 = blank1
                        close1 = True
                
                    if (focus_x+i < size) and (focus_y+i < size) and not close2:
                        if next_to_color == None and board[focus_y+i, focus_x+i] != 0:
                            next_to_color = board[focus_y+i, focus_x+i]
                            find_stone2 = True            
                        if board[focus_y+i, focus_x+i] == 0:
                            if next_to_color == None:
                                blank2 += 1
                            else:
                                blank_before_close2 += 1
                        elif board[focus_y+i, focus_x+i] == next_to_color:
                            diagonal_value1 *= next_to_value/(blank_value**blank2)
                        else:
                            close2 = True
                    else:
                        if not find_stone2:
                            blank_before_close2 = blank2
                        close2 = True
                
                half_diagonal_value1 = diagonal_value1/2
                if close1: diagonal_value1 -= (half_diagonal_value1/(blank_bfcls_value**blank_before_close1))
                if close2: diagonal_value1 -= (half_diagonal_value1/(blank_bfcls_value**blank_before_close2))
                
                # 대각선 /쪽 점수
                diagonal_value2 = start_value
                blank1, blank2 = 0, 0
                next_to_color = None
                find_stone1, find_stone2 = False, False
                blank_before_close1, blank_before_close2 = 0, 0
                close1, close2 = False, False
                for i in range(1, 5):
                    if (focus_x-i > -1) and (focus_y+i < size) and not close1:
                        if next_to_color == None and board[focus_y+i, focus_x-i] != 0:
                            next_to_color = board[focus_y+i, focus_x-i]
                            find_stone1 = True            
                        if board[focus_y+i, focus_x-i] == 0:
                            if next_to_color == None:
                                blank1 += 1
                            else:
                                blank_before_close1 += 1
                        elif board[focus_y+i, focus_x-i] == next_to_color:
                            diagonal_value2 *= next_to_value/(blank_value**blank1)
                        else:
                            close1 = True
                    else:
                        if not find_stone1:
                            blank_before_close1 = blank1
                        close1 = True
                
                    if (focus_x+i < size) and (focus_y-i > -1) and not close2:
                        if next_to_color == None and board[focus_y-i, focus_x+i] != 0:
                            next_to_color = board[focus_y-i, focus_x+i]
                            find_stone2 = True
                        if board[focus_y-i, focus_x+i] == 0:
                            if next_to_color == None:
                                blank2 += 1
                            else:
                                blank_before_close2 += 1
                        elif board[focus_y-i, focus_x+i] == next_to_color:
                            diagonal_value2 *= next_to_value/(blank_value**blank2)
                        else:
                            close2 = True
                    else:
                        if not find_stone2:
                            blank_before_close2 = blank2
                        close2 = True
                
                half_diagonal_value2 = diagonal_value2/2
                if close1: diagonal_value2 -= (half_diagonal_value2/(blank_bfcls_value**blank_before_close1))
                if close2: diagonal_value2 -= (half_diagonal_value2/(blank_bfcls_value**blank_before_close2))
                
                # 각 자리마다 연결 기대점수를 저장
                value = (horizontal_value * vertical_value * diagonal_value1 * diagonal_value2)
                value_board[focus_y, focus_x] = round(value, 3) # 연결 기대점수 정확도 (소수 3째 자리까지 반올림)
                value = 0 ### 초기화
    
    return value_board
    
# 각 좌표에 돌을 두었을 때 가치 변화량을 보드로 줌
def whose_difference_score_board(whose_turn, size, board):
    
    # 돌을 두기 전/후의 점수 보드 만들기
    before_placing_score_board = sum_adjacent_scores_board(whose_turn, size, board, placed=False) # 돌을 두기 전
    after_placing_score_board = sum_adjacent_scores_board(whose_turn, size, board, placed=whose_turn) # 돌을 둔 후
    # print(before_placing_score_board, "\n")
    # print(after_placing_score_board, "\n")
    
    # 돌을 두기 전/후의 점수 차이 보드 만들기
    difference_score_board = np.zeros([size, size])
    for y in range(size):
        for x in range(size): # 둔 후 가치 - 두기 전 가치
            difference_score_board[y][x] = after_placing_score_board[y][x] - before_placing_score_board[y][x] 
    
    return difference_score_board

