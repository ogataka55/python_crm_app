import os

from dotenv import load_dotenv

import psycopg2

load_dotenv()


def init_db():
    # DBの情報を取得
    dsn = os.environ.get('DATABASE_URL')
    # print(dsn)
    # DBに接続(コネクションを貼る)
    conn = psycopg2.connect(dsn)
    cur = conn.cursor()
    # SQLを用意 # 開けたら閉める!! with文
    with open('schema.sql', encoding="utf-8") as f:
        sql = f.read()
        # SQLを実行
        cur.execute(sql)

    # 実行状態を保存
    conn.commit()
    # コネクションを閉じる
    conn.close()


def find_all_users():
    # Connectionを貼る
    dsn = os.environ.get('DATABASE_URL')
    connection = psycopg2.connect(dsn)

    cursor = connection.cursor()

    sql = "SELECT * FROM users"

    cursor.execute(sql)

    users = cursor.fetchall()

    connection.commit()

    connection.close()

    return users


# ユーザー検索関数
def find_user(name):
    # Connectionを貼る
    dsn = os.environ.get('DATABASE_URL')
    connection = psycopg2.connect(dsn)

    cursor = connection.cursor()

    # WHEREで条件を指定
    sql = "SELECT name, age FROM users WHERE name = %(name)s"

    cursor.execute(sql, {'name': name})

    users = cursor.fetchone()  # fetchone()…データを1つのみ取得

    connection.commit()

    connection.close()

    return users


def register_user(name, age):
    # DBの情報を取得
    dsn = os.environ.get('DATABASE_URL')
    # print(dsn)
    # DBに接続(コネクションを貼る)
    conn = psycopg2.connect(dsn)
    cur = conn.cursor()
    # SQLを用意 # プレースホルダー
    sql = "INSERT INTO users (name, age) VALUES (%(name)s, %(age)s)"
    # SQLを実行
    cur.execute(sql, {'name': name, 'age': age})
    # 実行状態を保存
    conn.commit()
    # コネクションを閉じる
    conn.close()


# ユーザー削除関数
def delete_user(name):
    # Connectionを貼る
    dsn = os.environ.get('DATABASE_URL')
    connection = psycopg2.connect(dsn)

    cursor = connection.cursor()

    # WHEREで条件を指定
    sql = "DELETE FROM users WHERE name = %(name)s"

    cursor.execute(sql, {'name': name})

    connection.commit()

    connection.close()


# ユーザー編集関数
def update_user(new_name, new_age, name):
    # Connectionを貼る
    dsn = os.environ.get('DATABASE_URL')
    connection = psycopg2.connect(dsn)

    cursor = connection.cursor()

    # WHEREで条件を指定
    sql = "UPDATE users SET name = %(new_name)s, age = %(new_age)s WHERE name = %(name)s"

    cursor.execute(sql, {'new_name': new_name, 'new_age': new_age, 'name': name})

    connection.commit()

    connection.close()


# バリデート関数
def validate(name, age):
    if name == "":
        print(f"User name can't be blank")
    elif age == "":
        print(f"User age can't be blank")
    elif len(name) >= 21:
        print(f"User name is too long(maximum is 20 characters)")
    # 文字列（浮動小数点) -> エラー… int(float())で回避
    elif int(float(age)) > 120 or int(float(age)) < 0:
        print(f"Age is grater than 0 less than 120")


def main():
    top_msg = """===== Welcome to CRM Application =====
[S]how: Show all users info
[A]dd: Add new user
[F]ind: 
[D]elete:
[E]dit:
[Q]uit: Quit The Application
======================================"""

    print(top_msg)

    init_db()

    while True:
        print()
        command = input("Your command > ")
        # .upper()… 小文字を大文字変換
        if command.upper() == "S":
            if not find_all_users():
                print("No users")
            else:
                for user in find_all_users():
                    print(f"Name: {user[0]} Age: {user[1]}")
        elif command.upper() == "A":
            name = input("New user name > ")
            age = input("New user age > ")
            # バリデート処理
            validate(name, age)
            # 例外処理(try-except文)… エラーをキャッチして事前処理
            try:
                register_user(name, age)
            except psycopg2.errors.UniqueViolation:  # except エラー名:
                print(f"Duplicated user name {name}")
            except psycopg2.errors.InvalidTextRepresentation:  # except エラー名:
                print(f"Age is not positive integer")
            else:
                print(f"Add new user: {name}")
        # ユーザ検索機能追加
        elif command.upper() == "F":
            name = input("User name > ")
            find_user(name)
            if not find_user(name):
                print(f"Sorry, {name} is not found")
            else:
                print(f"Name: {name} Age: {find_user(name)[1]}")
        # ユーザ削除機能追加
        elif command.upper() == "D":
            name = input("User name > ")
            find_user(name)
            if not find_user(name):
                print(f"Sorry, {name} is not found")
            else:
                delete_user(name)
                print(f"User {name} is deleted")
        # ユーザ編集機能追加
        elif command.upper() == "E":
            name = input("User name > ")
            find_user(name)
            print(find_user(name))
            if not find_user(name):
                print(f"Sorry, {name} is not found")
            else:
                new_name = input(f"New user name({name}) > ")
                new_age = input(f"New user age({find_user(name)[1]}) > ")
                update_user(new_name, new_age, name)
                print(f"Update user: {new_name}")
        elif command.upper() == "Q":
            print(f"Bye!")
            break
        else:
            print(f"{command}: command not found")


if __name__ == "__main__":
    main()
