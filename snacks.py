from pygame.locals import *
import pygame
from random import choice
import time
import sys
import copy

gridSize = (12, 17)		# 宽 * 高 
MinHeight = 2
GameStatus = list(enumerate(["Ready", "Gaming", "GameOver"]))
ColorList = [(250, 0, 0), (0, 250, 0), (0, 0, 250), (250, 250, 0), (0, 250, 250), (250, 0, 250), (250, 100, 0)]
IDList = list(range(7))
'''
1.		 □□□□   □      □      □    □□     □□       □□
				□□□   □□□   □□□     □□    □□      □□       
'''


def stuff_list(stuff_id):
    if stuff_id == 0:
        ptr = [[0, 0], [0, 1], [0, 2], [0, 3]]
    elif stuff_id == 1:
        ptr = [[0, 0], [0, 1], [0, 2], [1, 0]]
    elif stuff_id == 2:
        ptr = [[0, 1], [0, 0], [0, 2], [1, 1]]
    elif stuff_id == 3:
        ptr = [[0, 2], [0, 1], [0, 0], [1, 2]]
    elif stuff_id == 4:
        ptr = [[0, 0], [0, 1], [1, 0], [1, 1]]
    elif stuff_id == 5:
        ptr = [[0, 1], [0, 0], [1, 1], [1, 2]]
    else:
        ptr = [[0, 1], [0, 2], [1, 0], [1, 1]]
    return ptr


