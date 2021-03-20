# 좌표 주변 조사 코드
    # # ㅡ 가로로 이어진 돌 수
    # for x_l in range(x-1, x-5, -1):
    #     if (x_l == -1): break
    # for x_r in range(x+1, x+5, +1):
    #     if (x_r == size): break

    # # ㅣ 세로로 이어진 돌 수
    # for y_u in range(y-1, y-5, -1):
    #     if (y_u == -1): break
    # for y_d in range(y+1, y+5, +1):
    #     if (y_d == size): break

    # # \ 대각선으로 이어진 돌 수 
    # x_l = x
    # y_u = y ### x -> y
    # for i in range(4):
    #     if (x_l-1 == -1) or (y_u-1 == -1): break
    #     x_l -= 1
    #     y_u -= 1
        
    # x_r = x
    # y_d = y
    # for i in range(4):
    #     if (x_r+1 == size) or (y_d+1 == size): break
    #     x_r += 1
    #     y_d += 1
        

    # # / 대각선으로 이어진 돌 수
    # x_l = x
    # y_d = y
    # for i in range(4):
    #     if (x_l-1 == -1) or (y_d+1 == size): break
    #     x_l -= 1
    #     y_d += 1
        
    # x_r = x
    # y_u = y
    # for i in range(4):
    #     if (x_r+1 == size) or (y_u-1 == -1): break
    #     x_r += 1
    #     y_u -= 1