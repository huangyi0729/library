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
            print("----------")
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
                print("----------")
                self.write_log(f"修改图书信息：图书ID{b_id}")
            else:
                print("未找到该图书")
                print("----------")
        except Exception as e:
            self.conn.rollback()
            print("图书信息更新失败",e)
    #删除图书信息
    def delete_book(self,b_id):
        try:
            sql_check = "SELECT * FROM book WHERE book_id=%s"
            self.cursor.execute(sql_check, b_id)
            res = self.cursor.fetchone()
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
                print("----------")
                return
            answer=input("确认删除该图书吗y/n")
            if answer=='y':
                sql_delete = "DELETE FROM book WHERE book_id=%s"
                self.cursor.execute(sql_delete, b_id)
                self.conn.commit()
                print("删除图书成功")
                print("----------")
                self.write_log(f"删除图书:图书ID{b_id}")
            else:
                print("取消删除成功")
                print("----------")
                return
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
                print("----------")
                self.write_log(f"查看图书：图书ID{b_id}")
            else:
                print("未找到该图书信息")
                print("----------")
        except Exception as e:
            self.conn.rollback()
            print("查询失败",e)

    #图书模糊查询
    def blurry_check_book(self):
        try:
            print("1.按书名查询\n2.按分类查询\n3.按作者查询\n0.取消查询")
            ch = int(input("请输入功能编号："))

            if ch == 1:
                keyword = input("请输入书名关键字：")
                # 模糊查询：使用 LIKE 并拼接 % 实现包含匹配
                sql = "SELECT * FROM book WHERE book_name LIKE %s"
                param = f'%{keyword}%'
                self.cursor.execute(sql, param)
                result = self.cursor.fetchall()
                if not result:
                    print("暂无相关图书信息")
                    print("----------")
                    return
                print("==========相关图书信息列表==========")
                for item in result:
                    print(f"图书ID：{item[0]:<10}图书名：{item[1]:<30}")
                    print(f"图书作者名：{item[2]:<20}")
                    print(f"图书种类：{item[3]:<10}图书状态：{item[4]:<10}")
                print("----------")
                self.write_log(f"按书名模糊查询：{keyword}")

            elif ch == 2:
                se_kind = input("请输入要查询的书籍分类：")
                sql2 = "SELECT * FROM book WHERE book_kind=%s"
                self.cursor.execute(sql2, se_kind)
                res2 = self.cursor.fetchall()
                if not res2:
                    print("暂无相关图书信息")
                    return
                print("==========相关图书信息列表==========")
                for item in res2:
                    print(f"图书ID：{item[0]:<10}图书名：{item[1]:<30}")
                    print(f"图书作者名：{item[2]:<20}")
                    print(f"图书种类：{item[3]:<10}图书状态：{item[4]:<10}")
                print("----------")
                self.write_log("按分类查询图书")

            elif ch == 3:
                se_writer = input("请输入要查询的作者名：")
                sql3 = "SELECT * FROM book WHERE writer=%s"
                self.cursor.execute(sql3, se_writer)
                res3 = self.cursor.fetchall()
                if not res3:
                    print("暂无相关图书信息")
                    return
                print("==========相关图书信息列表==========")
                for item in res3:
                    print(f"图书ID：{item[0]:<10}图书名：{item[1]:<30}")
                    print(f"图书作者名：{item[2]:<20}")
                    print(f"图书种类：{item[3]:<10}图书状态：{item[4]:<10}")
                print("----------")
                self.write_log("按作者查询图书")

            elif ch == 0:
                return
            else:
                print("输入无效")
                print("----------")
                return

        except Exception as e:
            self.conn.rollback()
            print("模糊查询失败", e)


    #查看所有图书信息
    def check_all_book(self):
        try:
            self.cursor.execute("SELECT * FROM book")
            result = self.cursor.fetchall()
            if not result:
                print("暂无图书信息")
                return
            print("==========所有图书信息列表==========")
            for item in result:
                print(f"图书ID：{item[0]:<10}图书名：{item[1]:<30}")
                print(f"图书作者名：{item[2]:<20}")
                print(f"图书种类：{item[3]:<10}图书状态：{item[4]:<10}")
            self.write_log("查看所有图书")
            print("----------")
        except Exception as e:
            self.conn.rollback()
            print("查询失败", e)

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
                print("----------")
                self.conn.commit()
            else:
                print("该图书已借出")
                print("----------")
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
                print("----------")
                self.conn.commit()
            else:
                print("该图书已归还，无需重复归还")
                print("----------")
                self.write_log(f"归还图书：图书ID{b_id}")
        except Exception as e:
            self.conn.rollback()
            print("归还失败",e)

    #登录账号
    def log_in(self,u_id,u_name,u_pwd):
        try:
            logsql="SELECT * FROM users WHERE user_id=%s"
            self.cursor.execute(logsql,u_id)
            result=self.cursor.fetchone()
            if result is None:
                print("不存在该账户")
                return None
            dbname=result[1]
            dbpwd=result[2]
            dbidentity=result[3]
            if u_name == dbname and u_pwd == dbpwd:
                self.write_log(f"用户{u_name}登录")
                print("密码正确")
                print("----------")
                return dbidentity
            else:
                self.write_log("有人尝试登录，失败")
                print("账号信息错误")
                print("----------")
                return None
        except:
            self.conn.rollback()
            print("登录失败")
            print("----------")
            return None

    #注册账号
    def create_user(self, new_id, new_name, new_pwd):
        # 先检查账号ID是否已存在
        check_sql = "SELECT user_id, user_name FROM users WHERE user_id=%s OR user_name=%s"
        self.cursor.execute(check_sql, (new_id, new_name))
        exist = self.cursor.fetchone()
        if exist:
            if exist[0] == new_id:
                print("注册失败：该管理员ID已被使用！")
                print("----------")
            elif exist[1] == new_name:
                print("注册失败：该管理员姓名已被注册！")
                print("----------")
            return

        # 无重复，执行插入
        try:
            insert_sql = "INSERT INTO users(user_id, user_name, user_pwd) VALUES(%s, %s, %s)"
            self.cursor.execute(insert_sql, (new_id, new_name, new_pwd))
            self.conn.commit()
            print("注册成功！请使用新账号登录。")
            print("----------")
            self.write_log(f"新增账户：ID={new_id} 姓名={new_name}")
            return
        except Exception as e:
            self.conn.rollback()
            print("注册失败，数据库错误：", e)
            return

    # 关闭数据库连接
    def close(self):
        self.cursor.close()
        self.conn.close()
        print("数据库连接已关闭")

