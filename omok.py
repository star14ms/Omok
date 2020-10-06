# 렌주룰 (#: 설명 or 안 쓰는 코드, ##: 참고 코드 ###: 실수 체크)

import numpy as np
import pygame

################################################################ 흑 금수 감지 함수들

# 5목, 6목 판정
def isFive(who_turn, size, board, x, y):

    # ㅡ 가로로 이어진 돌 수
    num1 = 1 # 방금 둔 1개부터 세기 시작
    for x_l in range(x-1, x-6, -1): ### x -> x-1 # 6목도 감지하기 위해 (x-6)+1까지 셈 
        if (x_l == -1): break
        if board[y, x_l] == who_turn: ## print(x_l) ### 1 -> l
            num1 += 1
        else:
            break
    for x_r in range(x+1, x+6, +1): ### x -> x+1
        if (x_r == size): break
        if board[y, x_r] == who_turn:
            num1 += 1
        else:
            break
    if num1 == 5:
        return True
        
    # ㅣ 세로로 이어진 돌 수
    num2 = 1
    for y_u in range(y-1, y-6, -1):  ### x-5 -> x-6(장목 검사) -> y-6 (복붙 주의)
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
    y_u = y ### x -> y
    for i in range(5):
        if (x_l-1 == -1) or (y_u-1 == -1): break ### or -> and (while 안에 있었을 때)
        x_l -= 1
        y_u -= 1
        if board[y_u, x_l] == who_turn:
            num3 += 1
        else: 
            break
    x_r = x
    y_d = y
    for i in range(5):
        if (x_r+1 == size) or (y_d+1 == size): break ### != -> == (while을 나오면서)
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
            return None # 흑 6목 감지
    else:
        return False

# 4-4 판정
def isFourFour(who_turn, size, board, x, y):

    if who_turn == 1: # 백은 금지 대상이 아님
        return False
    four = 0

    # ㅡ 가로 4 검사
    one_pass = False # 열린 4는 두번 세지기 때문에 한 번 패스
    for x_r in range(x-4, x, +1):
        if x_r > -1 and x_r+4 < size:
            line = board[y, x_r:x_r+5]

            if line.sum() == who_turn*4:
                if one_pass == False:
                    four += 1
                    one_pass = True
            else:
                one_pass = False
        else:
            continue

    # ㅣ 세로 4 검사
    one_pass = False
    for y_d in range(y-4, y, +1):
        if y_d > -1 and y_d+4 < size:
            line = board[y_d:y_d+5, x] ### [y, y_d:y_d+5] -> [y_d:y_d+5, x]

            if line.sum() == who_turn*4:
                if one_pass == False:
                    four += 1
                    one_pass = True
            else:
                one_pass = False
        else:
            continue

    line = [] # 대각선 검사할 때 이용

    # \ 대각선 4 검사
    x_r = x-4
    y_d = y-4
    one_pass = False
    for i in range(5):
        if x_r > -1 and x_r+4 < size and y_d > -1 and y_d+4 < size:
            for k in range(5):
                line.append(board[y_d+k, x_r+k])
            value = sum(line) ### line.sum() -> sum(line)
            del line[:]

            if value == who_turn*4:
                if one_pass == False:
                    four += 1
                    one_pass = True
            else:
                one_pass = False
            x_r += 1
            y_d += 1
        else:
            continue

    # / 대각선 4 검사
    x_r = x-4
    y_u = y+4
    one_pass = False
    for i in range(5):
        if x_r > -1 and x_r+4 < size and y_u < size and y_u-4 > -1: ### (y_u < size), (y_u+4 > -1) <-> (y_u < -1) and (y_u+4 > size) 
            for k in range(5):
                line.append(board[y_u-k, x_r+k])
            value = sum(line)
            del line[:]

            if value == who_turn*4:
                if one_pass == False:
                    four += 1
                    one_pass = True
            else:
                one_pass = False
            x_r += 1
            y_u -= 1
        else:
            continue

    if four >= 2:
        return True
    else:
        return False

