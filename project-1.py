import pygame # pygame 라이브러리 임포트
import random # random 라이브러리 임포트
from time import sleep

BLACK = (255,255,255)   # 게임 바탕화면 색상
RED = (255,0,0) # 글자 색상
pad_width = 480   # 게임의 가로크기
pad_height = 640  # 게임의 세로크기
fighter_width = 36
fighter_height = 38
enemy_width = 26
enmey_height = 20

# 배경화면 이미지를 출력할 수 있는 함수
def back(background):
    background_rect = background.get_rect()
    gamepad.blit(background, background_rect)
    
# 사과를 맞춘 개수 계산
def drawScore(count):
    global gamepad
    font = pygame.font.SysFont(None, 20)
    text = font.render('Enemy Kills:' + str(count), True, (255,255,255))
    gamepad.blit(text,(0,0))
 
# 사과가 바닥으로 떨어진 개수
def drawPassed(count):
    global gamepad
    font = pygame.font.SysFont(None, 20)
    text = font.render('Enemy Passed:' + str(count), True, RED)
    gamepad.blit(text, (360,0))
 
 
#사과가 활과 닿았을 때
def crash(count):
    global gamepad
    font1 = pygame.font.SysFont(None, 60) # Crashed
    font = pygame.font.SysFont(None, 40) # Score
    text1 = font1.render('Crashed!', True,(0,0,255))
    text = font.render('Your Score: ' + str(count), True,(0,0,255))
    textpos1 = text.get_rect() # score
    textpos1.center = (pad_width/2, pad_height/2 - 60)
    textpos = text.get_rect() # crashed
    textpos.center = (pad_width/2, pad_height/2)
    gamepad.blit(text,textpos) # score
    gamepad.blit(text1,textpos1) #crashed
    pygame.display.update() # 게임 화면 업데이트
    sleep(2) # 2초 정지
    runGame() # 게임 재실행
 
#게임 오버 함수
def gameover(count):
    global gamepad
    font1 = pygame.font.SysFont(None, 60) # over
    font = pygame.font.SysFont(None, 40) # score
    text1 = font1.render('GameOver!', True,(0,0,255))
    text = font.render('Your Score: ' + str(count), True,(0,0,255))
    textpos1 = text.get_rect() # score
    textpos1.center = (pad_width/2, pad_height/2 - 60)
    textpos = text.get_rect() # over
    textpos.center = (pad_width/2, pad_height/2)
    gamepad.blit(text,textpos) # score
    gamepad.blit(text1,textpos1) # over
    pygame.display.update() # 게임 화면 업데이트
    sleep(2)
    runGame() # 게임 재실행

#게임에 나타나는 객체들을 좌표상으로 표현하기 위한 함수
def drawObject(obj,x,y):
    global gamepad
    gamepad.blit(obj,(x,y))
 
