import tkinter
from tkinter import ttk
from tkinter import messagebox

import lib.manageDB as manageDB
from lib.windows import treeviewSortColumn, setWindowCenter


class UHomeFrame(tkinter.Frame):
    """用户初始欢迎界面"""

    def __init__(self, last=None):
        tkinter.Frame.__init__(self, last)

        self.root = last
        self.initGUI()

    def initGUI(self):
        """初始显示 欢迎用户界面"""
        tkinter.Label(self, text='欢迎使用系统！').pack()
        tkinter.Label(self, text='请使用上方工具栏选择所需功能。').pack()


class CheckUser(tkinter.Frame):
    """个人信息查看界面定义及功能实现"""


class ModifyUser(tkinter.Frame):
    """个人信息修改界面定义及功能实现"""


class Logout(tkinter.Frame):
    """退出登录界面定义及功能实现"""


class AddItem(tkinter.Frame):
    """物品添加界面定义及功能实现"""

    def __init__(self, last=None):
        tkinter.Frame.__init__(self, last)
        self.root = last
        self.cla = tkinter.StringVar()
        self.claList = {}
        self.name = tkinter.StringVar()
        self.desc = tkinter.StringVar()
        self.address = tkinter.StringVar()
        self.num = tkinter.StringVar()
        self.mail = tkinter.StringVar()
        self.chooseClass()

    def chooseClass(self):
        """添加物品前首先需通过弹窗选择物品类别"""
        page = tkinter.Toplevel()
        page.title("选择类别")
        page.resizable(False, False)
        setWindowCenter(page, 400, 100)

        tkinter.Label(page, text="请先选择添加物品的类别：").grid(row=1, stick="w", pady=10)
        claBox = ttk.Combobox(page, textvariable=self.cla)
        # 读取现有所有类别的名称和对应描述
        claList = manageDB.classList()
        for cla in claList:
            self.claList[cla["name"]] = cla["desc"]
        claBox['value'] = ([*self.claList])
        claBox.grid(row=1, column=1)

        tkinter.Button(page, text="确定", command=lambda: self.initPage(page)).grid(row=2)

    def error(self):
        """未选择物品类别而直接确定的错误处理"""
        messagebox.showinfo("错误", "请先选择需添加物品的类别")
        self.chooseClass()

    def initPage(self, page):
        """加载控件,包括添加各类物品信息输入的提示及文本框"""
        if self.cla.get() == "":
            self.error()

        else:
            page.destroy()

            head_frame = tkinter.LabelFrame(self, text="物品添加")
            head_frame.grid(row=0, column=0, columnspan=2, sticky="nswe")

            tkinter.Label(self, text="名称: ").grid(row=2, stick="w", pady=10)
            name = tkinter.Entry(self, textvariable=self.name)
            name.grid(row=2, column=1, stick="we")

            tkinter.Label(self, text="描述: ").grid(row=3, stick="w", pady=10)
            desc = tkinter.Entry(self, textvariable=self.desc)
            desc.grid(row=3, column=1, stick="we")

            # 根据用户所选物品类别，给出相应信息提示
            claDesc = self.claList[self.cla.get()]
            tkinter.Label(self, text=claDesc).grid(row=4, sticky="swe")

            tkinter.Label(self, text="所在地址: ").grid(row=5, stick="w", pady=10)
            address = tkinter.Entry(self, textvariable=self.address)
            address.grid(row=5, column=1, stick="we")

            tkinter.Label(self, text="联系电话: ").grid(row=6, stick="w", pady=10)
            num = tkinter.Entry(self, textvariable=self.num)
            num.grid(row=6, column=1, stick="we")

            tkinter.Label(self, text="邮箱: ").grid(row=7, stick="w", pady=10)
            mail = tkinter.Entry(self, textvariable=self.mail)
            mail.grid(row=7, column=1, stick="we")

            addButton = tkinter.Button(self, text="添加", command=self.addItem)
            addButton.grid(row=8, column=1, stick="w", pady=10)

    def addItem(self):
        """添加物品信息至数据库"""
        cla = self.cla.get()
        name = self.name.get()
        desc = self.desc.get()
        address = self.address.get()
        num = self.num.get()
        mail = self.mail.get()
        res = manageDB.addItem(cla, name, desc, address, num, mail)
        if res is True:
            self.name.set("")
            self.desc.set("")
            self.address.set("")
            self.num.set("")
            self.mail.set("")
            messagebox.showinfo(title="成功", message="物品添加成功")
        else:
            messagebox.showinfo(title="错误", message="物品添加失败，请将类别、名称、描述、所在地址、联系电话等信息填写完整")


