# 导入必要的模块
import tkinter as tk
import pyaudio
import numpy as np
import wave
import math
import time


# 定义一个类，用于创建图形界面和显示时钟和频谱图
class ClockSpectrum(tk.Tk):
    def __init__(self):
        # 初始化父类
        super().__init__()
        # 设置窗口标题和大小
        self.title("时钟和频谱图")
        self.geometry("1920x1080")
        # 设置窗口背景颜色为黑色
        self.config(bg="black")
        # 创建一个画布，用于绘制时钟和频谱图
        self.canvas = tk.Canvas(self, width=1920, height=1080, bg="black", highlightthickness=0)
        self.canvas.pack()
        # 创建一个标签，用于显示当前选择的声卡
        self.label = tk.Label(self, text="声卡：", bg="black", fg="white", font=("Arial", 16))
        self.label.place(x=10, y=10)
        # 创建一个下拉菜单，用于选择声卡
        self.devices = self.get_devices()  # 获取可用的声卡列表
        self.device = self.devices[0]  # 设置默认选择的声卡为第一个
        self.device_var = tk.StringVar()  # 创建一个字符串变量，用于存储当前选择的声卡
        self.device_var.set(self.devices[0])  # 设置默认选择的声卡为第一个
        self.option = tk.OptionMenu(self, self.device_var, *self.devices,
                                    command=self.change_device)  # 创建一个下拉菜单，绑定字符串变量和回调函数
        self.option.config(bg="black", fg="white", font=("Arial", 16))  # 设置下拉菜单的样式
        self.option.place(x=80, y=10)  # 设置下拉菜单的位置
        # 初始化一些常量和变量，用于绘制时钟和频谱图
        self.center_x = 400  # 时钟中心点的x坐标
        self.center_y = 500  # 时钟中心点的y坐标
        self.radius = 300  # 时钟的半径
        self.hour_length = 150  # 时针的长度
        self.minute_length = 200  # 分针的长度
        self.second_length = 250  # 秒针的长度
        self.hour_angle = 0  # 时针的角度（弧度）
        self.minute_angle = 0  # 分针的角度（弧度）
        self.second_angle = 0  # 秒针的角度（弧度）
        self.hour_id = None  # 时针在画布上的id
        self.minute_id = None  # 分针在画布上的id
        self.second_id = None  # 秒针在画布上的id
        self.spectrum_width = 20  # 频谱图每个柱状图的宽度（像素）
        self.spectrum_height = 100000  # 频谱图每个柱状图的最大高度（像素）
        self.spectrum_num = int(2 * math.pi * (self.radius + 10) / self.spectrum_width)  # 频谱图柱状图的数量（根据圆周长计算）
        self.spectrum_data = [0] * self.spectrum_num  # 频谱图柱状图的数据（初始为0）
        self.spectrum_ids = [None] * self.spectrum_num  # 频谱图柱状图在画布上的id列表（初始为None）

    def get_devices(self):
        # 定义一个函数，用于获取可用的声卡列表
        p = pyaudio.PyAudio()  # 创建一个pyaudio对象
        devices = []  # 创建一个空列表，用于存储声卡名称
        for i in range(p.get_device_count()):  # 遍历所有设备
            info = p.get_device_info_by_index(i)  # 获取设备信息
            if info["maxInputChannels"] > 0:  # 如果设备有输入通道
                devices.append(info["name"])  # 将设备名称添加到列表中
        p.terminate()  # 关闭pyaudio对象
        return devices  # 返回声卡列表

    def change_device(self, value):
        # 定义一个函数，用于切换声卡
        self.device = value  # 将当前选择的声卡赋值给self.device
        self.stop_stream()  # 停止当前的音频流
        self.start_stream()  # 开启新的音频流

    def start_stream(self):
        # 定义一个函数，用于开启音频流
        p = pyaudio.PyAudio()  # 创建一个pyaudio对象
        device_index = self.devices.index(self.device)  # 获取当前选择的声卡的索引
        self.stream = p.open(format=pyaudio.paInt16, channels=1, rate=44100, input=True,input_device_index=device_index, frames_per_buffer=512,stream_callback=self.callback)  # 创建一个音频流，绑定回调函数
        self.stream.start_stream()  # 开启音频流

    def stop_stream(self):
        # 定义一个函数，用于停止音频流
        if hasattr(self, "stream"):  # 如果self有stream属性
            self.stream.stop_stream()  # 停止音频流
            self.stream.close()  # 关闭音频流

    def callback(self, in_data, frame_count, time_info, status):
        # 定义一个函数，用于处理音频数据
        data = np.frombuffer(in_data, dtype=np.int16)  # 将字节数据转换为整数数组
        data = data / 32768.0  # 将整数数组归一化为浮点数数组
        spectrum = np.abs(np.fft.rfft(data))  # 对数据进行快速傅里叶变换，得到频谱数据
        spectrum = spectrum / len(spectrum) * 2  # 对频谱数据进行归一化处理
        spectrum = spectrum[:self.spectrum_num]  # 截取前self.spectrum_num个数据，作为频谱图的数据
        self.spectrum_data = spectrum.tolist()  # 将频谱数据转换为列表，赋值给self.spectrum_data
        return (None, pyaudio.paContinue)  # 返回一个元组，表示继续处理音频数据

    def draw_clock(self):
        # 定义一个函数，用于绘制时钟
        self.canvas.create_oval(self.center_x - self.radius, self.center_y - self.radius, self.center_x + self.radius,
                                self.center_y + self.radius, fill="black", outline="white", width=5)  # 绘制时钟的圆形边框
        for i in range(12):  # 遍历12个刻度
            angle = i * math.pi / 6 - math.pi / 2  # 计算刻度的角度（弧度）
            x1 = self.center_x + (self.radius - 10) * math.cos(angle)  # 计算刻度的起点x坐标
            y1 = self.center_y + (self.radius - 10) * math.sin(angle)  # 计算刻度的起点y坐标
            x2 = self.center_x + (self.radius - 20) * math.cos(angle) if i % 3 == 0 else self.center_x + (
                        self.radius - 15) * math.cos(angle)  # 计算刻度的终点x坐标（根据是否是整点刻度决定长度）
            y2 = self.center_y + (self.radius - 20) * math.sin(angle) if i % 3 == 0 else self.center_y + (
                        self.radius - 15) * math.sin(angle)  # 计算刻度的终点y坐标（根据是否是整点刻度决定长度）
            self.canvas.create_line(x1, y1, x2, y2, fill="white", width=3 if i % 3 == 0 else 2)  # 绘制刻度线（根据是否是整点刻度决定宽度）

    def update_clock(self):
        # 定义一个函数，用于更新时钟的指针和时间显示
        now = time.localtime()  # 获取当前的本地时间
        hour = now.tm_hour % 12  # 获取当前的小时数（转换为12小时制）
        minute = now.tm_min  # 获取当前的分钟数
        second = now.tm_sec  # 获取当前的秒数
        self.hour_angle = (hour + minute / 60) * math.pi / 6 - math.pi / 2  # 计算时针的角度（弧度）
        self.minute_angle = (minute + second / 60) * math.pi / 30 - math.pi / 2  # 计算分针的角度（弧度）
        self.second_angle = second * math.pi / 30 - math.pi / 2  # 计算秒针的角度（弧度）
        hour_x = self.center_x + self.hour_length * math.cos(self.hour_angle)  # 计算时针的终点x坐标
        hour_y = self.center_y + self.hour_length * math.sin(self.hour_angle)  # 计算时针的终点y坐标
        minute_x = self.center_x + self.minute_length * math.cos(self.minute_angle)  # 计算分针的终点x坐标
        minute_y = self.center_y + self.minute_length * math.sin(self.minute_angle)  # 计算分针的终点y坐标
        second_x = self.center_x + self.second_length * math.cos(self.second_angle)  # 计算秒针的终点x坐标
        second_y = self.center_y + self.second_length * math.sin(self.second_angle)  # 计算秒针的终点y坐标
        if self.hour_id:  # 如果时针已经存在
            self.canvas.delete(self.hour_id)  # 删除时针
        if self.minute_id:  # 如果分针已经存在
            self.canvas.delete(self.minute_id)  # 删除分针
        if self.second_id:  # 如果秒针已经存在
            self.canvas.delete(self.second_id)  # 删除秒针
        self.hour_id = self.canvas.create_line(self.center_x, self.center_y, hour_x, hour_y, fill="white",
                                               width=5)  # 绘制时针，保存id
        self.minute_id = self.canvas.create_line(self.center_x, self.center_y, minute_x, minute_y, fill="white",
                                                 width=3)  # 绘制分针，保存id
        self.second_id = self.canvas.create_line(self.center_x, self.center_y, second_x, second_y, fill="red",
                                                 width=2)  # 绘制秒针，保存id
        time_str = f"{hour:02d}:{minute:02d}:{second:02d}"  # 格式化时间字符串
        self.canvas.create_text(self.center_x, self.center_y, text=time_str, fill="white",
                                font=("Arial", 32))  # 在时钟中心显示时间字符串

    def draw_spectrum(self):
        # 定义一个函数，用于绘制频谱图
        for i in range(self.spectrum_num):  # 遍历每个柱状图
            angle = i * 2 * math.pi / self.spectrum_num - math.pi / 2  # 计算柱状图的角度（弧度）
            x1 = self.center_x + (self.radius + 10) * math.cos(angle)  # 计算柱状图的起点x坐标
            y1 = self.center_y + (self.radius + 10) * math.sin(angle)  # 计算柱状图的起点y坐标
            x2 = x1 + (self.spectrum_height * self.spectrum_data[i]) * math.cos(angle)  # 计算柱状图的终点x坐标（根据频谱数据决定长度）
            y2 = y1 + (self.spectrum_height * self.spectrum_data[i]) * math.sin(angle)  # 计算柱状图的终点y坐标（根据频谱数据决定长度）
            if self.spectrum_ids[i]:  # 如果柱状图已经存在
                self.canvas.delete(self.spectrum_ids[i])  # 删除柱状图
            color = f"#{int(255 * (1 - self.spectrum_data[i])):02x}{int(255 * (1 - abs(0.5 - self.spectrum_data[i]) * 2)):02x}{int(255 * (self.spectrum_data[i])):02x}"  # 根据频谱数据决定柱状图的颜色（RGB）
            self.spectrum_ids[i] = self.canvas.create_line(x1, y1, x2, y2, fill=color,
                                                           width=self.spectrum_width)  # 绘制柱状图，保存id

    def update(self):
        # 定义一个函数，用于更新画布
        self.canvas.delete("all")  # 清空画布
        self.draw_clock()  # 绘制时钟
        self.update_clock()  # 更新时钟
        self.draw_spectrum()  # 绘制频谱图
        self.after(45, self.update)  # 100毫秒后再次调用自己

    def run(self):
        # 定义一个函数，用于运行程序
        self.start_stream()  # 开启音频流
        self.update()  # 更新画布
        self.mainloop()  # 进入主循环

# 创建一个ClockSpectrum对象
app = ClockSpectrum()
# 运行程序
app.run()
