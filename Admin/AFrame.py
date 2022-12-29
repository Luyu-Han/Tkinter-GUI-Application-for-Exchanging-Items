import tkinter
from abc import abstractmethod
from tkinter import messagebox
from tkinter import ttk

import lib.manageDB as manageDB
from lib.windows import treeviewSortColumn, setWindowCenter


class AHomeFrame(tkinter.Frame):
    """管理员初始界面"""
    def __init__(self, last=None):
        tkinter.Frame.__init__(self, last)

        self.root = last
        self.initGUI()

    def initGUI(self):
        """初始显示 欢迎用户界面"""
        tkinter.Label(self, text='欢迎使用管理系统！').pack()
        tkinter.Label(self, text='请使用上方工具栏选择所需功能。').pack()


@abstractmethod
class ListAll(tkinter.Frame):
    """所有涉及列出数据库全部数据的抽象类"""
    def __init__(self, last=None):
        tkinter.Frame.__init__(self, last)
        self.root = last
        self.list = []
        self.selectedItem = None
        self.selectedName = tkinter.StringVar()
        self.initPage()

    def select(self, event):
        """选中"""
        # event.widget获取Treeview对象，调用selection获取选择所有选中的
        slct = event.widget.selection()[0]
        self.selectedItem = self.tree.item(slct)
        self.selectedName.set(self.selectedItem["values"][1])

    def initPage(self):
        pass


# 对应Menu中每个功能的界面窗口设置
class CheckNewUser(ListAll):
    """新用户审核界面定义及功能实现"""

    def initPage(self):
        """加载控件,分别是新用户的审核通过与删除"""
        self.list = manageDB.registrantList()

        headFrame = tkinter.LabelFrame(self, text="新用户审核")
        headFrame.grid(row=0, column=0, columnspan=2, sticky="nswe")
        tkinter.Label(headFrame, textvariable=self.selectedName).pack()

        passButton = tkinter.Button(headFrame, text="审核通过", command=self.passUser)
        passButton.pack(side="left")
        delButton = tkinter.Button(headFrame, text="拒绝并删除", command=self.delUser)
        delButton.pack(side="left")

        # 表格
        self.tree = ttk.Treeview(self, show="headings")
        self.tree["columns"] = ("序号", "姓名", "密码", "联系电话", "住址")

        self.tree.heading("序号", text="序号")
        self.tree.heading("姓名", text="姓名")
        self.tree.heading("密码", text="密码")
        self.tree.heading("联系电话", text="联系电话")
        self.tree.heading("住址", text="住址")

        # 插入数据
        num = 1
        for i in self.list:
            self.tree.insert(
                "",
                num,
                text="",
                values=(i["id"], i["name"], i["password"], i["num"], i["address"]),
            )

        # 选中行
        self.tree.bind("<<TreeviewSelect>>", self.select)

        # 排序
        for col in self.tree["columns"]:  # 给所有标题加
            self.tree.heading(
                col,
                text=col,
                command=lambda _col=col: treeviewSortColumn(
                    self.tree, _col, False
                ),
            )

        vbar = ttk.Scrollbar(self, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=vbar.set)
        self.tree.grid(row=1, column=0, sticky="nsew")
        vbar.grid(row=1, column=1, sticky="ns")

    def passUser(self):
        """管理员点击 审核通过 按钮，准入新注册用户"""
        if self.selectedItem is None:
            messagebox.showinfo("提示", "请先选择需要操作的用户")
        else:
            messagebox.showinfo("准入新注册用户？", self.selectedItem)  # 弹出消息提示框
            manageDB.addUser(self.selectedItem["values"][1], self.selectedItem["values"][2],
                             self.selectedItem["values"][3], self.selectedItem["values"][4])
            manageDB.delRegistrant(self.selectedItem["values"][1])
            messagebox.showinfo(title="成功", message="新用户添加成功")
            self.initPage()

    def delUser(self):
        """管理员点击 拒绝并删除 按钮，去除无效注册用户"""
        if self.selectedItem is None:
            messagebox.showinfo("提示", "请先选择需要操作的用户")
        else:
            messagebox.showinfo("删除用户？", self.selectedItem)  # 弹出消息提示框
            manageDB.delRegistrant(self.selectedItem["values"][1])
            self.initPage()


