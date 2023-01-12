import json
import random
import names
from random import randint
from load_map import Direction
from collections import defaultdict

DATABASE_PLAYER = 'player_database.json'
DATABASE_NPC = 'npc_database.json'
DATABASE_ENEMY = 'enemy_database.json'
DATABASE_LOCATION = 'location_database.json'
DATABASE_QUESTION = 'dialog_database.json'


class Protagonist(object):
    """
    Класс Protagonist
    """

    def __init__(self, dict_value: dict = None):
        """
        Конструктор класса Protagonist
        :param dict_value:
        """
        if dict_value is None:
            dict_value = {
                "id": random.randint(0, 100),
                "name": names.get_first_name(),
                "description": "The simple warrior",
                "home": "Tortuga",
                "inventory": [{"Axe": 1}, {"Knife": 1}, {"Gun": 1}, {"Coins": 4}]
            }
        self.hp: int = 10
        self.craft: int = 1
        self.strength: int = 1
        self.backpack: int = 5
        self.id: int = dict_value['id']
        self.name: str = dict_value['name']
        self.description = dict_value['description']
        self.home = dict_value['home']
        self.inventory = defaultdict(int)
        [self.inventory.update(tmp_value)
         for tmp_value in dict_value['inventory']]

    def talk_to(self, npc):
        """
        Метод разговора с NPC (не игровой персонаж)
        :param npc:
        :return:
        """
        return npc.question

    def attack(self, enemy):
        """
        Метод атаки противника
        :param enemy:
        :return:
        """
        hit_value = randint(1, 6) + self.strength
        enemy.take_hit(hit_value)

    def take_hit(self, value=1):
        """
        Метод получения повреждения во время сражения
        :param value:
        :return:
        """
        self.hp -= value
        if self.hp == 0:
            raise Exception("You died")

    def heal(self, value=1):
        """
        Метод восстановления одной единицы здоровья
        :param value:
        :return:
        """
        self.hp += value

    def advance_strength(self, value=1):
        """
        Метод повышения свойства/показателя силы
        :param value:
        :return:
        """
        self.strength += value

    def advance_craft(self, value=1):
        """
        Метод повышения свойства/показателя ремесла
        :param value:
        :return:
        """
        self.craft += value

    def advance_backpack(self, value=1):
        """
        Метод повышения свойства/показателя вместимости инвентаря
        :param value:
        :return:
        """
        self.backpack += value

    def give(self, npc, item: str):
        """
        Метод передачи одной единицы инвентаря NPC (не игровой персонаж)
        :param npc:
        :param item:
        :return:
        """
        if self.inventory[item] == 0:
            Exception("No this item")
        else:
            self.inventory[item] -= 1
            if self.inventory[item] == 0:
                del self.inventory[item]
            npc.receive(item)

    def receive(self, item: str):
        """
        Метод получения одной единицы инвентаря
        :param item:
        :return:
        """
        if self.backpack == self.sum_inventory():
            Exception("No place in backpack")
        else:
            self.inventory[item] += 1

    def drop(self, item: str):
        """
        Метод сброса одной единицы инвентаря
        :param item:
        :return:
        """
        if self.inventory[item] == 0:
            Exception("No this item")
        else:
            self.inventory[item] -= 1
            if self.inventory[item] == 0:
                del self.inventory[item]

    def get_inventory(self):
        """
        Метод возвращающий состав и кол-во инвентаря
        :return:
        """
        return self.inventory

    def sum_inventory(self):
        """
        Метод определяющий кол-во занятого места в инвентаре
        :return:
        """
        res_value = 0
        for value in self.inventory.values():
            res_value += value
        return res_value

    def go(self, direction: Direction, direct: int):
        """
        Метод смены локации
        :param direction:
        :param direct:
        :return:
        """
        direction.go(dict_to_json_location()[str(direct)])

    def whereami(self, direction: Direction):
        """
        Метод определения названия текущей локации
        :param direction:
        :return:
        """
        return direction.whereami()


