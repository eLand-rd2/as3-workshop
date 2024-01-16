from sqlalchemy.orm import Session


def create(conn: Session, database, data):
    """
    在資料庫中新增資料。

    Args:
        conn: 資料庫連線物件
        database: 資料庫表的名稱
        data: 要新增的資料，字典形式，其中鍵是資料庫表的欄位名稱，值是要插入的數據

    Returns:
        新增資料的主鍵值，視資料庫表設計而定，如果沒有主鍵，可以根據實際需求調整
    """
    try:
        # 使用 conn 對象執行 SQL 語句，將資料插入資料庫表中
        # 這裡的 SQL 語句和具體的資料庫類型有關，需要根據實際情況進行調整
        columns = ', '.join(data.keys())  # 將資料字典的鍵（即資料庫表的欄位名稱）連接為字串，用逗號分隔
        values = ', '.join(['%s'] * len(data))  # 建立一個與資料數量相同的 %s 字串列表，這將用於 SQL 語句中的值部分
        query = f"INSERT INTO {database} ({columns}) VALUES ({values})"
        # 構建 SQL 插入語句，其中 {database} 是表名，{columns} 是欄位列表，{values} 是對應的值列表。
        result = conn.execute(query, tuple(data.values()))
        # 執行 SQL 插入語句，將資料插入資料庫表。tuple(data.values()) 用來將資料字典的值轉換為元組，以便傳遞給 SQL 語句。

        conn.commit()  # 提交事務
        print("資料新增成功")

        # 返回新增資料的 Primary Key，視資料庫表設計而定，if not exists，可以根據實際需求調整
        return result.lastrowid
    except Exception as e:
        # 發生錯誤時回滾事務
        conn.rollback()
        print(f"資料新增失敗: {str(e)}")
        return None
    finally:
        # 關閉資料庫連線
        conn.close()


def retrieve(conn: Session, database, filter=None):
    """
        從資料庫中檢索資料。

        Args:
            conn: 資料庫連線物件
            table_name: 資料庫表的名稱
            filter: 用於過濾資料的條件，字典形式，其中鍵是欄位名稱，值是搜尋的條件

        Returns:
            檢索到的資料，可以是列表或其他格式，根據實際需求調整
        """
    try:
        # 構建 SQL 查詢語句
        if filter:
            where_clause = 'WHERE ' + ' AND '.join([f'{key} = %s' for key in filter.keys()])
        else:
            where_clause = ''

        query = f"SELECT * FROM {database} {where_clause}"

        result = conn.execute(query).fetchall()

        # 返回查到的資料
        return result
    except Exception as e:
        print(f"資料檢索失敗: {str(e)}")
        return None


def update(conn: Session, data):
    pass


def delete(conn: Session):
    pass
