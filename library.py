import pymysql
import time

class BookManager:
    def __init__(self):
        try:
            self.conn = pymysql.connect(
                host="localhost",
                user="root",
                password="root",
                database="book_db",
                charset="utf8mb4",
                autocommit=False
            )
            self.cursor = self.conn.cursor()
            print("数据库连接成功")
        except Exception as e:
            print("数据库连接失败：", e)

    def write_log(self, msg):
        now = time.strftime("%Y-%m-%d %H:%M:%S")
        with open("book_log.txt", "a", encoding="utf-8") as f:
            f.write(f"[{now}] {msg}\n")

    #添加图书信息
    def add_book(self,bname,bwriter,bkind):
        try:
            sql_add = "INSERT INTO book (book_name,writer,book_kind) VALUES (%s,%s,%s)"
            self.cursor.execute(sql_add, (bname, bwriter, bkind))
            self.conn.commit()
            print("图书添加成功")
            self.write_log(f"新增图书：图书名{bname} 并录入信息")
        except Exception as e:
            self.conn.rollback()
            print("图书添加失败！数据格式错误",e)

    #修改图书信息（不包括图书状态）
    def update_book(self,b_id,nb_name,nb_writer,nb_kind):
        try:
            sql_up = "UPDATE book SET book_name=%s,writer=%s,book_kind=%s WHERE book_id=%s"
            self.cursor.execute(sql_up,(nb_name,nb_writer,nb_kind,b_id))
            self.conn.commit()
            if self.cursor.rowcount > 0:
                print("图书信息更新成功")
                self.write_log(f"修改图书信息：图书ID{b_id}")
            else:
                print("未找到该图书")
        except Exception as e:
            self.conn.rollback()
            print("图书信息更新失败",e)
    #删除图书信息
    def delete_book(self,b_id):
        try:
            sql_delete="DELETE FROM book WHERE book_id=%s"
            self.cursor.execute(sql_delete,b_id)
            self.conn.commit()
            print("删除图书成功")
            self.write_log(f"删除图书:图书ID{b_id}")
        except Exception as e:
            self.conn.rollback()
            print("图书删除失败")

    #查看图书信息
    def check_book(self,b_id):
        try:
            sql_check="SELECT * FROM book WHERE book_id=%s"
            self.cursor.execute(sql_check,b_id)
            res=self.cursor.fetchone()
            if res:
                print("==图书信息详情==")
                print(f"图书ID：{res[0]}")
                print(f"图书名：{res[1]}")
                print(f"图书作者名：{res[2]}")
                print(f"图书种类：{res[3]}")
                print(f"图书状态：{res[4]}")
                self.write_log(f"查看图书：图书ID{b_id}")
            else:
                print("未找到该图书信息")
        except Exception as e:
            self.conn.rollback()
            print("查询失败",e)

    #查看所有图书信息
    def check_all_book(self):
        try:
            sql_check_all="SELECT * FROM book"
            self.cursor.execute(sql_check_all)
            result=self.cursor.fetchall()
            if not result:
                print("暂无图书信息")
            print("==所有图书信息列表==")
            for item in result:
                print(f"图书ID：{item[0]} |图书名：{item[1]} |图书作者名：{item[2]} |图书种类：{item[3]} |图书状态：{item[4]}")
            self.write_log("查看所有图书")
        except Exception as e:
            self.conn.rollback()
            print("查询失败",e)

    #借阅图书(修改图书状态）
    def borrow(self,b_id):
        try:
            sql_select="SELECT * FROM book WHERE book_id=%s"
            self.cursor.execute(sql_select,b_id)
            res=self.cursor.fetchone()
            if res[4]=='可借阅':
                sql_borrow="UPDATE book SET book_status='已借出' WHERE book_id=%s"
                self.cursor.execute(sql_borrow,b_id)
                print("借阅成功！")
            else:
                print("该图书已借出")
            self.write_log(f"借阅图书：图书ID{b_id}")
        except Exception as e:
            self.conn.rollback()
            print("借阅失败", e)

    #归还图书（修改图书状态）
    def return_book(self,b_id):
        try:
            sql_select="SELECT * FROM book WHERE book_id=%s"
            self.cursor.execute(sql_select,b_id)
            res=self.cursor.fetchone()
            if res[4]=='已借出':
                sql_return="UPDATE book SET book_status='可借阅' WHERE book_id=%s"
                self.cursor.execute(sql_return,b_id)
                print("归还成功！")
            else:
                print("该图书已归还，无需重复归还")
                self.write_log(f"归还图书：图书ID{b_id}")
        except Exception as e:
            self.conn.rollback()
            print("归还失败",e)

    #管理员登录
    def log_in(self,admini_id,admini_name,adpwd):
        try:
            logsql="SELECT ad_name,ad_pwd FROM admini WHERE ad_id=%s"
            self.cursor.execute(logsql,admini_id)
            result=self.cursor.fetchone()
            if result is None:
                print("管理员ID不存在")
            dbname=result[0]
            dbpwd=result[1]
            if admini_name == dbname and adpwd == dbpwd:
                self.write_log(f"管理员{admini_name}登录")
                print("密码正确")
                return True
            else:
                self.write_log("有人尝试登录管理员，失败")
                print("账号信息错误")
                return False
        except:
            self.conn.rollback()
            print("登录失败")
            return False

    # 关闭数据库连接
    def close(self):
        self.cursor.close()
        self.conn.close()
        print("数据库连接已关闭")

def main():
    sys=BookManager()
    print("===使用图书信息管理系统需要管理员权限，请登录管理员账户===")
    admini_id = int(input("请输入管理员账户ID:"))
    admini_name = input("请输入管理员姓名:")
    adpwd = input("请输入管理员账户密码:")
    if sys.log_in(admini_id, admini_name, adpwd):
        while True:
            print("欢迎进入图书管理系统")
            print(
                "1.添加图书信息\n2.更新图书信息\n3.查看图书信息\n4.查看所有图书信息\n5.借阅图书\n6.归还图书\n7.删除图书\n0.退出系统")
            choice = int(input("请输入功能编号："))
            if choice == 1:
                bname = input("请输入图书名：")
                bwriter = input("请输入图书的作者名：")
                bkind = input("请输入图书的分类：")
                sys.add_book(bname, bwriter, bkind)
            elif choice == 2:
                b_id = int(input("请输入图书ID："))
                nb_name = input("请输入新的图书名：")
                nb_writer = input("请输入新的图书作者名：")
                nb_kind = input("请输入新的图书的分类：")
                sys.update_book(b_id, nb_name, nb_writer, nb_kind)
            elif choice == 3:
                b_id = int(input("请输入图书ID："))
                sys.check_book(b_id)
            elif choice == 4:
                sys.check_all_book()
            elif choice == 5:
                b_id = int(input("请输入图书ID："))
                sys.borrow(b_id)
            elif choice == 6:
                b_id = int(input("请输入图书ID："))
                sys.return_book(b_id)
            elif choice==7:
                b_id = int(input("请输入图书ID："))
                sys.delete_book(b_id)
            elif choice == 0:
                sys.close()
                print("系统退出成功，再见！")
                break
            else:
                print("输入无效")
    else:
        print("登录失败，程序结束")
        sys.close()
        print("系统退出成功")


if __name__ == "__main__":
    main()