import pygame
import os   # 파일/폴더 등의 경로를 쉽게 가져오기 위해 사용

pygame.init()

# 화면 크기 설정
screen_width = 640
screen_height = 480
screen = pygame.display.set_mode((screen_width,screen_height)) # 창만들기

pygame.display.set_caption("!공을 맞춰라!") # 게임 타이틀