class UserList(ListAll):
    """用户信息查看界面定义及功能实现"""

    def initPage(self):
        """加载控件,仅包括用户的删除"""
        self.list = manageDB.userList()

        headFrame = tkinter.LabelFrame(self, text="用户信息查看")
        headFrame.grid(row=0, column=0, columnspan=2, sticky="nswe")
        tkinter.Label(headFrame, textvariable=self.selectedName).pack()

        delButton = tkinter.Button(headFrame, text="删除用户", command=self.delUser)
        delButton.pack(side="left")

        # 表格
        self.tree = ttk.Treeview(self, show="headings")
        self.tree["columns"] = ("序号", "姓名", "密码", "联系电话", "住址")

        self.tree.heading("序号", text="序号")
        self.tree.heading("姓名", text="姓名")
        self.tree.heading("密码", text="密码")
        self.tree.heading("联系电话", text="联系电话")
        self.tree.heading("住址", text="住址")

        # 插入数据
        num = 1
        for i in self.list:
            self.tree.insert(
                "",
                num,
                text="",
                values=(i["id"], i["name"], i["password"], i["num"], i["address"]),
            )

        # 选中行
        self.tree.bind("<<TreeviewSelect>>", self.select)

        # 排序
        for col in self.tree["columns"]:  # 给所有标题加
            self.tree.heading(
                col,
                text=col,
                command=lambda _col=col: treeviewSortColumn(
                    self.tree, _col, False
                ),
            )

        vbar = ttk.Scrollbar(self, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=vbar.set)
        self.tree.grid(row=1, column=0, sticky="nsew")
        vbar.grid(row=1, column=1, sticky="ns")

    def delUser(self):
        """点击 删除用户，删除已有用户"""
        if self.selectedItem is None:
            messagebox.showinfo("提示", "请先选择需要操作的用户")
        else:
            messagebox.showinfo("删除用户？", self.selectedItem)  # 弹出消息提示框
            manageDB.delUser(self.selectedItem["values"][1])
            self.initPage()


class AddAdmin(tkinter.Frame):
    """管理员账号添加界面定义及功能实现"""
    def __init__(self, last=None):
        tkinter.Frame.__init__(self, last)
        self.root = last
        self.adminName = tkinter.StringVar()
        self.password = tkinter.StringVar()
        self.initPage()

    def initPage(self):
        """加载界面，实现添加管理员账户，类似于用户注册界面"""
        tkinter.Label(self).grid(row=0, stick="w", pady=10)

        tkinter.Label(self, text="请输入新增管理员账户名: ").grid(row=1, stick="w", pady=10)
        tkinter.Entry(self, textvariable=self.adminName).grid(row=1, column=1, stick="we")

        tkinter.Label(self, text="请输入密码: ").grid(row=2, stick="w", pady=10)
        tkinter.Entry(self, textvariable=self.password, show='*').grid(row=2, column=1, stick="we")

        tkinter.Button(self, text="确认新增", command=self.addAdmin).grid(row=3, column=1, stick="w", pady=10)

    def addAdmin(self):
        """点击 确认添加 按钮后，添加新的物品类别"""
        res = manageDB.addAdmin(self.adminName.get(), self.password.get())
        if res is True:
            self.adminName.set("")
            self.password.set("")
            messagebox.showinfo(title="成功", message="管理员账户新增成功")
        else:
            messagebox.showinfo(title="错误", message="请将新增管理员账户名与密码填写完整；若已填写完整，则为用户名已存在，请重新输入")


class AddItemClass(tkinter.Frame):
    """类别新增界面定义及功能实现"""
    def __init__(self, parent=None):
        tkinter.Frame.__init__(self, parent)
        self.root = parent
        self.cla = tkinter.StringVar()
        self.desc = tkinter.StringVar()
        self.initPage()

    def initPage(self):
        """加载控件, 包括类别名称与类别信息描述的填写"""
        tkinter.Label(self).grid(row=0, stick="w", pady=10)

        tkinter.Label(self, text="新增类别名称: ").grid(row=1, stick="w", pady=10)
        tkinter.Entry(self, textvariable=self.cla).grid(row=1, column=1, stick="we")

        tkinter.Label(self, text="内容: ").grid(row=2, stick="nw", pady=10)
        tkinter.Entry(self, textvariable=self.desc).grid(row=2, column=1, stick="we")

        tkinter.Button(self, text="确认添加", command=self.addClass).grid(row=3, column=1, stick="w", pady=10)

    def addClass(self):
        """点击 确认添加 按钮后，添加新的物品类别"""
        res = manageDB.addClass(self.cla.get(), self.desc.get())
        if res is True:
            self.cla.set("")
            self.desc.set("")
            messagebox.showinfo(title="成功", message="物品类别添加成功")
        else:
            messagebox.showinfo(title="错误", message="请将新增类别名称与描述填写完整")