class Stuff:
    def __init__(self, stuff_id):
        self.space = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],		# 记录已固定的方块
                      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
        self.id = stuff_id
        self.ptr = []
        self.new_stuff(stuff_id)

    def new_stuff(self, stuff_id):
        self.id = stuff_id
        if self.id == 0:
            self.ptr = [[0, 4], [0, 3], [0, 5], [0, 6]]
        elif self.id == 1:
            self.ptr = [[0, 4], [0, 3], [0, 5], [1, 3]]
        elif self.id == 2:
            self.ptr = [[0, 4], [0, 3], [0, 5], [1, 4]]
        elif self.id == 3:
            self.ptr = [[0, 4], [0, 5], [0, 3], [1, 5]]
        elif self.id == 4:
            self.ptr = [[0, 4], [0, 3], [1, 3], [1, 4]]
        elif self.id == 5:
            self.ptr = [[0, 4], [0, 3], [1, 4], [1, 5]]
        else:
            self.ptr = [[0, 4], [0, 5], [1, 3], [1, 4]]

    def crash(self):
        """
        return:     0: no crash
                    1: down crash
                    2: up crash
                    3: left crash
                    4: right crash
                    5: note crash
        """
        for i in range(4):
            if self.ptr[i][0] > gridSize[1]-1:
                return 1
            elif self.ptr[i][0] < 0:
                return 2
            elif self.ptr[i][1] > gridSize[0]-1:
                return 3
            elif self.ptr[i][1] < 0:
                return 4
            elif self.space[self.ptr[i][0]][self.ptr[i][1]] != 0:
                return 5
        return 0

    def fix_stuff(self):		# 固定
        for ptr in self.ptr:
            self.space[ptr[0]][ptr[1]] = self.id + 1
        del_list = []
        for i in range(len(self.space)):	# 判断是否满行
            flag = True
            for g in self.space[i]:
                if g == 0:
                    flag = False
                    break
            if flag:
                del_list.append(i)
        for i in del_list:
            del self.space[i]
            self.space.insert(0, [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
        # return len(del_list)		此处可加一个返回，用于方便计算分数

    def down(self):
        temp_ptr = copy.deepcopy(self.ptr)
        for i in range(4):
            self.ptr[i][0] += 1
        crash_result = self.crash()
        if crash_result != 0:
            self.ptr = copy.deepcopy(temp_ptr)
            return False
        return True

    def up(self):
        temp_ptr = copy.deepcopy(self.ptr)
        for i in range(4):
            self.ptr[i][0] -= 1
        crash_result = self.crash()
        if crash_result != 0:
            self.ptr = copy.deepcopy(temp_ptr)
            return False
        return True

    def left(self):
        temp_ptr = copy.deepcopy(self.ptr)
        for i in range(4):
            self.ptr[i][1] -= 1
        crash_result = self.crash()
        if crash_result != 0:
            self.ptr = copy.deepcopy(temp_ptr)
            return False
        return True

    def right(self):
        temp_ptr = copy.deepcopy(self.ptr)
        for i in range(4):
            self.ptr[i][1] += 1
        crash_result = self.crash()
        if crash_result != 0:
            self.ptr = copy.deepcopy(temp_ptr)
            return False
        return True

    def rotate(self):		# 旋转方块
        temp_ptr = copy.deepcopy(self.ptr)
        for i in range(1, 4):
            temp_y, temp_x = temp_ptr[0][0], temp_ptr[0][1]
            i_y, i_x = temp_ptr[i][0], temp_ptr[i][1]
            self.ptr[i] = [temp_ptr[0][0] - temp_ptr[i][1] + temp_ptr[0][1],		# 逆时针旋转
                           temp_ptr[0][1] + temp_ptr[i][0] - temp_ptr[0][0]]
            # self.ptr[i][0] = temp_ptr[0][0] + temp_ptr[i][1] - temp_ptr[0][1]
        crash_result = self.crash()
        if crash_result == 0:
            return True
        elif crash_result == 1:
            if self.up():
                return True
        elif crash_result == 2:
            if self.down():
                return True
        elif crash_result == 3:
            if self.left():
                return True
        elif crash_result == 4:
            if self.right():
                return True
        self.ptr = copy.deepcopy(temp_ptr)
        return False

    def over(self):		#游戏结束判断
        for i in range(1):
            for value in self.space[i]:
                if value != 0:
                    return True
        return False


def show_text(screen, pos, text, text_color, font_bold=False, font_size=60, font_italic=False, font_mediate=True):
    # 获取系统字体，并设置文字大小
    cur_font = pygame.font.SysFont("宋体", font_size)
    # 设置是否加粗属性
    cur_font.set_bold(font_bold)
    # 设置是否斜体属性
    cur_font.set_italic(font_italic)
    # 设置文字内容
    text_fmt = cur_font.render(text, 1, text_color)
    text_pos = text_fmt.get_rect()
    text_pos.midtop = pos
    # 绘制文字
    if font_mediate:
    # 判断是否居中
        screen.blit(text_fmt, text_pos)
    else:
        screen.blit(text_fmt, pos)


def main():
    pygame.init()
    ftpsClock = pygame.time.Clock()
    screen = pygame.display.set_mode((800, 800))
    pygame.display.set_caption("Tetris")
    GAME_STATUS = 0
    next_stuff = choice(IDList)
    curr_stuff = choice(IDList)
    stuff = Stuff(curr_stuff)
    next_ptr = stuff_list(next_stuff)
    gamingTime = time.time()
    while True:
        screen.fill((150, 150, 150))
        pygame.draw.rect(screen, (50, 50, 50), (50, 50, 500, 700))
        pygame.draw.rect(screen, (100, 100, 100), (60, 60, 480, 80))
        if GAME_STATUS == 0:	# Ready
            for event in pygame.event.get():	# 事件遍历
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == KEYDOWN:		# 按键按下
                    if event.key in [K_RETURN, K_KP_ENTER]:
                        GAME_STATUS = 1
            show_text(screen, (400, 400), "Press enter to start game", (250, 250, 0), font_size=80)
        elif GAME_STATUS == 1:		# gaming
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == KEYDOWN:
                    if event.key in [K_UP, K_w, K_SPACE]:
                        stuff.rotate()
                    if event.key in [K_LEFT, K_a]:
                        stuff.left()
                    if event.key in [K_RIGHT, K_d]:
                        stuff.right()
                    if event.key in [K_DOWN, K_s]:	# 这里因为只判断了KEYDOWN，所以无论你按多久，都只会触发一次
                        stuff.down()				# 如果想实现长按快速下落这个效果可以和KEYUP事件一起食用
            if time.time() - gamingTime > 0.5:
                gamingTime = time.time()
                if not stuff.down():
                    stuff.fix_stuff()
                    curr_stuff = next_stuff
                    next_stuff = choice(IDList)
                    stuff.new_stuff(curr_stuff)
                    next_ptr = stuff_list(next_stuff)
            for pos in next_ptr:
                pygame.draw.rect(screen, ColorList[next_stuff], (601 + 50 * pos[1], 101 + 50 * pos[0], 48, 48))
            for i in range(gridSize[1]):
                for j in range(gridSize[0]):
                    ID = stuff.space[i][j]
                    if ID != 0:
                        pygame.draw.rect(screen, ColorList[ID - 1], (61 + 40 * j, 61 + 40 * i, 38, 38))
            for pos in stuff.ptr:
                pygame.draw.rect(screen, ColorList[stuff.id], (61 + 40 * pos[1], 61 + 40 * pos[0], 38, 38))
            if stuff.over():
                GAME_STATUS = 2
        elif GAME_STATUS == 2:	# Game over
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == KEYDOWN:
                    if event.key in [K_RETURN, K_KP_ENTER]:
                        GAME_STATUS = 0
                        next_stuff = choice(IDList)
                        curr_stuff = choice(IDList)
                        stuff = Stuff(curr_stuff)
                        next_ptr = stuff_list(next_stuff)
            show_text(screen, (400, 350), "GameOver", (250, 250, 0), font_size=80)
            show_text(screen, (400, 450), "Press enter to start game", (250, 250, 0), font_size=80)
        pygame.display.flip()
        ftpsClock.tick(20)	# 每秒20帧


if __name__ == '__main__':
    main()

