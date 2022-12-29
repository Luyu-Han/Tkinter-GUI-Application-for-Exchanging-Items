import tkinter
from tkinter import messagebox

import lib.GlobalVar as glv

from lib import manageDB
from Admin.ARoot import MainPage as AMainPage
from User.URoot import MainPage as UMainPage


class Login:
    """初始登录界面，需选择普通用户/管理员登录"""
    def __init__(self, last):
        last.destroy()

        self.root = tkinter.Tk()
        self.root.title("互帮互助系统")
        self.root.geometry('300x200+600+300')

        label1 = tkinter.Label(text='请选择登录身份：', font=('宋体', 12), bd=20)
        label1.pack()

        administrator = tkinter.Button(text='管理员', command=self.adminLogin)
        administrator.pack()
        administrator.place(relx=0.42, rely=0.3)

        user = tkinter.Button(text='普通用户', command=self.userLogin)
        user.pack()
        user.place(relx=0.4, rely=0.6)

        close = tkinter.Button(text='退出系统', command=self.root.destroy)
        close.pack()
        close.place(relx=0.75, rely=0.8)

    def adminLogin(self):
        login = AdminLogin(self.root)
        login.root.mainloop()

    def userLogin(self):
        login = UserLogin(self.root)
        login.root.mainloop()


class AdminLogin:
    """管理员登录界面"""
    def __init__(self, last):
        last.destroy()

        self.root = tkinter.Tk()
        self.root.title("互帮互助系统")
        self.root.geometry('500x300+500+200')
        self.password = tkinter.StringVar()
        self.userName = tkinter.StringVar()

        label0 = tkinter.Label(text='管理员登录', font=20)
        label0.place(relx=0.45, rely=0.1)
        label2 = tkinter.Label(text='请输入用户名：', font=('宋体', 10))
        label2.place(relx=0.2, rely=0.3)
        label3 = tkinter.Label(text='请输入密码：', font=('宋体', 10))
        label3.place(relx=0.2, rely=0.5)

        backButton = tkinter.Button(self.root, text='返回上一步', command=self.back)
        backButton.pack()
        backButton.place(relx=0.8, rely=0.8)

        # userName, password分别记录用户输入的用户名、密码
        p = tkinter.Entry(self.root, show='*', textvariable=self.password)
        p.pack()
        p.place(relx=0.4, rely=0.5)
        u = tkinter.Entry(self.root, textvariable=self.userName)
        u.pack()
        u.place(relx=0.4, rely=0.3)

        loginButton = tkinter.Button(self.root, text='确认', command=self.checkUser)
        loginButton.pack()
        loginButton.place(relx=0.5, rely=0.7)

    def back(self):
        """返回上一步"""
        Login(self.root)

    def checkUser(self):
        """检查管理员的用户名、密码输入是否正确"""
        res1 = manageDB.loginAdminName(self.userName.get())
        res2 = manageDB.loginAdminPass(self.userName.get(), self.password.get())

        if res2:
            glv.setVar("CURRENT_USER_NAME", str(self.userName))
            AMainPage(self.root)

        elif not res1:
            messagebox.showinfo(title="错误", message="您输入的用户不存在，请确认用户名是否正确。")

        else:
            messagebox.showinfo(title="错误", message="密码有误，请重新输入。")


