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


def main():
    top_msg = """===== Welcome to CRM Application =====
[S]how: Show all users info
[A]dd: Add new user
[Q]uit: Quit The Application
======================================"""

    print(top_msg)

    init_db()

    while True:
        print()
        command = input("Your command > ")
        if command == "S":
            if not find_all_users():
                print("No users")
            else:
                for user in find_all_users():
                    print(f"Name: {user[0]} Age: {user[1]}")
        elif command == "A":
            name = input("New user name > ")
            age = input("New user age > ")
            register_user(name, age)
            print(f"Add new user: {name}")
        elif command == "Q":
            print(f"Bye!")
            break
        else:
            print(f"{command}: command not found")


if __name__ == "__main__":
    main()
