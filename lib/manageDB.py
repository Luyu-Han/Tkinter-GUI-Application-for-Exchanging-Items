from lib.sqliteDB import UserDB, NewUserDB, ItemDB, AdminDB, ClassDB


# loginName,loginPass用于普通用户登录软件，addRegistrant为新用户注册
def loginName(name):
    """用户登录时验证用户名，查验用户名是否存在"""
    if name is None:
        return False
    else:
        db = UserDB()
        if db.checkUserName(name):
            return True
        else:
            return False


def loginPass(name, password):
    """用户登录时验证用户名与密码是否存在及对应，与loginName配合使用"""
    if name is None or password is None:
        return False
    else:
        db = UserDB()
        if db.checkUserPassword(name, password):
            return True
        else:
            return False


def addRegistrant(name, pw, num, address):
    """将新注册者信息添加到NewUserDB中，待管理员审核"""
    if name == "" or pw == "" or num == "" or address == "":
        return False
    db = NewUserDB()
    return db.addNewUser(name, pw, num, address)


# loginAdminName, loginAdminPass用于登入管理员账户
def loginAdminName(name):
    """用户登录时验证用户名，查验用户名是否存在"""
    if name is None:
        return False
    else:
        db = AdminDB()
        if db.checkAdminName(name):
            return True
        else:
            return False


def loginAdminPass(name, password):
    """用户登录时验证用户名与密码是否存在及对应，与loginName配合使用"""
    if name is None or password is None:
        return False
    else:
        db = AdminDB()
        if db.checkAdminPassword(name, password):
            return True
        else:
            return False


# delRegistrant，addUser用于管理员的用户准入与删除，list显示全部信息便于管理
def delRegistrant(name):
    """将已审核的无效注册用户从NewUserDB中移除"""
    db = NewUserDB()
    db.delNewUser(name)


def addUser(name, pw, num, address):
    """管理员审核后，将有效注册用户信息从NewUserDB移入UserDB"""
    db1 = NewUserDB()
    db2 = UserDB()
    db1.delNewUser(name)
    db2.addUser(name, pw, num, address)


def delUser(name):
    db = UserDB()
    db.delUser(name)


def registrantList():
    db = NewUserDB()
    return db.getAll()


def userList():
    db = UserDB()
    return db.getAll()


# 管理员设置新的物品类型，修改物品类型
def addClass(cla, desc):
    if cla == "" or desc == "":
        return False
    db = ClassDB()
    return db.addClass(cla, desc)


def classList():
    db = ClassDB()
    return db.getAll()


def delClass(name):
    db = ClassDB()
    db.delClass(name)


def addAdmin(name, password):
    if name == "" or password == "":
        return False
    db = AdminDB()
    return db.addNewAdmin(name, password)


# 普通用户增加物品信息（需先选择类型），查找物品信息（先确定类型，再关键字查询）,显示物品列表
def addItem(cla, name, desc, address, num, mail):
    if cla == "" or name == "" or desc == "" or address == "" or num == "":
        return False
    db = ItemDB()
    return db.addItem(cla, name, desc, address, num, mail)


def itemList():
    db = ItemDB()
    return db.getAll()


def delItem(name):
    db = ItemDB()
    db.delItem(name)


def searchClass(cla):
    db = ItemDB()
    return db.searchClass(cla)