class UserLogin:
    """普通用户登录界面"""
    def __init__(self, last):
        last.destroy()

        self.root = tkinter.Tk()
        self.root.title("互帮互助系统登录")
        self.root.geometry('500x300+500+200')
        self.password = tkinter.StringVar()
        self.userName = tkinter.StringVar()

        # 较管理员登录，增添新用户注册功能
        registerButton = tkinter.Button(self.root, text='新用户注册', command=self.register)
        registerButton.pack()
        registerButton.place(relx=0.8, rely=0.1)

        label0 = tkinter.Label(text='普通用户登录', font=20)
        label0.place(relx=0.45, rely=0.1)
        label2 = tkinter.Label(text='请输入用户名：', font=('宋体', 10))
        label2.place(relx=0.2, rely=0.3)
        label3 = tkinter.Label(text='请输入密码：', font=('宋体', 10))
        label3.place(relx=0.2, rely=0.5)

        # userName, password分别记录用户输入的用户名、密码
        p = tkinter.Entry(self.root, show='*', textvariable=self.password)
        p.pack()
        p.place(relx=0.4, rely=0.5)
        u = tkinter.Entry(self.root, textvariable=self.userName)
        u.pack()
        u.place(relx=0.4, rely=0.3)

        backButton = tkinter.Button(self.root, text='返回上一步', command=self.back)
        backButton.pack()
        backButton.place(relx=0.8, rely=0.8)

        loginButton = tkinter.Button(self.root, text='确认', command=self.checkUser)
        loginButton.pack()
        loginButton.place(relx=0.5, rely=0.7)

        self.root.mainloop()

    def register(self):
        """新用户注册功能"""
        NewUserRegister(self.root)

    def back(self):
        """返回上一步"""
        Login(self.root)

    def checkUser(self):
        """检查普通用户的用户名、密码输入是否正确"""
        res1 = manageDB.loginName(self.userName.get())
        res2 = manageDB.loginPass(self.userName.get(), self.password.get())

        if res2:
            glv.setVar("CURRENT_USER_NAME", str(self.userName))
            UMainPage(self.root)

        elif not res1:
            messagebox.showinfo(title="错误", message="您输入的用户不存在，请确认用户名是否正确。")

        else:
            messagebox.showinfo(title="错误", message="密码有误，请重新输入。")


class NewUserRegister:
    """新用户注册，用户名、密码符合要求后，进入管理员审核阶段"""
    def __init__(self, last):
        last.destroy()

        self.root = tkinter.Tk()
        self.root.title("互帮互助系统")
        self.root.geometry('500x300+500+200')
        self.userName = tkinter.StringVar()
        self.password = tkinter.StringVar()
        self.number = tkinter.StringVar()
        self.address = tkinter.StringVar()

        tkinter.Label(text='新用户注册', font=20).place(relx=0.45, rely=0.1)
        tkinter.Label(text='请输入用户名：', font=('宋体', 10)).place(relx=0.2, rely=0.35)
        userName = tkinter.Entry(self.root, textvariable=self.userName)
        userName.pack()
        userName.place(relx=0.55, rely=0.35)
        tkinter.Label(text='请输入密码：', font=('宋体', 10)).place(relx=0.2, rely=0.45)
        password = tkinter.Entry(self.root, show='*', textvariable=self.password)
        password.pack()
        password.place(relx=0.55, rely=0.45)
        tkinter.Label(text='请输入联系电话：', font=('宋体', 10)).place(relx=0.2, rely=0.55)
        number = tkinter.Entry(self.root, textvariable=self.number)
        number.pack()
        number.place(relx=0.55, rely=0.55)
        tkinter.Label(text='请输入住址：', font=('宋体', 10)).place(relx=0.2, rely=0.65)
        address = tkinter.Entry(self.root, textvariable=self.address)
        address.pack()
        address.place(relx=0.55, rely=0.65)

        backButton = tkinter.Button(self.root, text='返回上一步', command=self.back)
        backButton.pack()
        backButton.place(relx=0.8, rely=0.8)

        confirmButton = tkinter.Button(self.root, text='确认', command=self.confirm)
        confirmButton.pack()
        confirmButton.place(relx=0.5, rely=0.8)

        self.root.mainloop()

    def back(self):
        """返回上一步"""
        UserLogin(self.root)

    def confirm(self):
        """检查注册信息是否填写完整"""
        res = manageDB.addRegistrant(self.userName.get(), self.password.get(), self.number.get(), self.address.get())
        if res:
            self.userName.set("")
            self.password.set("")
            self.number.set("")
            self.address.set("")
            messagebox.showinfo(title="成功", message="账号注册成功，等待管理员审核")
        else:
            messagebox.showinfo(title="出错", message="请将所有信息填写完整，谢谢")
