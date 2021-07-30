import requests
import psycopg2
from psycopg2 import Error

try:
    # Подключиться к существующей базе данных
    connection = psycopg2.connect(user="postgres", password="postgres", host="localhost", port="5432", database="db1")
    cursor = connection.cursor()

    # Выполнение SQL-запроса для вставки данных в таблицу
    res = requests.get("https://mediametrics.ru/rating/index.tsv?titles")
    if res.status_code == 200:
        splits = res.text.split('\n')
        for i in range(0, len(splits)):
            v = splits[i].split('\t')
            if len(v) < 6:
                continue

            Title = str(v[1])
            Link = str(v[0])
            insert_query = "INSERT INTO news (header, link) VALUES (%s, %s)"
            val = (Title, Link)
            connection.autocommit = True
            cursor.execute(insert_query, val)
            connection.commit()
            print("1 запись успешно вставлена")
        # Получить результат
        cursor.execute("SELECT * from news")
        record = cursor.fetchall()
        print("Результат", record)


except (Exception, Error) as Error:
    print(Error)
