# 导入pygame模块，并初始化
import pygame
pygame.init()

# 创建一个窗口对象，设置大小和标题
window = pygame.display.set_mode((800, 600))
pygame.display.set_caption("时钟和频谱")

# 定义一些常量和变量
BLACK = (0, 0, 0) # 黑色
WHITE = (255, 255, 255) # 白色
RED = (255, 0, 0) # 红色
GREEN = (0, 255, 0) # 绿色
BLUE = (0, 0, 255) # 蓝色
YELLOW = (255, 255, 0) # 黄色
MAGENTA = (255, 0, 255) # 品红色
CYAN = (0, 255, 255) # 青色

font = pygame.font.SysFont("arial", 32) # 字体对象
clock = pygame.time.Clock() # 时钟对象
#soundcard = pygame.mixer.SoundCard() # 声卡对象

# 创建一个Sound对象，从一个文件或一个缓冲对象加载声音数据
sound = pygame.mixer.Sound("sound.wav") # 加载声音文件
sound.play(-1) # 播放声音，-1表示循环播放


# 定义一个函数，用于绘制一个圆形的指针式仿真时钟
def draw_clock(surface):
    # 获取当前的时间
    hour = pygame.time.get_hours()
    minute = pygame.time.get_minutes()
    second = pygame.time.get_seconds()

    # 计算指针的角度（以弧度为单位）
    hour_angle = (hour % 12 + minute / 60) * math.pi / 6 - math.pi / 2
    minute_angle = (minute + second / 60) * math.pi / 30 - math.pi / 2
    second_angle = second * math.pi / 30 - math.pi / 2

    # 计算表盘的中心和半径
    center_x = surface.get_width() // 2
    center_y = surface.get_height() // 2
    radius = min(center_x, center_y) - 50

    # 绘制一个白色的圆形表盘
    pygame.draw.circle(surface, WHITE, (center_x, center_y), radius)

    # 绘制刻度和数字
    for i in range(12):
        angle = i * math.pi / 6 - math.pi / 2 # 计算刻度的角度（以弧度为单位）
        x1 = center_x + radius * math.cos(angle) # 计算刻度的起点的横坐标
        y1 = center_y + radius * math.sin(angle) # 计算刻度的起点的纵坐标
        x2 = center_x + (radius - 10) * math.cos(angle) # 计算刻度的终点的横坐标
        y2 = center_y + (radius - 10) * math.sin(angle) # 计算刻度的终点的纵坐标
        pygame.draw.line(surface, BLACK, (x1, y1), (x2, y2), 3) # 绘制一条黑色的线作为刻度

        num = str(i + 1 if i > 0 else 12) # 计算数字的文本（以字符串为单位）
        text = font.render(num, True, BLACK) # 创建一个文本对象
        text_rect = text.get_rect() # 获取文本对象的矩形区域
        text_rect.centerx = center_x + (radius - 25) * math.cos(angle) # 设置文本对象的中心横坐标
        text_rect.centery = center_y + (radius - 25) * math.sin(angle) # 设置文本对象的中心纵坐标
        surface.blit(text, text_rect) # 将文本对象绘制到表面上

    # 绘制指针
    hour_hand = pygame.image.load("hour_hand.png") # 加载时针图片文件
    hour_hand_rect = hour_hand.get_rect() # 获取时针图片文件的矩形区域
    hour_hand_rect.centerx = center_x # 设置时针图片文件的中心横坐标
    hour_hand_rect.centery = center_y # 设置时针图片文件的中心纵坐标
    hour_hand = pygame.transform.rotate(hour_hand, math.degrees(hour_angle))  # 旋转时针图片文件，使其与时针的角度一致
    hour_hand_rect = hour_hand.get_rect(center=hour_hand_rect.center)  # 重新获取时针图片文件的矩形区域，使其中心不变
    surface.blit(hour_hand, hour_hand_rect)  # 将时针图片文件绘制到表面上

    minute_hand = pygame.image.load("minute_hand.png")  # 加载分针图片文件
    minute_hand_rect = minute_hand.get_rect()  # 获取分针图片文件的矩形区域
    minute_hand_rect.centerx = center_x  # 设置分针图片文件的中心横坐标
    minute_hand_rect.centery = center_y  # 设置分针图片文件的中心纵坐标
    minute_hand = pygame.transform.rotate(minute_hand, math.degrees(minute_angle))  # 旋转分针图片文件，使其与分针的角度一致
    minute_hand_rect = minute_hand.get_rect(center=minute_hand_rect.center)  # 重新获取分针图片文件的矩形区域，使其中心不变
    surface.blit(minute_hand, minute_hand_rect)  # 将分针图片文件绘制到表面上

    second_hand = pygame.image.load("second_hand.png")  # 加载秒针图片文件
    second_hand_rect = second_hand.get_rect()  # 获取秒针图片文件的矩形区域
    second_hand_rect.centerx = center_x  # 设置秒针图片文件的中心横坐标
    second_hand_rect.centery = center_y  # 设置秒针图片文件的中心纵坐标
    second_hand = pygame.transform.rotate(second_hand, math.degrees(second_angle))  # 旋转秒针图片文件，使其与秒针的角度一致
    second_hand_rect = second_hand.get_rect(center=second_hand_rect.center)  # 重新获取秒针图片文件的矩形区域，使其中心不变
    surface.blit(second_hand, second_hand_rect)  # 将秒针图片文件绘制到表面上


