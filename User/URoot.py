import tkinter

from User import UFrame, UMenu
from lib.windows import setWindowCenter


class MainPage:
    def __init__(self, last):
        last.destroy()

        self.root = tkinter.Tk()
        self.root.title("互帮互助系统")

        setWindowCenter(self.root, 800, 600)
        UMenu.UMenu(self)  # 使用self可以传递主窗口和主窗口操作函数
        # 初始化Frames
        self.currentFrame = None
        self.pageFrame = {
            "home": UFrame.UHomeFrame,
            "checkUser": UFrame.CheckUser,
            "modifyUser": UFrame.ModifyUser,
            "logout": UFrame.Logout,
            "addItem": UFrame.AddItem,
            "searchItem": UFrame.SearchItem,
        }
        self.openHome()

    def openWindow(self, frameName, title):
        """打开/更换主界面的通用函数"""
        self.root.title(title)
        # 先销毁之前frame
        if self.currentFrame is not None and (hasattr(self.currentFrame.destroy, '__call__')):
            self.currentFrame.destroy()

        self.currentFrame = self.pageFrame[frameName](self.root)
        self.currentFrame.pack()

    def openHome(self):
        """应用主界面"""
        self.openWindow("home", "互帮互助系统-主界面")

    def openCheckUser(self):
        """个人信息查看"""
        self.openWindow("checkUser", "互帮互助系统-个人信息查看")

    def openModifyUser(self):
        """个人信息修改"""
        self.openWindow("modifyUser", "互帮互助系统-个人信息修改")

    def openLogout(self):
        """退出登录"""
        self.openWindow("logout", "互帮互助系统-退出登录")

    def openAddItem(self):
        """物品添加"""
        self.openWindow("addItem", "互帮互助系统-物品添加")

    def openSearchItem(self):
        """物品查找"""
        self.openWindow("searchItem", "互帮互助系统-物品查找")
