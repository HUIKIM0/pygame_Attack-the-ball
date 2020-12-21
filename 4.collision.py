import pygame
import os   # 파일/폴더 등의 경로를 쉽게 가져오기 위해 사용

pygame.init()

# ●화면 크기 설정
screen_width = 640
screen_height = 480
screen = pygame.display.set_mode((screen_width,screen_height)) # 창만들기

pygame.display.set_caption("!공을 맞춰라!") # 게임 타이틀

# FPS
clock = pygame.time.Clock()


# ★1. 사용자 게임 초기화 (배경 화면, 게임 이미지, 좌표, 속도, 폰트 등)
# os.path.dirname(__file__)
# os.path.join(기존경로,새로운폴더이름) => 합쳐서 하위경로 만드는거
current_path = os.path.dirname(__file__)  # 현재 파일의 위치 반환(코딩 하고있는 이 파일 위치)
image_path = os.path.join(current_path, "images")


# ●배경 만들기. 배경 이미지 로드
background = pygame.image.load(os.path.join(image_path,"background.png"))


# ●스테이지 만들기(캐릭터가 서 있는 땅 같은 공간)
# ★스테이지의 사이즈 정보를 알아내야 함
# 스테이지의 높이를 계산해서 그 높이에 맞게 공을 튕긴다던지, 캐릭터를 위치시킨다던지..
stage = pygame.image.load(os.path.join(image_path,"stage.png"))

stage_size = stage.get_rect().size # 스테이지 이미지의 사이즈 정보
stage_height = stage_size[1] # stage_size[1]은 height, 0은 width. 스테이지의 위에 캐릭터를 두기위해 높이 필요


# ●캐릭터 만들기
character = pygame.image.load(os.path.join(image_path,"character.png"))

character_size = character.get_rect().size # ★캐릭터 이미지의 사이즈 정보

character_width = character_size[0]
character_height = character_size[1]   
character_x_pos = (screen_width/2) - (character_width/2)
character_y_pos = screen_height - character_height - stage_height # 스테이지도 빼야 스테이지 위에 캐릭터가 놓임


# 캐릭터 이동 방향 (가로로만 움직임). keyevent를 위함!!
character_go_x = 0

# 캐릭터의 이동 속도
character_speed = 5


# 무기 만들기
weapon = pygame.image.load(os.path.join(image_path, "weapon.png"))

weapon_size = weapon.get_rect().size  # ★무기의 이미지 사이즈정보
weapon_width = weapon_size[0]

# ●무기는 한 번에 여러 발 발사 가능(list로 처리)
weapons = []

# 무기의 이동 속도
weapon_speed = 10


# ●공 만들기 (4개 크기에 대해 따로 처리.list)
ball_images = [
    pygame.image.load(os.path.join(image_path,"balloon1.png")), # -18(공이 제일 큼)
    pygame.image.load(os.path.join(image_path,"balloon2.png")), # -15
    pygame.image.load(os.path.join(image_path,"balloon3.png")), # -12
    pygame.image.load(os.path.join(image_path,"balloon4.png"))  # -9
]


# 공 크기에 따른 최초 스피드
# 공이 튀겨졌을때 y값이 -가 되어야 위로 올라간다
ball_speed_y = [-18, -15, -12, -9]  # index 0,1,2,3에 해당

# 공 배열. 공도 무기처럼 자꾸 늘어남! 쪼개지기 때문에.. 그래서 list로 관리
balls = []

# dictionary{}
# 가장 큰 공(최초 발생 공) list에 추가
balls.append({
    "pos_x":50,  # 공의 x좌표
    "pos_y":50,  # 공의 y좌표
    "img_idx":0, # 공의 이미지 인덱스(처음에는 가장 큰 공 balloon1)
    "go_x":3, # x축 이동 방향. 3이면 오른쪽 -3이면 왼쪽
    "go_y": -6,  # y축 이동방향
    "init_spd_y": ball_speed_y[0] # y 최초속도
})


# 사라질 무기, 공 정보 저장 변수(부딪히면 사라지게 처리해야 하므로)
weapon_to_remove = -1
ball_to_remove = -1


