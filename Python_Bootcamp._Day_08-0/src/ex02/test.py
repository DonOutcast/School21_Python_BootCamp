import sqlite3
import redis
import json


def create_database():
    connection = sqlite3.connect(database="test_redis.db")
    cursor = connection.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users(id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL ,
        name TEXT NOT NULL);
    """)
    connection.commit()
    cursor.execute("""INSERT INTO users(name ) values('Misha')""")
    connection.commit()
    cursor.close()


def get_my_friends():
    redis_client = redis.Redis()
    cache_key = redis_client.get("my_friends")
    if cache_key is not None:
        return json.loads(cache_key)
    else:
        connection = sqlite3.connect(database="test_redis.db")
        cursor = connection.cursor()
        cursor.execute("""SELECT * FROM users;""")
        result = cursor.fetchall()
        redis_client.set("my_friends", json.dumps(result), ex=10)
        cursor.close()

    redis_client.close()

    return result


if __name__ == "__main__":
    print(get_my_friends())