class ClassList(ListAll):
    """全部类别查看界面定义及功能实现"""

    def initPage(self):
        """加载控件,仅包括用户的删除"""
        self.list = manageDB.classList()

        headFrame = tkinter.LabelFrame(self, text="全部类别查看")
        headFrame.grid(row=0, column=0, columnspan=2, sticky="nswe")
        tkinter.Label(headFrame, textvariable=self.selectedName).pack()

        delButton = tkinter.Button(headFrame, text="删除类别", command=self.delClass)
        delButton.pack(side="left")

        # 表格
        self.tree = ttk.Treeview(self, show="headings")
        self.tree["columns"] = ("序号", "类别名称", "描述")

        self.tree.heading("序号", text="序号")
        self.tree.heading("类别名称", text="类别名称")
        self.tree.heading("描述", text="描述")

        # 插入数据
        num = 1
        for i in self.list:
            self.tree.insert(
                "",
                num,
                text="",
                values=(i["id"], i["name"], i["desc"]),
            )

        # 选中行
        self.tree.bind("<<TreeviewSelect>>", self.select)

        # 排序
        for col in self.tree["columns"]:  # 给所有标题加
            self.tree.heading(
                col,
                text=col,
                command=lambda _col=col: treeviewSortColumn(
                    self.tree, _col, False
                ),
            )

        vbar = ttk.Scrollbar(self, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=vbar.set)
        self.tree.grid(row=1, column=0, sticky="nsew")
        vbar.grid(row=1, column=1, sticky="ns")

    def delClass(self):
        """点击 删除类别，删除现有类别"""
        if self.selectedItem is None:
            messagebox.showinfo("提示", "请先选择需要操作的类别")
        else:
            messagebox.showinfo("删除类别？", self.selectedItem)  # 弹出消息提示框
            manageDB.delClass(self.selectedItem["values"][1])
            self.initPage()


class ModifyItemClass(ListAll):
    """物品类别修改界面定义及功能实现"""
    def __init__(self, last=None):
        super().__init__(last)
        self.newCla = tkinter.StringVar()

    def initPage(self):
        """加载控件,包括物品的删除与类别修改"""
        self.list = manageDB.itemList()

        headFrame = tkinter.LabelFrame(self, text="物品类别修改")
        headFrame.grid(row=0, column=0, columnspan=2, sticky="nswe")
        tkinter.Label(headFrame, textvariable=self.selectedName).pack()

        delButton = tkinter.Button(headFrame, text="删除", command=self.delItem)
        delButton.pack(side="left")
        delButton = tkinter.Button(headFrame, text="修改类别", command=self.modifyClass)
        delButton.pack(side="left")

        # 表格
        self.tree = ttk.Treeview(self, show="headings")
        self.tree["columns"] = ("ID", "类别", "名称", "描述", "所在地址", "联系电话", "邮箱")

        # 显示表头
        self.tree.heading("ID", text="ID")
        self.tree.heading("类别", text="类别")
        self.tree.heading("名称", text="名称")
        self.tree.heading("描述", text="描述")
        self.tree.heading("所在地址", text="所在地址")
        self.tree.heading("联系电话", text="联系电话")
        self.tree.heading("邮箱", text="邮箱")

        # 插入数据
        num = 1
        for item in self.list:
            self.tree.insert(
                "",
                num,
                text="",
                values=(item["id"], item["class"], item["name"], item["desc"],
                        item["address"], item["num"], item["mail"]),
            )

        # 选中行
        self.tree.bind("<<TreeviewSelect>>", self.select)

        # 排序
        for col in self.tree["columns"]:  # 给所有标题加
            self.tree.heading(
                col,
                text=col,
                command=lambda _col=col: treeviewSortColumn(
                    self.tree, _col, False
                ),
            )

        vbar = ttk.Scrollbar(self, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=vbar.set)
        self.tree.grid(row=1, column=0, sticky="nsew")
        vbar.grid(row=1, column=1, sticky="ns")

    def delItem(self):
        """点击 删除类别，删除选中的现有物品"""
        if self.selectedItem is None:
            messagebox.showinfo("提示", "请先选择需要操作的类别")
        else:
            messagebox.showinfo("删除物品？", self.selectedItem)  # 弹出消息提示框
            manageDB.delItem(self.selectedItem["values"][2])
            self.initPage()

    def modifyClass(self):
        """修改选中物品的所属类别"""
        if self.selectedItem is None:
            messagebox.showinfo("提示", "请先选择需要操作的类别")
        else:
            page = tkinter.Toplevel()
            page.title("修改类别")
            page.resizable(False, False)
            setWindowCenter(page, 400, 100)

            tkinter.Label(page, text="请选择新的物品类别：").grid(row=1, stick="w", pady=10)
            claBox = ttk.Combobox(page, textvariable=self.newCla)
            # 读取现有所有类别的名称和对应描述
            claInfo = manageDB.classList()
            claList = []
            for cla in claInfo:
                claList.append(cla["name"])
            claBox['value'] = claList
            claBox.grid(row=1, column=1)

            tkinter.Button(page, text="确定", command=self.doModify).grid(row=2, column=1)
            tkinter.Button(page, text="取消", command=page.destroy).grid(row=2, column=2)

    def doModify(self):
        """用户确定修改后，更新数据库"""
        cla = self.newCla.get()
        if cla == "":
            messagebox.showinfo("失败", "请选择修改后的物品类别")
        else:
            name = self.selectedItem["values"][2]
            db = manageDB.ItemDB()

            db.cursor.execute("UPDATE items SET class=? WHERE Name=?", (cla, name))
            db.conn.commit()

            messagebox.showinfo("成功", "物品类别修改成功")
            self.initPage()

