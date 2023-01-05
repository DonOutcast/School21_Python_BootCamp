import re
import random
from .database import Database


def initialization_database() -> Database:
    """Initialization all databases

    :param file_loc: The file location of the spreadsheet
    :type file_loc: str
    :param print_cols: A flag used to print the columns to the console
        (default is False)
    :type print_cols: bool
    :returns: a list of strings representing the header columns
    :rtype: list
    """
    db = Database()
    db.create_table_questions()
    db.create_table_answers()
    db.crete_table_right_answer()
    return db


def add_questions(database_user: Database) -> None:
    questions = [
        "Сколько книг Ведьмака?",
        "Скольо книг Финансита?",
        "Кто является главным героем в романе Последний Дон?",
        "С кем срожается Ведьмак в первой главе?",
        "Полное имя Дона?",
        "Полное имя Ведьмака?",
        "Какую награду Ведьмак получил за упурицу?",
        "Кто убил Луку Брази?",
        "Как умер Джузупе Марипоза?",
        "Стал ли Мартен Иден писателем?"
    ]
    for question in questions:
        database_user.add_question(question)


def add_answers(database_user: Database) -> None:
    answers = {
        "1": [
            "3",
            "4",
            "7",
            "10",

        ],
        "2": [
            "1",
            "5",
            "4",
            "3",
        ],
        "3": [
            "Малик",
            "Сантино",
            "Лука",
            "Тоталия",
        ],
        "4": [
            "Упырица",
            "Василиск",
            "Дракон",
            "Троль",
        ],
        "5": [
            "Розатто",
            "Джузепе",
            "Алькапоне",
            "Вито",
        ],
        "6": [
            "Гарри",
            "Геральт",
            "Элидан",
            "Гулгар",
        ],
        "7": [
            "Золото",
            "Серебро",
            "3000 монет",
            "Сапфиры",
        ],
        "8": [
            "Сантино",
            "Таталья",
            "Вито",
            "Малик",
        ],
        "9": [
            "Застрелили",
            "Взорвали",
            "Задушили",
            "Утопили",
        ],
        "10": [
            "Да",
            "Нет",
            "Почти",
            "Несовсем",
        ],

    }
    for number_question, question in enumerate(answers):
        for number_answer, answer in enumerate(answers[question]):
            database_user.add_answer(number_question + 1, number_answer + 1, answer)


def add_right_answer(database_user: Database) -> None:
    right_answer = {
        "1": 3,
        "2": 4,
        "3": 1,
        "4": 1,
        "5": 4,
        "6": 2,
        "7": 3,
        "8": 2,
        "9": 3,
        "10": 1,
    }
    for number_question, right in enumerate(right_answer):
        database_user.add_right_answer(right_answer[right], number_question + 1)


def check_param(breath, heart_rate, blushing_level, pupillary_dilation):
    """Проверить введенные данные на валидность.

    Args:
        param1 (int): Параметр "дыхание"
        param2 (int): Параметр "частота сердечных сокращений"
        param3 (int): Параметр "уровень покраснения"
        param4 (int): Параметр "расширение зрачка"

    Returns:
        bool
    """
    res = True
    if breath not in range(12, 17):
        res = False
        print('Параметр "дыхание" введен неверно')
    if heart_rate not in range(60, 101):
        res = False
        print('Параметр "частота сердечных сокращений" введен неверно')
    if blushing_level not in range(1, 7):
        res = False
        print('Параметр "уровень покраснения" введен неверно')
    if pupillary_dilation not in range(2, 9):
        res = False
        print('Параметр "расширение зрачка" введен неверно')
    return res


def check_len(var):
    """Проверить количество введенных аргументов.

    Args:
        param1 (str): Вводные данные

    Returns:
        bool
    """
    res = True
    if len(var) != 4:
        print('Нужно ввести четыре параметра')
        res = False
    return res


def check_type(var):
    """Проверить тип введенных данных.

    Args:
        param1 (str): Вводные данные

    Returns:
        bool
    """
    res = True
    for i in range(len(var)):
        if re.match(r'[0-9]', var[i]):
            if not var[i].isdigit():
                res = False
                break
        else:
            res = False
    if res is False:
        print('Ошибка типа переменной, передаваемой на вход')
    return res


def get_param():
    """Прочитать данные из stdin и запустить проверку введенных данных.

    eturns:
        int: Возвращает сумму параметров
    """
    while True:
        print('Введите параметры: дыхание (12-16 вдох/мин), '
              'частота сердечных сокращений (60-100 удар/мин), '
              'уровень покраснения (6 уровней), расширение зрачка (2-8) мм')
        var = input().split()
        if check_len(var) is True and check_type(var) is True:
            breath = int(var[0])
            heart_rate = int(var[1])
            blushing_level = int(var[2])
            pupillary_dilation = int(var[3])
            if check_param(breath, heart_rate, blushing_level,
                           pupillary_dilation) is False:
                get_param()
            return breath + heart_rate + blushing_level + pupillary_dilation


def make_question(database_user: Database) -> None:
    all_questions = database_user.select_all_questions()
    right_answer_count = 0
    for count, question in enumerate(all_questions):
        print(question[-1])
        answers_of_question = database_user.select_answer(id_question=count + 1)
        counter = 0
        temp_answers = []
        for answer in answers_of_question:
            counter += 1
            print(f"{counter}. {answer[-1]}")
            temp_answers.append(answer[-1])
        random_answer = random.choice(temp_answers)
        original_right = database_user.select_right_answer(count + 1)
        print(f"Ваш Ответ {random_answer}")
        get_param()
        if original_right is not None:
            if random_answer == original_right[-1]:
                right_answer_count += 1
    if right_answer_count < 5:
        print("Yor a Replicant")
    else:
        print("Yor a Human")


def start_event_loop() -> None:
    database_user = initialization_database()
    add_questions(database_user)
    add_answers(database_user)
    add_right_answer(database_user)
    make_question(database_user)


if __name__ == "__main__":
    start_event_loop()
