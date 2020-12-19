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
# 스테이지의 사이즈 정보를 알아내야 함
# 스테이지의 높이를 계산해서 그 높이에 맞게 공을 튕긴다던지, 캐릭터를 위치시킨다던지..
stage = pygame.image.load(os.path.join(image_path,"stage.png"))

stage_size = stage.get_rect().size # 스테이지의 사이즈 정보
stage_height = stage_size[1] # stage_size[1]은 height, 0은 width. 스테이지의 위에 캐릭터를 두기위해 높이 필요


# ●캐릭터 만들기
character = pygame.image.load(os.path.join(image_path,"character.png"))

character_size = character.get_rect().size # 캐릭터의 사이즈 정보

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

weapon_size = weapon.get_rect().size
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
    "to_x":3, # x축 이동 방향. 3이면 오른쪽 -3이면 왼쪽
    "to_y": -6,  # y축 이동방향
    "init_spd_y": ball_speed_y[0] # y 최초속도
})


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
    # 0번째 인덱스의 값, 1번째 인덱스의 값 에서 weapon_speed만큼 빼기
    # 위로 올라갈수록 0에 가까워지니까, x는 그대로 두고 y는 스피드만큼 빼야함
    weapons = [ [up[0], up[1] - weapon_speed] for up in weapons]  # ★

    # ★4. 충돌 처리

    # ★5. 화면에 그리기
    screen.blit(background,(0,0))

    # list weapons에 담긴 개수 만큼 weapon.png를 그려준다
    for weapon_x_pos,weapon_y_pos in weapons:
        screen.blit(weapon,(weapon_x_pos,weapon_y_pos))

    screen.blit(stage,(0,(screen_height-stage_height))) # 0,430
    screen.blit(character,(character_x_pos,character_y_pos))


    pygame.display.update()



            
pygame.time.delay(1500)
pygame.quit()