# 3-3 판정
def isThreeThree(who_turn, size, board, x, y):
    
    if who_turn == 1: # 백은 금지 대상이 아님
        return False
    three = 0

    # ㅡ 가로 3 검사
    one_pass = False # 열린 3도 두번 세지기 때문에 한 번 패스 
    for x_r in range(x-3, x+1, +1): ### x -> x+1
        if x_r > -1 and x_r+3 < size:
            line = board[y, x_r:x_r+4]

            if line.sum() == who_turn*3:
                if (one_pass == False) and (x_r-1 > -1 and x_r+4 < size):
                    if (board[y, x_r-1] == 0) and (board[y, x_r+4] == 0):
                        three += 1
                        one_pass = True
            else:
                one_pass = False
        else:
            continue
    
    # ㅣ 세로 3 검사
    one_pass = False
    for y_d in range(y-3, y+1, +1):
        if y_d > -1 and y_d+3 < size:
            line = board[y_d:y_d+4, x]

            if line.sum() == who_turn*3:
                if (one_pass == False) and (y_d-1 > -1 and y_d+4 < size):
                    if (board[y_d-1, x] == 0) and (board[y_d+4, x] == 0):
                        three += 1
                        one_pass = True
            else:
                one_pass = False
        else:
            continue

    line = [] # 대각선 검사할 때 이용

    # \ 대각선 3 검사
    x_r = x-3 ### -4 -> -3 (복붙주의)
    y_d = y-3
    one_pass = False
    for i in range(4):
        if x_r > -1 and x_r+3 < size and y_d > -1 and y_d+3 < size:
            for k in range(4):
                line.append(board[y_d+k, x_r+k])
            value = sum(line) ### line.sum() -> sum(line)
            del line[:]

            if value == who_turn*3:
                if (one_pass == False) and (x_r-1 > -1) and (x_r+4 < size) and (y_d-1 > -1) and (y_d+4 < size):
                    if (board[y_d-1, x_r-1] == 0 and board[y_d+4, x_r+4] == 0):
                        three += 1
                        one_pass = True
            else:
                one_pass = False
            x_r += 1
            y_d += 1
        else:
            continue

    # / 대각선 3 검사
    x_r = x-3
    y_u = y+3
    one_pass = False
    for i in range(4):
        if x_r > -1 and x_r+3 < size and y_u+1 < size and y_u-3 > -1: ### (y_u-1 > -1), (y_u+3 < size) -> (y_u+1 < size), (y_u-3 > -1)
            for k in range(4):
                line.append(board[y_u-k, x_r+k])
            value = sum(line)
            del line[:]

            if value == who_turn*3:
                if (one_pass == False) and (x_r-1 > -1 and x_r+4 < size and y_u+1 < size and y_u-4 > -1): ### y_u-1, y_u+4 -> y_u+1, y_u-4
                    if (board[y_u+1, x_r-1] == 0 and board[y_u-4, x_r+4] == 0): ### y_u-1, y_u+4 -> y_u+1, y_u-4
                        three += 1
                        one_pass = True
            else:
                one_pass = False
            x_r += 1
            y_u -= 1
        else:
            continue

    if three >= 2:
        return True
    else:
        return False

################################################################ pygame code

pygame.init()
window_length=250*3
window_high=250*3
window_num=0
screen=pygame.display.set_mode((window_length,window_high))
pygame.display.set_caption("이걸 보다니 정말 대단해!")

my_img=pygame.image.load("img\game_board.png")
my_img=pygame.transform.scale(my_img,(window_high,window_high))

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

# play_button=pygame.image.load("img\play_button.png")
# play_button=pygame.transform.scale(play_button,(250*2+14,250*1))

# play_button2=pygame.image.load("img\play_button2.png")
# play_button2=pygame.transform.scale(play_button2,(250*2,250*1))

# selected_button=pygame.image.load("img\selected_button.png")
# selected_button=pygame.transform.scale(selected_button,(250*2+14,250*1))

# selected_button2=pygame.image.load("img\selected_button2.png")
# selected_button2=pygame.transform.scale(selected_button2,(250*2,250*1))

sound1 = pygame.mixer.Sound("sound\피싱.wav") # 최후의 수!
sound2 = pygame.mixer.Sound("sound\othree.wav") # 게임 시작!
sound3 = pygame.mixer.Sound("sound\바둑알 놓기.wav") 
sound4 = pygame.mixer.Sound("sound\바둑알 꺼내기.wav") # 돌을 걷어낼 때 효과음 (다시보기 모드)
forbid_sound = pygame.mixer.Sound("sound\디제이스탑.wav") # 거기 두면 안 돼!
lose_sound = pygame.mixer.Sound("sound\[효과음]BOING.wav") # 응 졌어

# pygame.font.init()
# myfont = pygame.font.SysFont('Arial', 80)
# textsurface = myfont.render('금수입니다!', False, (240, 200, 200))

size=15 # 바둑판 격자 크기
dis=47 # 격자 사이의 거리