# 定义一个函数，用于绘制一个环绕时钟的最外围圆形环绕显示的频谱图
def draw_spectrum(surface):
    # 获取当前默认声卡的音频数据，并将其转换为numpy数组
    audio_data = soundcard.get_audio_data()
    audio_array = numpy.frombuffer(audio_data, dtype=numpy.int16)

    # 对音频数据进行快速傅里叶变换（FFT），得到不同频段的强度值
    fft_array = numpy.fft.rfft(audio_array)
    fft_abs_array = numpy.abs(fft_array)

    # 计算表盘的中心和半径
    center_x = surface.get_width() // 2
    center_y = surface.get_height() // 2
    radius = min(center_x, center_y) - 50

    # 绘制一个黑色的圆形边框
    pygame.draw.circle(surface, BLACK, (center_x, center_y), radius + 10, 10)

    # 绘制多个柱状图，表示不同频段的强度值
    bars = 64  # 柱状图的数量
    width = 5  # 柱状图的宽度（以像素为单位）
    gap = 2  # 柱状图之间的间隙（以像素为单位）
    for i in range(bars):
        angle = i * math.pi / bars - math.pi / 2  # 计算柱状图的角度（以弧度为单位）
        x1 = center_x + (radius + 10) * math.cos(angle)  # 计算柱状图的起点的横坐标
        y1 = center_y + (radius + 10) * math.sin(angle)  # 计算柱状图的起点的纵坐标
        length = fft_abs_array[i] / 1000  # 计算柱状图的长度（以像素为单位）
        x2 = center_x + (radius + 10 + length) * math.cos(angle)  # 计算柱状图的终点的横坐标
        y2 = center_y + (radius + 10 + length) * math.sin(angle)  # 计算柱状图的终点的纵坐标
        color = pygame.Color(0, 0, 0)  # 创建一个颜色对象
        color.hsva = (i * 360 / bars, 100, 100, 100)  # 设置颜色对象的色相、饱和度、亮度和透明度
        pygame.draw.line(surface, color, (x1, y1), (x2, y2), width)  # 绘制一条彩色的线作为柱状图


# 定义一个主循环
running = True  # 控制循环是否继续运行的变量
while running:
    # 处理用户输入的事件
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # 如果用户点击了窗口的关闭按钮
            running = False  # 设置循环不再继续运行
        elif event.type == pygame.KEYDOWN:  # 如果用户按下了键盘上的某个键
            if event.key == pygame.K_ESCAPE:  # 如果用户按下了Esc键
                running = False  # 设置循环不再继续运行

    # 在窗口上绘制时钟和频谱图
    window.fill(BLACK)  # 填充窗口的背景颜色为黑色
    draw_clock(window)  # 调用draw_clock函数，在窗口上绘制时钟
    draw_spectrum(window)  # 调用draw_spectrum函数，在窗口上绘制频谱图

    # 更新窗口的显示
    pygame.display.flip()

    # 控制循环的速度
    clock.tick(60)

# 退出pygame模块
pygame.quit()

