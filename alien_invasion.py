import sys
import pygame

def run_game():
    
    pygame.init()
    #设置屏幕大小
    screen = pygame.display.set_mode((1200,800))
    #设置标题
    pygame.display.set_caption("外星人大战")
    bg_color = (230,230,230)


    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
        
        #设置背景色
        screen.fill(bg_color)
        #刷新
        pygame.display.flip()

run_game()
        