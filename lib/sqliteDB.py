import os
import sqlite3
from abc import abstractmethod

import lib.GlobalVar as glv


class DB(object):
    def __init__(self):
        self.dbPath = os.path.join(glv.getVar("APP_PATH"), glv.getVar("DATA_DIR"), 'database.db')
        self.conn = sqlite3.connect(self.dbPath)
        self.cursor = self.conn.cursor()

    @abstractmethod
    def createDB(self):
        pass

    @abstractmethod
    def resetDB(self):
        pass

    @abstractmethod
    def getAll(self):
        pass


class ClassDB(DB):
    """物品类别数据库，包括类别名称、描述等信息"""

    def createDB(self):
        """创建数据库文件"""
        self.cursor.execute('''create table IF NOT EXISTS class(id INTEGER, name TEXT, desc TEXT)''')
        self.cursor.execute('''create unique index IF NOT EXISTS class_unique_index on class(name)''')
        self.conn.commit()

    def resetDB(self):
        """删除/初始化表"""
        self.cursor.execute("DROP TABLE IF EXISTS class")
        self.conn.commit()
        self.createDB()

    def addClass(self, name, desc):
        """新增类别信息"""
        name = name.strip()
        desc = desc.strip()
        info = name, desc
        try:
            self.cursor.execute('INSERT INTO class(name, desc) VALUES(?, ?)', info)
            self.conn.commit()
            return True
        except:
            return False

    def getAll(self):
        """获取所有类别的信息"""
        classInfo = []
        rows = self.cursor.execute('SELECT id, name, desc FROM class')
        for cla in rows:
            classInfo.append({
                'id': cla[0],
                'name': cla[1],
                'desc': cla[2],
            })
        return classInfo

    def delClass(self, name):
        """删除已有物品类别"""
        self.cursor.execute('DELETE FROM class WHERE name=?', (name,))
        self.conn.commit()


class ItemDB(DB):
    """物品信息数据库的建立与初始化、增删、列表显示等相关功能"""

    def createDB(self):
        """创建数据库文件"""
        self.cursor.execute('''create table IF NOT EXISTS items(id INTEGER, class TEXT, name TEXT, desc TEXT, 
                                address TEXT, num TEXT, mail TEXT)''')
        self.cursor.execute('''create unique index IF NOT EXISTS items_unique_index on items(name)''')
        self.conn.commit()

    def resetDB(self):
        """删除/初始化表"""
        self.cursor.execute("DROP TABLE IF EXISTS items")
        self.conn.commit()
        self.createDB()

    def addItem(self, cla, name, desc, address, num, mail):
        """新增物品信息"""
        cla = cla.strip()
        name = name.strip()
        desc = desc.strip()
        address = address.strip()
        num = num.strip()
        mail = mail.strip()
        info = cla, name, desc, address, num, mail
        try:
            self.cursor.execute('INSERT INTO items(class, name, desc, address, num, mail) VALUES(?, ?, ?, ?, ?, ?)', info)
            self.conn.commit()
            return True
        except:
            return False

    def getAll(self):
        """获取所有物品的信息"""
        itemInfo = []
        rows = self.cursor.execute('SELECT id, class, name, desc, address, num, mail FROM items')
        for item in rows:
            itemInfo.append({
                'id': item[0],
                'class': item[1],
                'name': item[2],
                'desc': item[3],
                'address': item[4],
                'num': item[5],
                'mail': item[6]
            })
        return itemInfo

    def searchClass(self, cla):
        """查找类别来获取物品信息"""
        res = []
        itemInfo = self.cursor.execute(
            'SELECT id, class, name, desc, address, num, mail FROM items WHERE class=?', (cla,)).fetchall()
        for info in itemInfo:
            if info is not None:
                res.append({
                    'id': info[0],
                    'class': info[1],
                    'name': info[2],
                    'desc': info[3],
                    'address': info[4],
                    'num': info[5],
                    'mail': info[6]
                })
        return res

    def delItem(self, name):
        """删除物品信息"""
        self.cursor.execute('DELETE FROM items WHERE name=?', (name,))
        self.conn.commit()