def make_board(board): # 바둑알 표시하기
    for a in range(size):
        for b in range(size):
            if board[a][b]!=0 and board[a][b]==1:
                screen.blit(black_stone,(625-18+(b-7)*dis-250,375-19+(a-7)*dis)) ## 18.75 -> 19 # 소수면 콘솔창에 경고 알림 뜸
            if board[a][b]!=0 and board[a][b]==-1:
                screen.blit(white_stone,(625-18+(b-7)*dis-250,375-19+(a-7)*dis)) ## 18.75 -> 19
                
def last_stone(board): # 마지막 돌 위치 표시하기 
    screen.blit(last_sign1,(625-18+(board[0]-7)*dis-250,375-19+(board[1]-7)*dis)) ## 18.75 -> 19

################################################################ main code

exit=False # 프로그램 종료?

while not exit:
    print("\n게임 시작!")
    pygame.display.set_caption("나랑 같이...오목 할래?")
    pygame.mixer.music.stop()
    pygame.mixer.music.load('bgm\딥마인드챌린지 알파고 경기 시작전 브금1.wav')
    pygame.mixer.music.play(-1) # -1 : 반복 재생
    pygame.mixer.Sound.play(sound2)

    who_turn = 1 # 누구 턴인지 알려줌 (-1: 흑, 1: 백)
    turn = 0
    final_turn = None # 승패가 결정난 턴 (수순 다시보기 할 때 활용)
    max_turn = size ** 2

    forbid = False # 금수를 뒀나?
    three_stack = 0 # 3-3 금수 시도 횟수
    four_stack = 0 # 4-4 금수 시도 횟수
    six_stack = 0 # 6목 이상 시도 횟수

    game_end = False # 게임 후 검토까지 끝났나?
    black_win = None # 흑,백 승패 여부
    game_over = False # 게임이 끝났나?
    game_review = False # 수순 다시보기 모드인가?
    record = [] # 기보 기록할 곳

    y=375-19 ## 18.75 -> 19
    x=625-18-250
    x_1=7
    y_1=7
    
    screen.blit(my_img,(window_num, 0)) # 바둑판 이미지 추가
    board = np.zeros([size, size]) # 컴퓨터가 이용할 바둑판
    screen.blit(select,(x,y))
    pygame.display.update()

    while not game_end:
        screen.fill(0)
        screen.blit(my_img,(window_num, 0))
        
        # 입력 받기
        for event in pygame.event.get():
            
            # 창 닫기(X) 버튼을 클릭했을 때
            if event.type == pygame.QUIT:
                exit=True
                game_end=True
            
            # 키보드를 누르고 땔 때
            if event.type == pygame.KEYDOWN:

                # ↑ ↓ → ← 방향키
                if event.key == pygame.K_UP: 
                    if not game_review:
                        if y-dis > 0:
                            y -= dis
                            y_1 -= 1
                elif event.key == pygame.K_DOWN:
                    if not game_review:
                        if y+dis < window_high-dis:
                            y += dis
                            y_1 += 1
                elif event.key == pygame.K_LEFT:
                    if not game_review:
                        if x-dis > window_num:
                            x -= dis
                            x_1 -= 1
                    elif turn > 0:
                        pygame.mixer.Sound.play(sound4)
                        turn -= 1
                        board[record[turn][0], record[turn][1]] = 0
                        last_stone_xy = [record[turn-1][0], record[turn-1][1]] # last_stone_xy : 돌의 마지막 위치
                elif event.key == pygame.K_RIGHT:
                    if not game_review:
                        if x+dis < window_high + window_num - dis:
                            x += dis
                            x_1 += 1
                    elif turn < final_turn:
                        pygame.mixer.Sound.play(sound3)
                        turn += 1
                        board[record[turn-1][0], record[turn-1][1]] = record[turn-1][2]
                        last_stone_xy = [record[turn-1][0], record[turn-1][1]]

                # enter 키
                elif event.key == pygame.K_RETURN and game_over: # 게임 종료
                        game_end=True
                        game_over=False
                elif event.key == pygame.K_SPACE and not game_over: # 돌 두기
    
                    # 이미 돌이 놓여 있으면 다시
                    if board[y_1][x_1] == -1 or board[y_1][x_1] == 1: 
                        print("돌이 그 자리에 이미 놓임")
                        pygame.mixer.Sound.play(forbid_sound)
                        continue

                    # 흑 차례엔 흑돌, 백 차례엔 백돌 두기
                    if who_turn == 1: 
                        board[y_1][x_1] = 1
                    else:
                        board[y_1][x_1] = -1
                    
                    is_five = isFive(who_turn, size, board, x_1, y_1)

                    # 오목이 생겼으면 게임 종료 신호 키기
                    if is_five == True:
                        pygame.mixer.music.stop()
                        pygame.mixer.Sound.play(sound1)
                        pygame.display.set_caption("오목이 좋아, 볼록이 좋아? 오목!")

                        record.append([y_1, x_1, who_turn]) # 기보 기록
                        last_stone_xy = [y_1,x_1]
                        turn += 1
                        game_over=True

                        if who_turn == 1:
                            black_win=True
                            print("흑 승리!")
                            # pygame.mixer.music.load('bgm\알파고 쉣낏.wav') # vs인공지능 용
                            # pygame.mixer.music.play()
                        else:
                            black_win=False
                            print("백 승리!")
                            # pygame.mixer.Sound.play(lose_sound) # vs인공지능 용
                            
                    # 금수 확인 후 돌 위치 확정
                    else:
                        # 흑만 금수 규칙이 있음
                        if who_turn == 1: 

                            if isThreeThree(who_turn, size, board, x_1, y_1):
                                print("흑은 삼삼에 둘 수 없음")
                                three_stack += 1
                                forbid = True
                            elif isFourFour(who_turn, size, board, x_1, y_1):
                                print("흑은 사사에 둘 수 없음")
                                four_stack += 1
                                forbid = True
                            elif is_five == None:
                                print("흑은 장목을 둘 수 없음")
                                six_stack += 1
                                forbid = True
                            
                            if forbid: # 금수를 두면 무르고 다시 (각 금수당 기회 10번)
                                if three_stack < 10 and four_stack < 10 and six_stack < 10:
                                    pygame.mixer.Sound.play(forbid_sound)
                                    board[y_1][x_1] = 0
                                    forbid = False
                                    continue
                                else: 
                                    print("그렇게 두고 싶으면 그냥 둬\n흑 반칙패!")
                                    pygame.mixer.music.stop()
                                    pygame.mixer.Sound.play(sound1)
                                    pygame.display.set_caption("이건 몰랐지?ㅋㅋ")

                                    last_stone_xy = [y_1,x_1]
                                    forbid = False
                                    game_over=True
                                    black_win=False
        
                        # 돌 위치 확정
                        if not game_over:
                            pygame.mixer.Sound.play(sound3) 
                            record.append([y_1, x_1, who_turn]) # 기보 기록

                            # 돌이 가득 차면 바둑판 초기화
                            if turn > max_turn:
                                who_turn *= -1 # 턴 교체
                                turn = 0
                                board = np.zeros([size, size])
                            else:
                                who_turn *= -1 
                                turn += 1 # 턴 수 +1
                                last_stone_xy = [y_1,x_1] # 마지막 놓은 자리 표시

                # 기타 키
                elif event.key == pygame.K_F1: # 바둑돌 지우기
                    board[y_1][x_1]=0
                elif event.key == pygame.K_F2: # 검은 바둑돌
                    board[y_1][x_1]=-1
                    last_stone_xy = [y_1,x_1]
                    pygame.mixer.Sound.play(sound3)
                elif event.key == pygame.K_F3: # 흰 바둑돌
                    board[y_1][x_1]=1
                    last_stone_xy = [y_1,x_1]
                    pygame.mixer.Sound.play(sound3)
                elif event.key == pygame.K_F4: # 커서 현재 위치 출력
                    print("커서 위치:", x_1, y_1)
                elif event.key == pygame.K_F5: # 바둑판 비우기
                    board = np.zeros([size, size])
                elif event.key == pygame.K_F6: # 현재 턴 출력
                    print(str(turn)+"턴째")
                elif event.key == pygame.K_F10: # 창 닫기
                    exit=True
                    game_end=True

                # 바둑알, 커서 위치 표시, 마지막 돌 표시 화면에 추가
                if not exit:
                    make_board(board)
                    if not game_review:
                        screen.blit(select,(x,y))
                    if turn != 0:
                        last_stone([last_stone_xy[1],last_stone_xy[0]])

                # 흑,백 승리 이미지 화면에 추가
                if game_over and not game_review:
                    game_review = True
                    final_turn = turn
                    if black_win: # 흑 승
                        screen.blit(win_black,(0,250))
                    else: # 백 승
                        screen.blit(win_white,(0,250))

                # 화면 업데이트
                pygame.display.update()
    
print("\nGood Bye")
pygame.quit()