class NPC(object):
    """
    Класс NPC (Не игровой персонаж)
    """

    def __init__(self, dict_value: dict = None):
        """
        Конструктор класса NPC
        :param dict_value:
        """
        if dict_value is None:
            dict_value = {
                "id": random.randint(0, 100),
                "name": names.get_first_name(),
                "description": str(random.randint(0, 10)) + "_quest",
                "quest": "Go to home",
                "inventory": [
                    {"Coins": 1},
                    {"blaster": 1},
                    {"knife": 1}
                ]

            }
        self.id: int = dict_value['id']
        self.name: str = dict_value['name']
        self.description = dict_value['description']
        self.quest = dict_value['quest']
        self.question = dict_to_json_question()
        self.inventory = defaultdict(int)
        [self.inventory.update(tmp_value)
         for tmp_value in dict_value['inventory']]

    def request(self):
        """
        Метод обработки запрос от основного персонажа
        Метод находится в разработке
        :return:
        """
        pass

    def receive(self, item: str):
        """
        Метод получения одной единицы инвертаря
        :param item:
        :return:
        """
        self.inventory[item] += 1

    def give(self, protagonist: Protagonist, item: str):
        """
        Метод передачи одной единицы инвертаря
        :param protagonist:
        :param item:
        :return:
        """
        if self.inventory[item] == 0:
            Exception("No this item")
        else:
            self.inventory[item] -= 1
            if self.inventory[item] == 0:
                del self.inventory[item]
            protagonist.receive(item)


class Enemy(NPC):
    """
    Класс Enemy
    """

    def __init__(self, dict_value: dict = None):
        """
        Конструктор класса Enemy
        :param dict_value:
        """
        if dict_value is None:
            dict_value = {
                "id": random.randint(0, 100),
                "name": names.get_first_name(),
                "description": "Simple_enemy"

            }
        self.hp: int = 10
        self.strength: int = 1
        self.id: int = dict_value['id']
        self.name: str = dict_value['name']
        self.description = dict_value['description']

    def attack(self, protagonist: Protagonist):
        """
        Метод атаки класса Enemy
        :param protagonist:
        :return:
        """
        if self.hp > 0:
            hit_value = randint(0, 6) + self.strength
            protagonist.take_hit(hit_value)

    def take_hit(self, value):
        """
        Метод получения удара классом Enemy
        :param value:
        :return:
        """
        if self.hp == 0:
            raise Exception("Enemy died")
        else:
            self.hp -= value
            if self.hp == 0:
                raise Exception("Enemy died")

    def give(self, protagonist: Protagonist, item: str):
        """
        Метод передачи одной единицы инвентаря
        :param protagonist:
        :param item:
        :return:
        """
        if self.inventory[item] == 0:
            Exception("No this item")
        else:
            self.inventory[item] -= 1
            if self.inventory[item] == 0:
                del self.inventory[item]
            protagonist.receive(item)


def dict_to_json_player():
    """
    Метод конвертирования json БД игрока в словарь
    :return:
    """
    with open(DATABASE_PLAYER) as json_file:
        player_dict = json.load(json_file)
        dict_value = player_dict['player']
        return dict_value


def dict_to_json_npc():
    """
        Метод конвертирования json БД NPC в словарь
        :return:
        """
    with open(DATABASE_NPC) as json_file:
        npc_dict = json.load(json_file)
        dict_value = npc_dict['npc']
        return dict_value


def dict_to_json_enemy():
    """
        Метод конвертирования json БД Злодея в словарь
        :return:
        """
    with open(DATABASE_ENEMY) as json_file:
        enemy_dict = json.load(json_file)
        dict_value = enemy_dict['enemy']
        return dict_value


def dict_to_json_location():
    """
        Метод конвертирования json БД локаций в словарь
        :return:
        """
    with open(DATABASE_LOCATION) as json_file:
        location_dict = json.load(json_file)
        dict_value = location_dict['locations']
        return dict_value


def dict_to_json_question():
    """
        Метод конвертирования json БД Диалогов в словарь
        :return:
        """
    with open(DATABASE_QUESTION) as json_file:
        question_dict = json.load(json_file)
        dict_value = question_dict['item']
        return dict_value