def student_system(sys):
    while True:
        print("欢迎进入图书管理系统")
        print("1.根据图书ID查询图书信息\n2.根据书名、分类、作者查询图书信息\n3.查看所有图书信息\n4.借阅图书\n5.归还图书\n0.退出系统")
        choice = int(input("请输入功能编号："))
        if choice == 1:
            b_id = int(input("请输入图书ID："))
            sys.check_book(b_id)
        elif choice == 2:
            sys.blurry_check_book()
        elif choice == 3:
            sys.check_all_book()
        elif choice == 4:
            b_id = int(input("请输入图书ID："))
            sys.borrow(b_id)
        elif choice == 5:
            b_id = int(input("请输入图书ID："))
            sys.return_book(b_id)
        elif choice == 0:
            sys.close()
            print("系统退出成功，再见！")
            break
        else:
            print("输入无效")
def admini_system(sys):
    while True:
        print("欢迎进入图书管理系统")
        print(
            "1.添加图书信息\n2.更新图书信息\n3.根据图书ID查询图书信息\n4.模糊查询图书信息\n5.一键查询所有图书信息\n6.借阅图书\n7.归还图书\n8.删除图书\n0.退出系统")
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
        elif choice==4:
            sys.blurry_check_book()
        elif choice == 5:
            sys.check_all_book()
        elif choice == 6:
            b_id = int(input("请输入图书ID："))
            sys.borrow(b_id)
        elif choice == 7:
            b_id = int(input("请输入图书ID："))
            sys.return_book(b_id)
        elif choice == 8:
            b_id = int(input("请输入图书ID："))
            sys.delete_book(b_id)
        elif choice == 0:
            sys.close()
            print("系统退出成功，再见！")
            break
        else:
            print("输入无效")

def main():
    sys = BookManager()
    print("===使用图书信息管理系统需要登录===")
    u_id = int(input("请输入账户ID:"))
    u_name = input("请输入姓名:")
    u_pwd = input("请输入账户密码:")
    user_identity = sys.log_in(u_id, u_name, u_pwd)
    if user_identity == '管理员':
        admini_system(sys)
    elif user_identity == '学生':
        student_system(sys)
    else:
        print("检测到登录失败，是否注册账户（新注册账户默认为学生身份）y/n")
        ans =input("您的选择是：")
        if ans == 'y':
            new_id = int(input("请输入账户ID:"))
            new_name=input("请输入姓名:")
            new_pwd = input("请输入账户密码:")
            sys.create_user(new_id,new_name,new_pwd)
            main()
        else:
            sys.close()
            print("系统退出成功")

if __name__ == "__main__":
    main()
