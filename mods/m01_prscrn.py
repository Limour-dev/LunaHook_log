from PIL import ImageGrab
import tkinter
import ctypes


class CTkPrScrn:
    def __init__(self, rectangle=None):
        if rectangle is None:
            rectangle = (0, 0, 0, 0, 1)
        self.__start_x, self.__start_y, self.__end_x, self.__end_y, self.__scale = rectangle
        self.__init_x, self.__init_y = 0, 0

    def setRectangle(self, _top=None):
        if _top is None:
            __win = tkinter.Tk()
        else:
            __win = tkinter.Toplevel(_top)
        self.__win = __win  # 传递窗口对象
        __win.attributes("-alpha", 0.5)  # 设置窗口半透明
        __win.attributes("-fullscreen", True)  # 设置全屏
        __win.attributes("-topmost", True)  # 设置窗口在最上层
        __width, __height = __win.winfo_screenwidth(), __win.winfo_screenheight()
        # 创建画布
        __canvas = tkinter.Canvas(__win, width=__width, height=__height, bg="gray")
        self.__canvas = __canvas  # 传递窗口对象
        __win.bind('<Button-1>', self.xFunc1)  # 绑定鼠标左键点击事件
        __win.bind('<ButtonRelease-1>', self.xFunc1)  # 绑定鼠标左键点击释放事件
        __win.bind('<B1-Motion>', self.xFunc2)  # 绑定鼠标左键点击移动事件
        __win.bind('<Escape>', lambda e: self.__win.destroy())  # 绑定Esc按键退出事件
        user32 = ctypes.windll.user32
        gdi32 = ctypes.windll.gdi32
        dc = user32.GetDC(None)
        widthScale = gdi32.GetDeviceCaps(dc, 8)  # 分辨率缩放后的宽度
        heightScale = gdi32.GetDeviceCaps(dc, 10)  # 分辨率缩放后的高度
        width = gdi32.GetDeviceCaps(dc, 118)  # 原始分辨率的宽度
        height = gdi32.GetDeviceCaps(dc, 117)  # 原始分辨率的高度
        self.__scale = width / widthScale
        print('m01_prscrn setRectangle 创建遮罩', __width, __height, widthScale, heightScale, width, height,
              self.__scale)
        if _top is None:
            __win.mainloop()
        else:
            _top.wait_window(__win)
        return self.getRectangle()

    def _setRectangle(self, _e_x, _e_y):
        if self.__init_x < _e_x:
            self.__end_x = _e_x
        else:
            self.__start_x = _e_x

        if self.__init_y < _e_y:
            self.__end_y = _e_y
        else:
            self.__start_y = _e_y

    def getRectangle(self):
        return (self.__start_x, self.__start_y, self.__end_x, self.__end_y, self.__scale)

    def __call__(self):
        assert self.__end_x > self.__start_x and self.__end_y > self.__start_y
        im = ImageGrab.grab((self.__scale * self.__start_x, self.__scale * self.__start_y,
                             self.__scale * self.__end_x, self.__scale * self.__end_y))
        return im

    def xFunc1(self, event):
        # print(f"鼠标左键点击了一次坐标是:x={g_scale * event.x}, y={g_scale * event.y}")
        if event.state == 8:  # 鼠标左键按下
            self.__init_x, self.__init_y = event.x, event.y
            self.__start_x, self.__start_y = self.__init_x, self.__init_y
            self.__end_x, self.__end_y = self.__init_x, self.__init_y
        elif event.state == 264:  # 鼠标左键释放
            self._setRectangle(event.x, event.y)
            print('m01_prscrn xFunc1 获取区域坐标', self.getRectangle())
            self.__win.destroy()

    def xFunc2(self, event):
        self._setRectangle(event.x, event.y)
        self.__canvas.delete("prscrn")
        self.__canvas.create_rectangle(self.__start_x, self.__start_y, self.__end_x, self.__end_y,
                                       fill='white', outline='red', tags="prscrn")
        # 包装画布
        self.__canvas.pack()

    def __repr__(self):
        return f'CTkPrScrn(rectangle={self.getRectangle()})'


if __name__ == '__main__':
    prScrn = CTkPrScrn()
    prScrn.setRectangle()
    print(prScrn)
    prScrn().show()
