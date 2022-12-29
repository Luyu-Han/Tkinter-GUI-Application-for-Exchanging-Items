from tkinter import Menu, messagebox


class UMenu:
    """用户系统主界面，包括个人信息管理、物品交换系统"""

    def __init__(self, master):
        """初始化菜单"""
        self.master = master  # 上级
        self.root = master.root  # 主窗口
        self.initMenu()

    def initMenu(self):
        """加载菜单"""

        # 创建菜单栏
        self.menubar = Menu(self.root)

        # 将菜单栏添加到窗口
        self.root.config(menu=self.menubar)

        # 个人信息下拉菜单
        usermenu = Menu(self.menubar, tearoff=0)
        usermenu.add_command(label="个人信息查看", command=self.master.openCheckUser)
        usermenu.add_command(label="个人信息修改", command=self.master.openModifyUser)
        usermenu.add_command(label="退出登录", command=self.master.openLogout)

        # 物品交换下拉菜单
        itemmenu = Menu(self.menubar, tearoff=0)
        itemmenu.add_command(label="物品添加", command=self.master.openAddItem)
        itemmenu.add_command(label="物品查找", command=self.master.openSearchItem)
        # 物品删除、显示物品列表功能包含在物品查找中

        # 将下拉菜单加到菜单
        self.menubar.add_cascade(label="个人信息", menu=usermenu)
        self.menubar.add_cascade(label="物品交换", menu=itemmenu)