class SearchItem(tkinter.Frame):
    """物品查找界面定义及功能实现, 包括物品查找、全部信息显示、删除物品信息等"""
    def __init__(self, last=None):
        tkinter.Frame.__init__(self, last)
        self.root = last
        self.selectedItem = None
        self.selectedName = tkinter.StringVar()
        self.cla = tkinter.StringVar()
        self.key = tkinter.StringVar()
        self.initPage()

    def initPage(self):
        """加载物品查找界面控件，仅包括物品删除功能"""
        headFrame = tkinter.LabelFrame(self, text="物品查找")
        headFrame.grid(row=0, column=0, columnspan=3, sticky="nswe")

        tkinter.Label(headFrame, text="请选择查找物品的类别：").grid(row=1, stick="w", pady=10)
        claBox = ttk.Combobox(headFrame, textvariable=self.cla)
        # 读取现有所有类别的名称和对应描述
        claList = manageDB.classList()
        allClass = []
        for cla in claList:
            allClass.append(cla["name"])
        claBox['value'] = allClass
        claBox.grid(row=1, column=1)

        tkinter.Label(headFrame, text="请输入查找关键字：").grid(row=2, stick="w", pady=10)
        tkinter.Entry(headFrame, textvariable=self.key).grid(row=2, column=1, stick="w", pady=10)

        listButton = tkinter.Button(headFrame, text="全部物品", command=lambda: self.itemList(manageDB.itemList()))
        listButton.grid(row=3, column=0, pady=10)
        searchButton = tkinter.Button(headFrame, text="查找", command=self.search)
        searchButton.grid(row=3, column=1, pady=10)
        delButton = tkinter.Button(headFrame, text="删除", command=self.delItem)
        delButton.grid(row=3, column=2, pady=10)

        # 表格
        self.treeView = ttk.Treeview(self, show="headings")
        self.treeView["columns"] = ("ID", "类别", "名称", "描述", "所在地址", "联系电话", "邮箱")

        # 显示表头
        self.treeView.heading("ID", text="ID")
        self.treeView.heading("类别", text="类别")
        self.treeView.heading("名称", text="名称")
        self.treeView.heading("描述", text="描述")
        self.treeView.heading("所在地址", text="所在地址")
        self.treeView.heading("联系电话", text="联系电话")
        self.treeView.heading("邮箱", text="邮箱")
        self.treeView.grid(row=1, column=0, sticky="nsew")

    def select(self, event):
        """选中"""
        # event.widget获取Treeview对象，调用selection获取选择所有选中的
        slct = event.widget.selection()[0]
        self.selectedItem = self.treeView.item(slct)
        self.selectedName.set(self.selectedItem["values"][2])

    def delItem(self):
        """用户点击 删除 按钮，删除物品信息"""
        if self.selectedItem is None:
            messagebox.showinfo("提示", "请先选择需要删除的物品")
        else:
            page = tkinter.Toplevel()
            page.title("删除物品？")
            page.resizable(False, False)
            setWindowCenter(page, 400, 100)
            tkinter.Label(page, text=self.selectedItem).grid(row=1, stick="w", pady=10)

            tkinter.Button(page, text="确定", command=self.doDelete).grid(row=2)
            tkinter.Button(page, text="取消", command=page.destroy).grid(row=3)

    def doDelete(self):
        manageDB.delItem(self.selectedItem["values"][2])
        self.initPage()

    def itemList(self, info):
        """显示全部物品信息"""
        self.initPage()
        # 插入数据
        num = 1
        for item in info:
            self.treeView.insert(
                "",
                num,
                text="",
                values=(item["id"], item["class"], item["name"], item["desc"],
                        item["address"], item["num"], item["mail"]),
            )

        # 选中行
        self.treeView.bind("<<TreeviewSelect>>", self.select)

        # 排序
        for col in self.treeView["columns"]:  # 给所有标题加
            self.treeView.heading(
                col,
                text=col,
                command=lambda _col=col: treeviewSortColumn(
                    self.treeView, _col, False
                ),
            )

        vbar = ttk.Scrollbar(self, orient="vertical", command=self.treeView.yview)
        self.treeView.configure(yscrollcommand=vbar.set)
        self.treeView.grid(row=1, column=0, sticky="nsew")
        vbar.grid(row=1, column=1, sticky="ns")

    def search(self):
        """根据输入查找相关物品"""
        self.initPage()
        cla = self.cla.get()
        key = self.key.get()
        if cla == "":
            messagebox.showinfo(title="错误", message="请先选择物品所属类别。")
        elif key == "":
            self.searchClass()
        else:
            self.searchClassKey()

    def searchClass(self):
        """仅根据类别查找"""
        itemOfClass = manageDB.searchClass(self.cla.get())
        self.itemList(itemOfClass)

    def searchClassKey(self):
        """在某类别中查找物品名称、描述中所含关键字"""
        itemOfClass = manageDB.searchClass(self.cla.get())
        key = self.key.get()
        res = []
        for i in itemOfClass:
            if key in i["name"] or key in i["desc"]:
                res.append(i)
        self.itemList(res)



