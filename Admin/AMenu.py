from tkinter import Menu


class AMenu:
    """管理员主界面菜单，主要功能包括用户管理（新用户审核、用户信息查看）、物品管理（物品类别增删、修改物品类型）"""

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

        # 用户管理下拉菜单
        usermenu = Menu(self.menubar, tearoff=0)
        usermenu.add_command(label="新用户审核", command=self.master.openCheckNewUser)
        usermenu.add_command(label="用户信息查看", command=self.master.openUserList)
        usermenu.add_command(label="管理员账号添加", command=self.master.openAddAdmin)

        # 物品管理下拉菜单
        itemmenu = Menu(self.menubar, tearoff=0)
        itemmenu.add_command(label="类别新增", command=self.master.openAddItemClass)
        itemmenu.add_command(label="全部类别查看", command=self.master.openClassList)
        itemmenu.add_command(label="物品类别修改", command=self.master.openModifyItemClass)

        # 将下拉菜单加到菜单
        self.menubar.add_cascade(label="用户管理", menu=usermenu)
        self.menubar.add_cascade(label="物品管理", menu=itemmenu)


