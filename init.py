import tkinter
from tkinter import Tk
from tkinter import messagebox

from lib.windows import setWindowCenter
from lib.sqliteDB import UserDB, NewUserDB, ItemDB, AdminDB, ClassDB
from main import App


class InitWindow(Tk):
    """初始化窗口"""

    def __init__(self):
        Tk.__init__(self)
        self.title("初始化数据")
        setWindowCenter(self, 300, 180)
        self.resizable(False, False)
        self.winSuccess = None  # 初始化成功的提示窗口
        self.initPage()

    def initPage(self):
        """初始化数据库窗口"""
        tkinter.Button(self, text="初始化数据库", command=self.initDB).pack(expand="yes", padx=10, pady=10, ipadx=5, ipady=5)

    def initDB(self):
        """实现初始化数据库"""
        db1 = UserDB()
        db2 = AdminDB()
        db3 = NewUserDB()
        db4 = ItemDB()
        db5 = ClassDB()

        db1.resetDB()
        db1.createDB()
        db2.resetDB()
        db2.createDB()
        db3.resetDB()
        db3.createDB()
        db4.resetDB()
        db4.createDB()
        db5.createDB()
        db5.resetDB()

        try:
            """设置各数据库的初始数据"""
            tmp1 = db1.addUser("user", "123456", "123456", "1-202")
            tmp2 = db2.addNewAdmin("admin", "admin")
            tmp3 = db3.addNewUser("newUser", "123456", "123456", "1-202")
            tmp4 = db4.addItem("食品", "巧克力", "*1", "1-202", "123456", "123456@qq.com")
            db4.addItem("食品", "果冻", "*2", "1-101", "123456", "123456@qq.com")
            db4.addItem("药物", "布洛芬", "6粒，保质期至2023年6月", "1-202", "123456", "123")
            db4.addItem("书籍", "哈利波特", "J.K.罗琳，9成新", "1-202", "123456", "123")
            tmp5 = db5.addClass("食品", "请在”描述”中输入食品的数量、保质期等信息")
            db5.addClass("药物", "请在”描述”中输入药物的数量、保质期、适用症、敏感人群等信息")
            db5.addClass("书籍", "请在”描述”中输入书籍的作者、出版社、新旧程度等信息")
            print("添加用户user:", tmp1)
            print("添加用户admin:", tmp2)
            print("添加新用户newUser:", tmp3)
            print("添加物品item:", tmp4)
            print("添加物品类别：", tmp5)

            self.doSuccess()
            self.destroy()
        except KeyError:
            print(KeyError)
            self.doFailed()

    def doFailed(self):
        """若初始化失败是否重试"""
        res = tkinter.messagebox.askretrycancel('提示', '初始化失败，是否重试？', parent=self)
        if res is True:
            self.initDB()
        elif res is False:
            self.destroy()

    def doSuccess(self):
        """初始化成功弹窗，选择启动程序或退出"""
        self.winSuccess = Tk()
        self.winSuccess.title("初始化成功")
        setWindowCenter(self.winSuccess, 250, 150)
        self.winSuccess.resizable(False, False)
        msg = tkinter.Label(self.winSuccess, text="初始化成功")
        msg.pack(expand="yes", fill="both")

        btn = tkinter.Button(self.winSuccess, text="确定", command=self.quit)
        btn.pack(side="right", padx=10, pady=10, ipadx=5, ipady=5)
        openButton = tkinter.Button(self.winSuccess, text="启动程序", command=self.openApp)
        openButton.pack(side="right", padx=10, pady=10, ipadx=5, ipady=5)

    def openApp(self):
        """打开应用程序"""
        self.quit()
        self.winSuccess.destroy()
        self.winSuccess.quit()

        App()


if __name__ == "__main__":
    APP_INIT = InitWindow()
    APP_INIT.mainloop()

