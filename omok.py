#: 설명, ##: 참고 코드 ###: 실수 체크

import numpy as np
import pygame


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

################################################################ pygame

window_length=250*3
window_high=250*3
window_num=0
pygame.init()
screen=pygame.display.set_mode((window_length,window_high))
pygame.display.set_caption("오목!")

my_img=pygame.image.load("omok\game_board.png")
my_img=pygame.transform.scale(my_img,(window_high,window_high))

win_black=pygame.image.load("omok\win_black.png")
win_black=pygame.transform.scale(win_black,(int(300*2.5),300))

win_white=pygame.image.load("omok\win_white.png")
win_white=pygame.transform.scale(win_white,(int(300*2.5),300))

select=pygame.image.load("omok\select2.png")
select=pygame.transform.scale(select,(int(45*5/6),int(45*5/6)))

last_sign1=pygame.image.load("omok\last_sign1.png")
last_sign1=pygame.transform.scale(last_sign1,(int(45*5/6),int(45*5/6)))

last_sign2=pygame.image.load("omok\last_sign2.png")
last_sign2=pygame.transform.scale(last_sign2,(int(45*5/6),int(45*5/6)))

stone_b=pygame.image.load("omok\wblack_stone.png")
stone_b=pygame.transform.scale(stone_b,(int(45*5/6),int(45*5/6)))

stone_w=pygame.image.load("omok\white_stone.png")
stone_w=pygame.transform.scale(stone_w,(int(45*5/6),int(45*5/6)))

my_rect1 = pygame.Rect(0,0,window_num,window_high)
your_rect1 =  pygame.Rect(window_length-window_num,0,window_length,window_high)

play_button=pygame.image.load("omok\play_button.png")
play_button=pygame.transform.scale(play_button,(250*2+14,250*1))

play_button2=pygame.image.load("omok\play_button2.png")
play_button2=pygame.transform.scale(play_button2,(250*2,250*1))

selected_button=pygame.image.load("omok\selected_button.png")
selected_button=pygame.transform.scale(selected_button,(250*2+14,250*1))

selected_button2=pygame.image.load("omok\selected_button2.png")
selected_button2=pygame.transform.scale(selected_button2,(250*2,250*1))
# pygame.font.init()
myfont = pygame.font.SysFont('Arial', 80)
# textsurface = myfont.render('금수입니다!', False, (240, 200, 200))

def make_board(board):
    for a in range(len(board)):
        for b in range(len(board)):
            if board[a][b]!=0 and board[a][b]==-1:
                screen.blit(stone_b,(625-18+(b-7)*47-250,375-18.75+(a-7)*47))
            if board[a][b]!=0 and board[a][b]==1:
                screen.blit(stone_w,(625-18+(b-7)*47-250,375-18.75+(a-7)*47))
                
def last_stone(board):
    screen.blit(last_sign1,(625-18+(board[0]-7)*47-250,375-18.75+(board[1]-7)*47))

size=15
exit=False

while not exit:
    
    who_turn = -1
    turn = 0
    max_turn = size ** 2

    black_win=False
    game_end=False
    game_finish=False
    check=0
    y=375-18.75
    x=625-18-250
    x_1=7
    y_1=7
    dis=47
    clock=pygame.time.Clock()
    time_a=5
    turn_dol=1

    last_stone_xy=[7,7]
    board = np.zeros([size, size])
    screen.blit(my_img,(window_num,0))
    screen.blit(select,(x,y))
    pygame.display.update()

    while not game_finish:
        screen.fill(0)
        screen.blit(my_img,(window_num,0))

        for event in pygame.event.get():
            
            # 창 닫기(X) 버튼
            if event.type==pygame.QUIT:
                exit=True
                game_finish=True
            
            # 키보드를 누르고 땔 때
            if event.type == pygame.KEYDOWN:

                # ↑ ↓ → ← 방향키
                if event.key == pygame.K_UP: 
                    if y-dis > 0:
                        y -= dis
                        y_1 -= 1
                elif event.key == pygame.K_DOWN:
                    if y+dis < window_high-dis:
                        y += dis
                        y_1 += 1
                elif event.key == pygame.K_RIGHT:
                    if x+dis < window_high+window_num-dis:
                        x += dis
                        x_1 += 1
                elif event.key == pygame.K_LEFT:
                    if x-dis >window_num:
                        x -= dis
                        x_1 -= 1

                # enter 키
                elif event.key == pygame.K_RETURN and game_end ==True: 
                        game_finish=True
                elif event.key == pygame.K_RETURN and game_end ==False: 

                    # 이미 돌이 놓여 있으면 다시
                    if board[y_1][x_1] == -1 or board[y_1][x_1] == 1: 
                        print("돌이 그 자리에 이미 놓임")
                        continue

                    # 흑 차례엔 흑돌, 백 차례엔 백돌 두기
                    if who_turn == -1: 
                        board[y_1][x_1] = -1
                    else:
                        board[y_1][x_1] = 1
                    
                    five = isFive(who_turn, size, board, x_1, y_1)

                    # 오목이 생겼으면 육목 검사하고 게임 종료 신호 키기
                    if five == True:
                        game_end=True
                        if who_turn == -1:
                            black_win=True
                        else:
                            black_win=False

                    # 금수 확인
                    else:
                        if five == None:
                            print("흑은 장목을 두면 반칙패")
                            game_end=True
                            black_win=False
                        
                        # elif is_three_three(): # 3-3이면 무르고 다시
                        #     print("흑은 삼삼에 둘 수 없음")
                        #     board[x_1][y_1] = 0
                        #     continue
                        # elif is_four_four(): # 4-4여도 무르고 다시
                        #     print("흑은 사사에 둘 수 없음")
                        #     board[x_1][y_1] = 0
                        #     continue

                        # 돌이 가득 차면 바둑판 초기화
                        if turn > max_turn: 
                            who_turn *= -1
                            turn = 0
                            board= np.zeros([size, size])
                        else:
                            who_turn *= -1 # 턴 교체
                            turn += 1 # 턴 수 +1
                            last_stone_xy = [y_1,x_1] # 마지막 놓은 자리 표시
                
                # 기타 키
                elif event.key == pygame.K_F1: # 바둑돌 지우기
                    board[x_1][y_1]=0
                elif event.key == pygame.K_F2: # 검은 바둑돌
                    board[x_1][y_1]=-1
                elif event.key == pygame.K_F3: # 흰 바둑돌
                    board[x_1][y_1]=1
                elif event.key == pygame.K_F4: # 커서 현재 위치 출력
                    print("커서 위치:", x_1, y_1)
                elif event.key == pygame.K_F5: # 바둑판 비우기
                    board = np.zeros([size, size])
                elif event.key == pygame.K_F10: # 창 닫기
                    exit=True
                    game_finish=True

                # 화면 업데이트
                screen.blit(select,(x,y))
                make_board(board)
                last_stone([last_stone_xy[1],last_stone_xy[0]])

                # 게임 종료
                if game_end:
                    if black_win==True: # 흑 승
                        screen.blit(win_black,(0,250))
                    elif black_win==False: # 백 승
                        screen.blit(win_white,(0,250))
                
                pygame.display.update()
