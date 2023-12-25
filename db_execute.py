import sqlite3


def create_database():
    # 建立與資料庫的連接（如果不存在則會被創建），'example.db'是資料庫文件的名稱
    conn = sqlite3.connect('AS3_data.db')

    # 創建一個游標對象cursor → 可以用來存取每一個對資料庫的查詢/處理後的紀錄，且後續可以針對cursor進行各種操作，譬如修改數據、檢查數據
    cursor = conn.cursor()

    # 建立一個資料表
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS articles (
    id INTEGER PRIMARY KEY, 
    title TEXT, 
    content TEXT, 
    url TEXT)
    ''')

    # 提交變更並關閉連接
    conn.commit()
    conn.close()


def insert_data():
    # 建立與資料庫的連接（如果不存在則會被創建），'example.db'是資料庫文件的名稱
    conn = sqlite3.connect('AS3_data.db')

    # 創建一個游標對象cursor → 可以用來存取每一個對資料庫的查詢/處理後的紀錄，且後續可以針對cursor進行各種操作，譬如修改數據、檢查數據
    cursor = conn.cursor()
    # 插入一筆資料
    # 這裡使用了參數化查詢，以防止SQL注入攻擊。→GPT給的參考但我沒有很懂這個
    cursor.execute("INSERT INTO articles (title, content, url) VALUES (?, ?, ?)",
                   ('Article Title', 'Article Content', 'Article URL'))

    # 用來確認修改後的模樣
    cursor.execute("SELECT * FROM articles")
    print(cursor.fetchall())  # fetchall() 獲取查詢結果的所有資料，並輸出成列表形式。

    # 提交變更並關閉連接
    conn.commit()
    conn.close()


if __name__ == '__main__':
    create_database()
    insert_data()

