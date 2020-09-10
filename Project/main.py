import pygame
import time
import snake,one_to_50,hanoi
from pygame.locals import *

WHITE = (255, 255, 255)
BLACK = (0,0,0)
pad_width = 1040#1024 # 게임판의 크기설정
pad_heith  = 500#490
'''이미지 로드'''
main_btn = pygame.image.load("image\\mainlogo2.png")

'''폰트 설정'''
font = pygame.font.Font('BMJUA_ttf.ttf', 25)
select_font = pygame.font.Font('BMJUA_ttf.ttf',30)
mainfont = pygame.font.Font('BMJUA_ttf.ttf',110)
'''폰트 렌더'''
select_font_render = select_font.render("돌아가기", True, (255, 255, 255))
main_text1 = font.render("게임 시작", True, (255, 255, 255), (100, 100, 100))
main_text1_1 = font.render("게임 시작", True,(255,255,255))
main_text2 = font.render("종료 하기", True,(255,255,255),(100,100,100))
main_text2_1 = font.render("종료 하기", True,(255,255,255))
snake_text = font.render("뱀 게임",True,(255,255,255))
oneto_text = font.render("1 to 50", True,(255,255,255))
hanoi_text = font.render("하노이의 탑",True,(255,255,255))
log_text = mainfont.render("이상한 코딩의 파이썬",True,(255,255,255))
end_text = mainfont.render("게임 종료",True,(255,255,255))
try_text = select_font.render("다시 하시겠습니까? (Y/N)",True,(255,255,255))
'''rect 변수'''
end_rect = end_text.get_rect(center=(520,250))
try_rect = try_text.get_rect(center=(520,370))
'''기타 변수'''
end_state = 1



class Data_base():

    def __init__(self):
        self.snake_score = 0
        self.one_to_50_score = 0
        self.hanoi_score = 0
        self.load_data()
        self.last_score = 0


    def save_data(self):
        with open("Savefolder\\save.txt", "w") as f:
            f.write("%d,%d,%d"%(self.snake_score,self.one_to_50_score,self.hanoi_score))

    def load_data(self):
        try:
            with open("Savefolder\\save.txt","r") as f:
                self.read_data  = f.read()
                self.read_data =  self.read_data.split(",")
                self.snake_score = int(self.read_data[0])
                self.one_to_50_score = int(self.read_data[1])
                self.hanoi_score = int(self.read_data[2])
        except FileNotFoundError:
            with open("Savefolder\\save.txt","w") as f:
                f.write("0,0,0")
data_save = Data_base()

def main_display(): # 초기 로고타이틀 출력함수
    global gamepad, main_btn, clock ,main_btn_rect
    main_btn_rect = main_btn.get_rect()
    main_btn_rect.center = (int((pad_width) / 2), int((pad_heith) / 2))  # 해당좌표를 main_btn의 중심좌표로 지정한다
    i = 0
    while i<255:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                break
        i +=10
        main_btn.set_alpha(i)
        gamepad.blit(main_btn, main_btn_rect)
        clock.tick(30)
        pygame.display.update()
        time.sleep(0.1)
    runGame(1)