class UserDB(DB):
    """用户信息数据库的建立、初始化、增删等"""

    def createDB(self):
        """创建数据库文件"""
        self.cursor.execute('''create table IF NOT EXISTS users(id INTEGER, name TEXT, password TEXT,
                            num TEXT, address TEXT)''')
        self.cursor.execute('''create unique index IF NOT EXISTS users_unique_index on users(name)''')
        self.conn.commit()

    def resetDB(self):
        """删除/初始化表"""
        self.cursor.execute("DROP TABLE IF EXISTS users")
        self.conn.commit()
        self.createDB()

    def addUser(self, name, pw, num, address):
        """新增用户信息"""
        info = name, pw, num, address
        try:
            self.cursor.execute('INSERT INTO users(name, password, num, address) VALUES(?, ?, ?, ?)', info)
            self.conn.commit()
            return True
        except:
            return False

    def getAll(self):
        """获取所有用户信息"""
        userInfo = []
        rows = self.cursor.execute('SELECT id, name, password, num, address FROM users')
        for user in rows:
            userInfo.append({
                'id': user[0],
                'name': user[1],
                'password': user[2],
                'num': user[3],
                'address': user[4],
            })
        return userInfo

    def getUser(self, name):
        info = []
        r = self.cursor.execute(
            'SELECT id, name, password, num, address FROM content WHERE name=?',
            name).fetchone()
        if r is not None:
            info.append({
                'id': r[0],
                'name': r[1],
                'password': r[2],
                'num': r[3],
                'address': r[4]
            })
        return info

    def checkUserName(self, name):
        """通过用户名检查用户是否存在"""
        name = name.strip()
        flag = self.cursor.execute('SELECT * FROM users WHERE name=?', (name,)).fetchall()
        if not flag:
            return False
        else:
            return True

    def checkUserPassword(self, name, password):
        """检查用户名与对应密码是否存在于数据库中，与checkUserName结合使用"""
        name = name.strip()
        password = password.strip()
        info = name, password
        flag = self.cursor.execute(
            'SELECT * FROM users WHERE name=? and password=?', info).fetchall()
        if not flag:
            return False
        else:
            return True

    def delUser(self, name):
        """删除用户信息"""
        self.cursor.execute('DELETE FROM users WHERE name=?', (name,))
        self.conn.commit()


class NewUserDB(DB):
    """新注册用户的信息暂存、展示、增删等"""

    def createDB(self):
        """创建数据库文件"""
        self.cursor.execute('''create table IF NOT EXISTS newUsers(id INTEGER, name TEXT, password TEXT,
                            num TEXT, address TEXT)''')
        self.cursor.execute('''create unique index IF NOT EXISTS users_unique_index on newUsers(name)''')
        self.conn.commit()

    def resetDB(self):
        """删除/初始化表"""
        self.cursor.execute("DROP TABLE IF EXISTS newUsers")
        self.conn.commit()
        self.createDB()

    def addNewUser(self, name, pw, num, address):
        """新增新用户信息"""
        name = name.strip()
        pw = pw.strip()
        address = address.strip()
        num = num.strip()
        info = name, pw, num, address
        try:
            self.cursor.execute('INSERT INTO newUsers(name, password, num, address) VALUES(?, ?, ?, ?)', info)
            self.conn.commit()
            return True
        except:
            return False

    def getAll(self):
        """获取所有新用户的信息"""
        userInfo = []
        rows = self.cursor.execute('SELECT id, name, password, num, address FROM newUsers')
        for user in rows:
            userInfo.append({
                'id': user[0],
                'name': user[1],
                'password': user[2],
                'num': user[3],
                'address': user[4],
            })
        return userInfo

    def delNewUser(self, name):
        """删除新用户信息"""
        self.cursor.execute('DELETE FROM newUsers WHERE name=?', (name,))
        self.conn.commit()


class AdminDB(DB):
    """管理员数据库"""

    def createDB(self):
        """创建数据库文件"""
        self.cursor.execute('''create table IF NOT EXISTS admin(id INTEGER, name TEXT, password TEXT)''')
        self.cursor.execute('''create unique index IF NOT EXISTS admin_unique_index on admin(name)''')
        self.conn.commit()

    def resetDB(self):
        """删除/初始化表"""
        self.cursor.execute("DROP TABLE IF EXISTS admin")
        self.conn.commit()
        self.createDB()

    def addNewAdmin(self, name, pw):
        """新增管理员账户"""
        name = name.strip()
        pw = pw.strip()
        info = name, pw
        try:
            self.cursor.execute('INSERT INTO admin(name, password) VALUES(?, ?)', info)
            self.conn.commit()
            return True
        except:
            return False

    def getAll(self):
        """获取所有管理员账户的信息"""
        adminInfo = []
        rows = self.cursor.execute('SELECT id, name, password FROM admin')
        for admin in rows:
            adminInfo.append({
                'id': admin[0],
                'name': admin[1],
                'password': admin[2],
            })
        return adminInfo

    def delAdmin(self, name):
        """删除管理员账户"""
        self.cursor.execute('DELETE FROM admin WHERE name=?', (name,))
        self.conn.commit()

    def checkAdminName(self, name):
        """通过用户名检查用户是否存在"""
        name = name.strip()
        flag = self.cursor.execute('SELECT * FROM admin WHERE name=?', (name,)).fetchone()
        if not flag:
            return False
        else:
            return True

    def checkAdminPassword(self, name, password):
        """检查用户名与对应密码是否存在于数据库中，与checkUserName结合使用"""
        name = name.strip()
        password = password.strip()
        info = name, password
        flag = self.cursor.execute(
            'SELECT * FROM admin WHERE name=? and password=?', info).fetchall()
        if not flag:
            return False
        else:
            return True

