"""程序入口文件"""

import os
from tkinter import Tk

import lib.GlobalVar as glv
from windows import winLogin

glv.initGlobalVar()
glv.setVar("APP_NAME", "Application")
glv.setVar("APP_PATH", os.path.dirname(__file__))  # 当前目录
glv.setVar("DATA_DIR", "data")


class App(Tk):
    def __init__(self):
        Tk.__init__(self)
        winLogin.Login(self)

        self.mainloop()


if __name__ == '__main__':
    App()