running = True  # 게임이 진행중인가?
while running:
    dt = clock.tick(30)  # 게임화면의 초당 프레임 수를 설정

    # ★2. 이벤트 처리 (키보드,마우스 등)
    for event in pygame.event.get():   # 사용자로 인한 동작이 들어오는지 체크
        if event.type == pygame.QUIT:  # 만약 사용자가 창을 닫으면
            running = False  # 게임 진행중 X
        
        # ●키보드에 입력 들어옴
        if event.type == pygame.KEYDOWN:  
            if event.key == pygame.K_LEFT:
                character_go_x -= character_speed
            elif event.key == pygame.K_RIGHT:
                character_go_x += character_speed

            elif event.key == pygame.K_SPACE: # 무기 발사 
                weapon_x_pos = character_x_pos +  (character_width/2) - (weapon_width/2) # 무기는 캐릭터의 중앙에서 나옴
                weapon_y_pos = character_y_pos  # 캐릭터의 바로 위에서 발사되게
                weapons.append([weapon_x_pos, weapon_y_pos])  # list의 형태로 weapons list에 x좌표 y좌표 추가
                                                                 # 무기를 여러번 쏘면 쏠수록 이런 값들이 계속 추가됨
                                                                
        # ●사용자가 손을 땜
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
               character_go_x = 0

                
    
    # ★3. 게임 캐릭터 위치 정의
    character_x_pos += character_go_x  # x위치에 키보드 입력으로 인해 변한 값을 더해줌(캐릭터 위치 지정)
    
    # 캐릭터가 화면에 벗어나지 않게 처리
    if character_x_pos < 0:
        character_x_pos = 0
    elif character_x_pos > screen_width - character_width:   # 캐릭터위치 > 607. 화면을 벗어났음
        character_x_pos = screen_width - character_width     


    # 공격시 무기 위치 위로 올라가게 변경. 한줄 for문 [ i for i in 변수명]
    # 0번째 인덱스의 값(x좌표), 1번째 인덱스의 값(y좌표) - weapon_speed만큼 빼기
    # 위로 올라갈수록 0에 가까워지니까, x는 그대로 두고 y는 스피드만큼 빼야함
    weapons = [ [up[0], up[1] - weapon_speed] for up in weapons]  # ★

    # 천장에 닿은 무기 없애기
    # y좌표가 0보다 크다 -> 천장에 닿지 않았다
    # 천장에 닿지 않은 것만 리스트로 만들어서 다시 저장
    weapons = [ [up[0], up[1]] for up in weapons if up[1] > 0]

    # ● 공 위치 정의
    # enumerate -> 인덱스와 그에 해당하는 값을 보여줌
    for ball_idx, ball_val in enumerate(balls):
        ball_pos_x = ball_val["pos_x"] # balls = []에 있는 x값(50)
        ball_pos_y = ball_val["pos_y"]  # 50
        ball_img_idx = ball_val["img_idx"]  # 0

        ball_size = ball_images[ball_img_idx].get_rect().size  # ball_images=[] ★공 이미지 사이즈 정보
        ball_width = ball_size[0]
        ball_height = ball_size[1]

        # ★
        # 공이 튕겨지다가 가로벽에 닿으면 안 벗어나고 반대쪽으로 튕겨나가는 효과를 주기 위함
        if ball_pos_x < 0 or ball_pos_x > screen_width - ball_width:
            ball_val["go_x"] = ball_val["go_x"] * -1  # 3이였으면 -3으로(왼쪽). -3이였으면 3으로(오른쪽)

        # 세로 위치. 스테이지에 닿으면 튕김처리 -> 공 속도 줄여나감(통!!통..통....느낌위해)
        if ball_pos_y >= screen_height - stage_height - ball_height:
            ball_val["go_y"] = ball_val["init_spd_y"]  # 스테이지에 닿으면 공이 튕겨지는 높이는 최초속도(init_spd_y)값
        else:  # 스테이지에 튕겨지고 올라간 후의 올라가고 내려가는 처리
            ball_val["go_y"] +=0.5   # go_y의 초기값은 -6. -5.5, -5 .. 위로 가다가 0이되면 +가 되서 아래로 떨어짐 

        ball_val["pos_x"] += ball_val["go_x"]
        ball_val["pos_y"] += ball_val["go_y"]


    # ★4. 충돌 처리

    # 캐릭터 rect 정보 업데이트
    character_rect = character.get_rect()
    character_rect.left = character_x_pos
    character_rect.top = character_y_pos

    # 공
    for ball_idx, ball_val in enumerate(balls):
        ball_pos_x = ball_val["pos_x"]
        ball_pos_y = ball_val["pos_y"]
        ball_img_idx = ball_val["img_idx"]

        # 공 rect 정보 업데이트. 리스트 ball_images
        ball_rect = ball_images[ball_img_idx].get_rect()
        ball_rect.left = ball_pos_x
        ball_rect.top = ball_pos_y

        # 공과 캐릭터 충돌 체크(충돌 시 게임종료)
        if character_rect.colliderect(ball_rect):
            running = False
            break

        # 공과 무기들 충돌 처리(충돌 시 사라져야함)
        for weapon_idx, weapon_val in enumerate(weapons):
            weapon_pos_x = weapon_val[0]
            weapon_pos_y = weapon_val[1]

            # 무기 rect 정보 업데이트
            weapon_rect = weapon.get_rect()
            weapon_rect.left = weapon_pos_x
            weapon_rect.top = weapon_pos_y

            # 충돌 체크
            if weapon_rect.colliderect(ball_rect):
                # 해당 인덱스의 무기 없애기 위해 값 설정
                weapon_to_remove = weapon_idx  
                # 해당 인덱스의 공 없애기 위해 값 설정
                ball_to_remove = ball_idx 
                
                # 가장 작은 공이 아니였다면, 그 다음 공으로 나눠주기
                # 현재 인덱스의 공 ball_img_idx
                if ball_img_idx < 3:

                    # 현재 공 크기(가로세로) 정보를 가져옴. 공 rect정보 업데이트 된것의 사이즈
                    ball_width = ball_rect.size[0]  
                    ball_height = ball_rect.size[1]
                    
                    # 나눠진 공 정보.
                    next_ball_rect = ball_images[ball_img_idx +1].get_rect()
                    next_ball_width = next_ball_rect.size[0]
                    next_ball_height = next_ball_rect.size[1]

                    # 왼쪽으로 튕겨나가는 작은 공
                    balls.append({
                        "pos_x": ball_pos_x + (ball_width/2) - (next_ball_width/2),
                        "pos_y": ball_pos_y + (ball_height/2) - (next_ball_height/2),
                        "img_idx": ball_img_idx + 1, # 지금 크기보다 작아진 크기의 img idx를 참조
                        "go_x": -3, # x축 이동 방향. 3이면 오른쪽 -3이면 왼쪽
                        "go_y": -6,  # y축 이동방향
                        "init_spd_y": ball_speed_y[ball_img_idx + 1] # 공 사이즈에 따른 최초 스피드를 다음 idx로 넘김
                    })

                    # 오른쪽으로 튕겨나가는 작은 공
                    balls.append({
                        "pos_x": ball_pos_x + (ball_width/2) - (next_ball_width/2),
                        "pos_y": ball_pos_y + (ball_height/2) - (next_ball_height/2),
                        "img_idx": ball_img_idx + 1,
                        "go_x": 3, # x축 이동 방향. 3이면 오른쪽 -3이면 왼쪽
                        "go_y": -6,  # y축 이동방향
                        "init_spd_y": ball_speed_y[ball_img_idx + 1]
                    })
                break

    # ★충돌된 공 or 무기 없애기★
    # ●ball_to_remove와 weapon_to_remove의 초기값은 -1임
    # ●인덱스는 0부터 시작..ball_to_remove과 weapon_to_remove의 값이 -1보다 크다?
    # ●충돌 체크 작업을 마쳤다는 뜻! 제거대상
    if ball_to_remove > -1:  
        del balls[ball_to_remove]  # 공 list의 해당 인덱스 제거 
        ball_to_remove = -1

    if weapon_to_remove > -1:
        del weapons[weapon_to_remove]  # 무기 list의 해당 인덱스 제거
        weapon_to_remove = -1



    # ★5. 화면에 그리기(이미지,(좌표,좌표))
    screen.blit(background,(0,0))

    # list weapons에 담긴 개수 만큼 weapon.png를 그려준다
    for weapon_x_pos,weapon_y_pos in weapons:
        screen.blit(weapon,(weapon_x_pos,weapon_y_pos))
   
    
    for idx, val in enumerate(balls):
        ball_pos_x = val["pos_x"]
        ball_pos_y = val["pos_y"]
        ball_img_idx = val["img_idx"]

        screen.blit(ball_images[ball_img_idx], (ball_pos_x, ball_pos_y))

    screen.blit(stage,(0,(screen_height-stage_height))) # 0,430
    screen.blit(character,(character_x_pos,character_y_pos))
    

    pygame.display.update()



pygame.time.delay(1500)
pygame.quit()