#게임 실행 메인 함수
def runGame():
    # 전역 변수들 선언
    global gamepad, clock, fighter, apple, gold, blackapple, blueapple, rainbow, bullet, background


    rand = random.randrange(1,11)
    back(background) #바탕화면 표시
    gamepad.fill((255,255,255)) #게임화면을 검은색으로 채우고 화면을 업데이트함

    
    # 사과를 맞췄을 경우 True로 설정되는 플래그
    isShot = False
    shotcount = 0
    enemypassed = 0
 
    # 무기 좌표를 위한 리스트 자료
    bullet_xy = []
 
    # 활 초기 위치 (x,y)
    x = pad_width * 0.45
    y = pad_height * 0.9
    x_change = 0
 
    # 사과 초기 위치
    enemy_x = random.randrange(0,430 - enemy_width)
    enemy_y = 0
    enemy_speed = 3


            
    ongame = False
    while not ongame:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: #마우스로 창을 닫는 이벤트
                doneFlag = True
                
             # 해당 방향키를 누르면 5만큼 이동
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x_change -= 5
                
                elif  event.key == pygame.K_RIGHT:
                    x_change += 5
 
                #스페이스바를 누르면 무기 발사
                elif  event.key == pygame.K_SPACE:
                    if len(bullet_xy) < 3:
                        bullet_x = x + fighter_width/2
                        bullet_y = y - fighter_height
                        bullet_xy.append([bullet_x, bullet_y])
 
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    x_change = 0
                    
        back(background)
         
        # 활 위치를 재조정
        x += x_change
        if x < 0:
            x = 0
        elif x > pad_width - fighter_width:
            x = pad_width - fighter_width
 
        # 활과 사과가 닿았을 때 crash() 함수를 부름
        if y < enemy_y + enmey_height:
            if(enemy_x > x and enemy_x < x + fighter_width) or\
                (enemy_x + enemy_width > x and enemy_x + enemy_width < x + fighter_width):
                crash(shotcount) #shotcount = score를 출력하기 위해서 shotcount를 넣음

        drawObject(fighter,x,y) # 활을 게임 화면의 (x,y) 좌표에 표시
         
        # 활을 쏘는 부분
        if len(bullet_xy) != 0:
            for i, bxy in enumerate(bullet_xy): # 활요소에대해 반복함
                bxy[1] -= 10 # 활의 y좌표를 -10함 (위로 이동)
                bullet_xy[i][1] = bxy[1]
 
                #사과를 맞췄을 경우
                if bxy[1] < enemy_y:
                    if bxy[0] > enemy_x and bxy[0] < enemy_x + enemy_width:
                        bullet_xy.remove(bxy)
                        isShot = True
                        shotcount += 1
 
                if bxy[1] <= 0: # 활이 화면 밖으로 나가는 경우
                    try:
                        bullet_xy.remove(bxy)  # 활을 화면에서 지운다
                    except:
                        pass
 
        if len(bullet_xy) != 0:
            for bx,by in bullet_xy:
                drawObject(bullet,bx,by)
 
 
        drawScore(shotcount) # 상단에 현재 점수를 출력하는 함수
 
        # 사과를 떨어지게 함
        enemy_y += enemy_speed
 
        if enemy_y > pad_height:
            enemy_y = 0
            enemy_x = random.randrange(0, 430 - enemy_width)
            enemypassed += 1
            # 독사과를 땅에 떨어지게 하는 경우는 enemypassed가 증가하지 않도록
            if rand == 2:
                enemypassed += -1
                if enemypassed < 0:
                    enemypassed = 0
                rand = random.randrange(1,11)    
            if rand == 5:
                enemypassed += -1
                if enemypassed < 0:
                    enemypassed = 0
                rand = random.randrange(1,11)
 
        if enemypassed == 3:
            gameover(shotcount)
 
        drawPassed(enemypassed) # 사과를 몇 개 떨어뜨렸는지 출력하는 함수
 
        #사과가 맞았는지 체크하고 맞았으면 스피드를 높이면서 난이도 올리기
        if isShot:
            enemy_speed += 0.3
            if enemy_speed >= 10:
                enemy_speed = 10 # 10 이상이면 너무 빠르기 때문에 최대 속도를 10으로
 
            enemy_x = random.randrange(0, pad_width-enemy_width)
            enemy_y = 0
            if rand == 1:
                shotcount += 49 # 황금사과일 경우 보너스 점수를 얻음
            if rand == 2:
                shotcount += -1
                gameover(shotcount) # 독사과를 맞출 경우 게임 오버 함수 표시
            if rand == 3:
                shotcount += 1 # 파란사과는 2점
            if rand == 4:
                shotcount += 9 # 무지개 사과는 10점
            if rand == 5:
                shotcount += -1
                gameover(shotcount) # 독사과
            if rand == 6:
                shotcount += 1
            isShot = False
            
            rand = random.randrange(1,11) # 다양한 사과를 화면에 표시하기 위해 넣은 변수
        
        if rand == 1:
            drawObject(gold, enemy_x, enemy_y) # 보너스 50점을 얻을 수 있는 황금사과
        elif rand == 2:
            drawObject(blackapple, enemy_x, enemy_y) # 독사과를 맞추면 게임이 종료됨
        elif rand == 3:
            drawObject(blueapple,enemy_x,enemy_y) # 2점 사과
        elif rand == 4:
            drawObject(rainbow,enemy_x,enemy_y) # 10점을 얻을 수 있는 무지개 사과
        elif rand == 5:
            drawObject(blackapple,enemy_x,enemy_y)
        elif rand == 6:
            drawObject(blueapple,enemy_x,enemy_y)
        elif rand == 7:
            drawObject(apple,enemy_x,enemy_y)
        elif rand == 8:
            drawObject(apple,enemy_x,enemy_y)
        elif rand == 9:
            drawObject(apple,enemy_x,enemy_y)
        elif rand == 10:
            drawObject(apple,enemy_x,enemy_y)
            

        pygame.display.update() #게임화면을 다시그림
        clock.tick(60) #게임화면 초당 프레임수를 60으로 설정
 
    pygame.quit() # 파이게임 종료
 
#게임 초기화 함수
def initGame():
    global gamepad,clock,fighter,apple, gold, blackapple, blueapple, rainbow, bullet, background #게임이 진행될 게임 화면, 게임의 초당 프레임(FPS), 비행기 변수 선언, 적 선언
 
    pygame.init() # 파이게임 초기화
    gamepad = pygame.display.set_mode((pad_width, pad_height)) #게임화면의 가로세로크기를 설정
    pygame.display.set_caption('Project Game') #게임화면의 제목
    background = pygame.image.load('sky.png') # 배경화면 이미지
    fighter = pygame.image.load('arrow.png') # 활 이미지
    apple = pygame.image.load('apple.png') # 사과 이미지
    gold = pygame.image.load('goldapple.png') # 황금사과 이미지
    blackapple = pygame.image.load('blackapple.png') # 독사과 이미지
    blueapple = pygame.image.load('blueapple.png') # 청사과 이미지
    rainbow = pygame.image.load('rainbow.png') # 무지개사과 이미지
    bullet = pygame.image.load('bow.png') # 화살 이미지
    clock = pygame.time.Clock() #초당 프레임수를 설정할 수 있는 Clock객체 생성

    
initGame()
runGame() # 게임 실행