def runGame(state):
    global gamepad, clock, game_status,text , font ,texts,gamestart_t
    global mainfont, select_font_render
    global menu
    global savefile_o,savefile,alpha
    global background, main_btn
    game_status = state
    data_save.load_data()
  #game_status의 숫자를 기준으로 게임의 상태를 구분
    menu = 0
    sub_menu = 0
    while game_status == 1: # 초기메뉴화면

        gamepad.fill(BLACK)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
               pygame.quit()
               break
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    if menu < 1:
                        menu = menu + 1
                if event.key == pygame.K_UP:
                    if menu > 0:
                        menu = menu - 1
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_RETURN:
                    if menu == 0:
                        runGame(2)
                    elif menu == 1:
                        pygame.quit()
        if menu == 0:
            gamepad.blit(main_text1,(470,350))
            gamepad.blit(main_text2_1,(470,376))
        elif menu == 1:
            gamepad.blit(main_text1_1,(470,350))
            gamepad.blit(main_text2,(470,376))
        pygame.draw.rect(gamepad,(255,255,255),(40,40,960,420),3)
        gamepad.blit(log_text,(80,100))
        pygame.display.update()
        clock.tick(60)
    while game_status == 2: # 게임선택화면
        '''game_status 2일떄 쓰는 변수들'''
        _snake_score = font.render("최고기록 : %s점"%data_save.snake_score,True,(255,255,255))
        _snake_rect = _snake_score.get_rect(center=(200,310))
        _oneto_score = font.render("최고기록 : %s초"%data_save.one_to_50_score,True,(255,255,255))
        _oneto_rect = _oneto_score.get_rect(center=(500,310))
        _hanoi_score = font.render("최고기록 : %s초"%data_save.hanoi_score,True,(255,255,255))
        _hanoi_rect = _hanoi_score.get_rect(center=(800,310))
        _not_score = font.render("   기록 없음",True,(255,255,255))
        _not_rect = _not_score.get_rect(center=(200,310))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_UP:
                    if sub_menu == 3:
                        sub_menu = 1
                if event.key == pygame.K_RIGHT:
                    if sub_menu < 3:
                        sub_menu += 1
                if event.key == pygame.K_LEFT:
                    if sub_menu > 0:
                        sub_menu -= 1
                if event.key == pygame.K_RETURN:
                    if sub_menu == 0 :
                        snake.start_game()
                    elif sub_menu == 1:
                        one_to_50.initgame()
                    elif sub_menu == 2:
                        hanoi.initgame()
                    elif sub_menu == 3:
                        runGame(1)
                if event.key == pygame.K_DOWN:
                    sub_menu = 3
        gamepad.fill((0,0,0))
        if sub_menu == 0:
            pygame.draw.rect(gamepad, (50,155,155),(80,130,250,200), 3)
            pygame.draw.rect(gamepad,(255,255,255),(380,130,250,200),3)
            pygame.draw.rect(gamepad,(255,255,255),(680,130,250,200),3)
            pygame.draw.rect(gamepad,(255,255,255),(430,400,140,50),3)
            gamepad.blit(select_font_render,(450,410))
        elif sub_menu == 1:
            pygame.draw.rect(gamepad, (255, 255, 255), (80, 130, 250, 200), 3)
            pygame.draw.rect(gamepad, (50, 155, 155), (380, 130, 250, 200), 3)
            pygame.draw.rect(gamepad, (255, 255, 255), (680, 130, 250, 200), 3)
            pygame.draw.rect(gamepad, (255, 255, 255), (430, 400, 140, 50), 3)
            gamepad.blit(select_font_render, (450, 410))
        elif sub_menu == 2:
            pygame.draw.rect(gamepad, (255, 255, 255), (80, 130, 250, 200), 3)
            pygame.draw.rect(gamepad, (255, 255, 255), (380, 130, 250, 200), 3)
            pygame.draw.rect(gamepad, (50, 155, 155), (680, 130, 250, 200), 3)
            pygame.draw.rect(gamepad, (255, 255, 255), (430, 400, 140, 50), 3)
            gamepad.blit(select_font_render, (450, 410))
        elif sub_menu == 3:
            pygame.draw.rect(gamepad, (255, 255, 255), (80, 130, 250, 200), 3)
            pygame.draw.rect(gamepad, (255, 255, 255), (380, 130, 250, 200), 3)
            pygame.draw.rect(gamepad, (255, 255, 255), (680, 130, 250, 200), 3)
            pygame.draw.rect(gamepad, (50, 155, 155), (430, 400, 140, 50), 3)
            gamepad.blit(select_font_render, (450, 410))
        if data_save.snake_score:
            gamepad.blit(_snake_score,_snake_rect)
        else:
            gamepad.blit(_not_score,_snake_rect)
        if data_save.one_to_50_score:
            gamepad.blit(_oneto_score,_oneto_rect)
        else:
            gamepad.blit(_not_score,_oneto_rect)
        if data_save.hanoi_score:
            gamepad.blit(_hanoi_score,_hanoi_rect)
        else:
            gamepad.blit(_not_score,_hanoi_rect)
        gamepad.blit(snake_text,(170,140))
        gamepad.blit(oneto_text,(470,140))
        gamepad.blit(hanoi_text,(750,140))
        #print(data_save.snake_score,data_save.one_to_50_score,data_save.hanoi_score)
        pygame.display.update()
        # 140,300
    while game_status == 3:  # 게인선택화면2
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_y:
                    snake.start_game()
                elif event.key == pygame.K_n:
                    runGame(2)
        gamepad.fill((0,0,0))
        pygame.draw.rect(gamepad,(255,255,255),(40,40,960,420),3)
        gamepad.blit(end_text,end_rect)
        if end_state == 1:
            end_score = select_font.render("획득 점수: {}점 ".format(data_save.last_score),True,(255,255,255))
            end_score_rect = end_score.get_rect(center=(520,330))
            gamepad.blit(end_score,end_score_rect)
            gamepad.blit(try_text,try_rect)


        elif end_state == 2:
            end_score = select_font.render("소요 시간: {}초".format(data_save.one_to_50_score),True,(255,255,255))
            end_score_rect = end_score.get_rect(center=(520,330))
            gamepad.blit(end_score,end_score_rect)
            gamepad.blit(try_text, try_rect)

        elif end_state == 3:
            end_score = select_font.render("소요 시간: {}초".format(data_save.one_to_50_score),True,(255,255,255))
            end_score_rect = end_score.get_rect(center=(520,330))
            gamepad.blit(end_score,end_score_rect)
            gamepad.blit(try_text, try_rect)
        pygame.display.update()


    while game_status == 4: #스네이크 종료
        pass
    while game_status == 5: # 1to 50 종료
        pass
    while game_status == 6: # hanoi 종료
        pass

        gamepad.fill(BLACK)

        pygame.display.update()
        clock.tick(60)

def initGame(load_state): # 게임 초기설정 초기화
    global gamepad, clock,player2 ,font  ,text,texts
    global mainfont, select_font_render
    global game_status,crashed,menu
    global background, main_btn
    global t1,t2
    pygame.init()
    init_state = load_state
    gamepad = pygame.display.set_mode((pad_width,pad_heith))
    pygame.display.set_caption("뭘 봐")

    font = pygame.font.Font('BMJUA_ttf.ttf', 25)
    game_status = 0
    crashed = False
    menu = 0
    clock = pygame.time.Clock()
    # init_state=1
    if init_state == 0:
        main_display()
    if init_state != 0:
        runGame(3)

if __name__ == "__main__":
    initGame(0)