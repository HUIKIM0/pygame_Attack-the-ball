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


# 1. 사용자 게임 초기화 (배경 화면, 게임 이미지, 좌표, 속도, 폰트 등)
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

# 캐릭터 이동 방향 (가로로만 움직임)
character_to_x = 0

# 캐릭터의 이동 속도
character_speed = 5


# ●무기는 한 번에 여러 발 발사 가능(list로 처리)
weapons = []

# 무기의 이동 속도
weapons_speed = 10


# ●공 만들기 (4개 크기에 대해 따로 처리.list)
ball_images = [
    pygame.image.load(os.path.join(image_path,"balloon1.png")),
    pygame.image.load(os.path.join(image_path,"balloon2.png")),
    pygame.image.load(os.path.join(image_path,"balloon3.png")),
    pygame.image.load(os.path.join(image_path,"balloon4.png"))
]


running = True  # 게임이 진행중인가?
while running:
    dt = clock.tick(30)  # 게임화면의 초당 프레임 수를 설정

    # 2. 이벤트 처리 (키보드,마우스 등)
    for event in pygame.event.get():   # 사용자로 인한 동작이 들어오는지 체크
        if event.type == pygame.QUIT:  # 만약 사용자가 창을 닫으면
            running = False  # 게임 진행중 X


    
    # 3. 게임 캐릭터 위치 정의

    # 4. 충돌 처리

    # 5. 화면에 그리기
    screen.blit(background,(0,0))
    screen.blit(stage,(0,(screen_height-stage_height))) # 0,430
    screen.blit(character,(character_x_pos,character_y_pos))

    pygame.display.update()



pygame.time.delay(1500)
pygame.quit()