# def game_visualize(board_img, ball, position):
#   ball_size = ball.shape[0]
#   step_size = 48
#   off_set = 7

#   y_step = step_size*position[0] - round(step_size/2) + off_set
#   x_step = step_size*position[0] - round(step_size/2) + off_set

#   board_img[y_step : y_step + ball_size, x_step : x_step + ball_size] - ball

#   plt.imshow(board_img)


import pygame

window_length=250*3
window_high=250*3
window_num=0#window_high/3
pygame.init()
screen=pygame.display.set_mode((window_length,window_high)) # 크기 150*150
pygame.display.set_caption("오목!")
finish=False

my_img=pygame.image.load("omok\game_board.png")
my_img=pygame.transform.scale(my_img,(window_high,window_high))

#a=300
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
pygame.font.init()
myfont = pygame.font.SysFont('Arial', 80)
textsurface = myfont.render('금수입니다!', False, (240, 200, 200))
check=0
y=375-18.75
x=625-18
x_1=7
y_1=7
dis=47
clock=pygame.time.Clock()
time_a=5
turn_dol=1

def make_pan(list_a):
    for a in range(len(list_a)):
        for b in range(15):
            if list_a[a][b]>0 and list_a[a][b]==1:
                screen.blit(stone_b,(625-18+(b-7)*47-250,375-18.75+(a-7)*47))
            if list_a[a][b]>0 and list_a[a][b]==2:
                screen.blit(stone_w,(625-18+(b-7)*47-250,375-18.75+(a-7)*47))
def last_stone(list_a):
    screen.blit(last_sign1,(625-18+(list_a[0]-7)*47-250,375-18.75+(list_a[1]-7)*47))

end_value=True

while end_value:
    game_end=False
    game_end1=False
    turn_dol1=1
    ai_lose=False
    finish=False
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
    pan=[
     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
    screen.blit(my_img,(window_num,0))
    screen.blit(select,(x,y))
    pygame.display.update()
    while not finish:
        screen.fill(0)
        #pygame.draw.rect(screen, (219,188,104), my_rect1)
        #pygame.draw.rect(screen, (219,188,104), your_rect1)
        screen.blit(my_img,(window_num,0))
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                end_value=False
                finish=True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    if y-dis > 0:
                        y -= dis
                        x_1 -= 1
                elif event.key == pygame.K_DOWN:
                    if y+dis < window_high-dis:
                        y += dis
                        x_1 += 1
                elif event.key == pygame.K_RIGHT:
                    if x+dis < window_high+window_num-dis:
                        x += dis
                        y_1 += 1
                elif event.key == pygame.K_LEFT:
                    if x-dis >window_num:
                        x -= dis
                        y_1 -= 1
                # elif event.key == pygame.K_RETURN and game_end ==False:
                #     if pan[x_1][y_1]==0:
                #         save_samsam,_=samsam_all_non(pan,turn_dol)
                #         pan[x_1][y_1]=turn_dol
                #         save_list=samsam_all_non(pan,turn_dol)[1]
                #         if sasa_all(pan,turn_dol)[0]:
                #             pan[x_1][y_1]=0
                #         elif save_samsam+1 < samsam_all_non(pan,turn_dol)[0]:
                #             pan[x_1][y_1]=0
                #         elif jangmok_all(pan) and pan[x_1][y_1]==1:
                #             pan[x_1][y_1]=0
                #         else:
                            
                #             game_end,_ = panjung_all(pan)
                #             if game_end==True:
                #                 ai_lose=True
                #             screen.blit(my_img,(window_num,0))
                #             screen.blit(select,(x,y))
                #             make_pan(pan)
                #             pygame.display.update()
                            
                #             _,test =ai_first(pan)
                #             ask=ask_end(pan)
                #             #print(ask)
                #             if not ask==[15,15]:
                #                 pan[ask[0]][ask[1]]=2
                #                 if ai_lose==False and panjung_all(pan)[0]:
                #                     game_end=True
                #                     ai_lose==False
                #                 last_stone_xy=ask[0],ask[1]
                #             elif len(test) > 0:
                #                 pan[test[0][0]][test[0][1]]=2
                #                 if ai_lose==False and panjung_all(pan)[0]:
                #                     game_end=True
                #                     ai_lose==False
                #                 last_stone_xy=test[0][0],test[0][1]
                #             else:
                #                 print("생각중..")
                #                 board1=np.array(ai_defence(pan,2))
                #                 board2=np.array(ai_attack(pan,2))
                #                 board4=np.array(ai_sa(pan,2))
                #                 board3=board1+board2+board4
                #                 print(board3)
                #                 save=0
                #                 list_save_xy=[]
                #                 for a in range(15):
                #                     for b in range(15):
                #                         if board3[a][b] >save:
                #                             save=int(board3[a][b])
                #                             list_save_xy=[a,b]
                #                 pan[list_save_xy[0]][list_save_xy[1]] = 2
                #                 last_stone_xy=list_save_xy[0],list_save_xy[1]
                #                 if ai_lose==False and panjung_all(pan)[0]:
                #                     game_end=True
                #                     ai_lose==False
                elif event.key == pygame.K_RETURN and game_end ==True:
                        finish=True
                elif event.key == pygame.K_F5:
                    pan=[[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
                elif event.key == pygame.K_F1:
                    pan[x_1][y_1]=0
                elif event.key == pygame.K_F2:
                    pan[x_1][y_1]=2
                elif event.key == pygame.K_F3:
                    pan[x_1][y_1]=1
                elif event.key == pygame.K_F4:
                    print(x_1,y_1)
                elif event.key == pygame.K_F10:
                    end_value=False
                    finish=True
                
                screen.blit(my_img,(window_num,0))
                screen.blit(select,(x,y))
                make_pan(pan)
                last_stone([last_stone_xy[1],last_stone_xy[0]])
                
                # if game_end: 
                #     if ai_lose==False and not game_end1: # 백 승
                #         screen.blit(win_white,(0,250))
                #         pygame.display.update()
                #         game_end1=True
                #     elif ai_lose==True and not game_end1: # 흑 승
                #         screen.blit(win_black,(0,250))
                #         pygame.display.update()
                #         game_end1=True
                pygame.display.update()
