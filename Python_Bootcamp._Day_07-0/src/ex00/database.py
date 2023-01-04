import sqlite3
import logging

logging.basicConfig(level=logging.INFO, format='%(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("DonOutcast")


class Database:
    def __init__(self, path_to_db="test.db"):
        self.path_to_db = path_to_db

    @property
    def connection(self):
        return sqlite3.connect(self.path_to_db)

    def execute(self, sql_query: str, parameters: tuple = None, fetchone=False, fetchall=False, commit=False):
        connection = None
        data = None
        try:
            if not parameters:
                parameters = tuple()
            connection = self.connection
            cursor = connection.cursor()
            cursor.execute(sql_query, parameters)
            if commit:
                connection.commit()
            if fetchone:
                data = cursor.fetchone()
            if fetchall:
                data = cursor.fetchall()
        except sqlite3.Error as error:
            logger.info(f"Ошибка при подключении к Sqlite {error}")
        finally:
            if connection:
                connection.close()
                logger.info("Соединение с Sqlite закрыто")
        return data

    def create_table_questions(self):
        sql_query = """
        CREATE TABLE IF NOT EXISTS questions (
    id INTEGER PRIMARY KEY ASC AUTOINCREMENT NOT NULL ,
    description TEXT NOT NULL);
    """
        logger.info("Таблица Sqlite сделана")
        self.execute(sql_query, commit=True)

    def create_table_answers(self):
        sql_query = """
            CREATE TABLE IF NOT EXISTS  answers (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    count_of INTEGER NOT NULL ,
    answer TEXT NOT NULL,
    id_question INTEGER NOT NULL,
    FOREIGN KEY (id_question) REFERENCES questions (id));
        """
        logger.info("Таблица Sqlite answers сделана")
        self.execute(sql_query, commit=True)

    def crete_table_right_answer(self):
        sql_query = """
            CREATE TABLE IF NOT EXISTS right_answer (
            id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL ,
            right_a INTEGER NOT NULL,
            id_right_q INTEGER NOT NULL,
            FOREIGN KEY (id_right_q) REFERENCES answers(count_of));
        """
        logger.info("Таблица Sqlite right_answer сделана")
        self.execute(sql_query, commit=True)

    def add_question(self, question: str):
        sql_query = """ INSERT INTO questions(description) VALUES (?);"""
        parameters = (question,)
        logger.info("Запись Sqlite успешна вставлена в таблицу ")
        self.execute(sql_query, parameters, commit=True)

    def add_answer(self, id_q: int, count: int, answer: str):
        sql_query = """ INSERT INTO answers(id_question, count_of, answer) VALUES (?, ?, ?);"""
        parameters = (id_q, count, answer)
        logger.info("Запись Sqlite answers успешна вставлена в таблицу ")
        self.execute(sql_query, parameters, commit=True)

    def add_right_answer(self, right: int, id_right: int):
        sql_query = """
        INSERT INTO right_answer(id_right_q, right_a) VALUES (?, ?) ;
        """
        parameters = (id_right, right)
        logger.info("Запись Sqlite right_answer успешна вставлена в таблицу ")
        self.execute(sql_query, parameters, commit=True)

    def select_all_questions(self):
        sql_query = """SELECT description FROM questions;"""
        return self.execute(sql_query, fetchall=True)

    def select_answer(self, **kwargs):
        sql_query = """SELECT answer FROM answers WHERE """
        sql_query, parameters = self.format_args(sql_query, kwargs)
        return self.execute(sql_query, parameters, fetchall=True)

    def select_right_answer(self, id_question):
        sql_query = """SELECT right_a FROM right_answer WHERE id_right_q = ?"""
        parameters = tuple(str(id_question))
        return self.execute(sql_query, parameters, fetchone=True)

    @staticmethod
    def format_args(sql_query, parameters):
        sql_query += """ AND """.join([
            f"{item} = ?" for item in parameters
        ])
        return sql_query, tuple(parameters.values())

    def select_question(self, **kwargs):
        sql_query = """SELECT * FROM answers WHERE """
        sql_query, parameters = self.format_args(sql_query, kwargs)
        return self.execute(sql_query, parameters, fetchone=True)

# temp = Database()
#
# temp.create_table_questions()
# temp.create_table_answers()
# temp.crete_table_right_answer()
# testing = temp.select_all_questions()
# temp.add_question("Кто ты воин?")
# temp.add_answer(1, 1, "da")
# temp.add_answer(1, 2, "ner")
# temp.add_answer(1, 3, "daa")
# temp.add_answer(1, 4, "date")
