import tkinter

from Admin import AFrame, AMenu
from lib.windows import setWindowCenter


class MainPage:
    def __init__(self, last):
        last.destroy()

        self.root = tkinter.Tk()
        self.root.title("互帮互助 管理系统")

        setWindowCenter(self.root, 800, 600)
        AMenu.AMenu(self)  # 使用self可以传递主窗口和主窗口操作函数
        # 初始化Frames
        self.currentFrame = None
        self.pageFrame = {
            "home": AFrame.AHomeFrame,
            "checkNewUser": AFrame.CheckNewUser,
            "userList": AFrame.UserList,
            "addAdmin": AFrame.AddAdmin,
            "addItemClass": AFrame.AddItemClass,
            "classList": AFrame.ClassList,
            "modifyItemClass": AFrame.ModifyItemClass
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
        self.openWindow("home", "互帮互助 管理系统-主界面")

    def openCheckNewUser(self):
        """新用户审核"""
        self.openWindow("checkNewUser", "互帮互助 管理系统-新用户审核")

    def openUserList(self):
        """用户信息查看"""
        self.openWindow("userList", "互帮互助 管理系统-用户信息查看")

    def openAddAdmin(self):
        """管理员账户添加"""
        self.openWindow("addAdmin", "互帮互助 管理系统-管理员账户添加")

    def openAddItemClass(self):
        """类别新增"""
        self.openWindow("addItemClass", "互帮互助 管理系统-类别新增")

    def openClassList(self):
        """全部类别查看"""
        self.openWindow("classList", "互帮互助 管理系统-全部类别查看")

    def openModifyItemClass(self):
        """物品类别修改"""
        self.openWindow("modifyItemClass", "互帮互助 管理系统-物品类别修改")
