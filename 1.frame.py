import pygame
import os   # 파일/폴더 등의 경로를 쉽게 가져오기 위해 사용

pygame.init()

# 화면 크기 설정
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


# 배경 만들기. 배경 이미지 로드
background = pygame.image.load(os.path.join(image_path,"background.png"))


# 스테이지 만들기(캐릭터가 서 있는 땅 같은 공간)
# 스테이지의 사이즈 정보를 알아내야 함
# 스테이지의 높이를 계산해서 그 높이에 맞게 공을 튕긴다던지, 캐릭터를 위치시킨다던지..
stage = pygame.image.load(os.path.join(image_path,"stage.png"))

stage_size = stage.get_rect().size # 스테이지의 사이즈 정보
stage_height = stage_size[1] # stage_size[1]은 width, 0은 height. 스테이지의 위에 캐릭터를 두기위해 높이 필요


# 캐릭터 만들기
character = pygame.image.load(os.path.join(image_path,"character.png"))




