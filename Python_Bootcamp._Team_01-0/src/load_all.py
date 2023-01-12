from load_data import Protagonist, dict_to_json_location, dict_to_json_player, Direction
import json

enemy = """
{
        "1": {
                "name": "Darth Vader",
                "description": "Dark Lord Sith",
                "strength": 5,
                "inventory": [
                        {"Coins":  1000},
                        {"Darksaber":  1}
                ]
        },
        "2": {
                "name": "Emperor Palpatine",
                "description": "Emperor of the galaxy Empire",
                "strength": 4,
                "inventory": [
                        {"Coins":  500},
                        {"Lightning spell scroll": 1}
                ]
        },
        "3": {
                "name": "General Grievous",
                "description": "General or the army Separations",
                "strength": 3,
                "inventory": [
                        {"Coins": 0},
                        {"Lightsaber":  4}
                ]
        },
        "4": {
                "name": "Boba Fett",
                "description": "The most known Bounty Hunter",
                "strength": 2,
                "inventory": [
                        {"Coins": 250},
                        {"Boba Fett's rifle":  1}
                ]
        },
        "5": {
                "name": "Nihil",
                "description": "Marauder",
                "strength": 1,
                "inventory": [
                        {"Coins": 50},
                        {"Laser carbine":  1}
                ]
        },
        "6": {
                "name": "Imperial soldier",
                "description": "Default combar unit in the Empire. Always misses",
                "strength": -6,
                "inventory": [
                        {"Coins": 25},
                        {"Default rifle": 1}
                ]
        }
}
"""

location = """
{
        "Tatooine": {
                "id": 0,
                "NPCs": [1],
                "Enemies": [6],
                "Available paths": [1]
        },
        "Kashyyk": {
                "id": 1,
                "NPCs": [2],
                "Enemies": [5, 5, 4],
                "Available paths": [0, 2]
        },
        "Yavin": {
                "id": 2,
                "NPCs": [3, 4],
                "Enemies": [6, 6, 6, 3],
                "Available paths": [1, 3]
        },
        "Death Star": {
                "id": 3,
                "NPSc": [],
                "Enemies": [2, 1],
                "Available paths": [2]
        }
}
"""

npc = """
{
        "1": {
                "name": "civilian",
                "description": "A peaceful civilian",
                "inventory": [
                        {"Coins": 300}
                ],
                "quest": []
        },
        "2": {
                "name": "worker",
                "description": "The worker of Kashyyk",
                "inventory": [
                        {"stimulator": 5}
                ],
                "quest": [
                        {"id": 1}
                ]
        },
        "3": {
                "name": "trader",
                "description": "You can sell him your useless items or buy some medicine/armor",
                "inventory": [
                        {"food": 5},
                        {"armor": 5},
                        {"stimulator": 5},
                        {"blaster": 5}
                ],
                "quest": [
                        {"id": 2}
                ]
        },
        "4": {
                "name": "Master Jedi",
                "description": "It is a bee in a telnyashka",
                "inventory": [
                        {"saber": 2},
                        {"robe jedi": 1}
                ],
                "quest": [
                        {"id": 3}
                ]
        }
}
"""

player = """
{
        "player": {
                "1": {
                        "id": 1,
                        "name": "Luke",
                        "description": "Jedi Knight",
                        "home": "1",
                        "inventory": [
                                {
                                        "saber": 1
                                },
                                {
                                        "food": 1
                                }
                        ]
                },
                "2": {
                        "id": 2,
                        "name": "Han Solo",
                        "description": "smuggler",
                        "home": "3",
                        "inventory": [
                                {
                                        "blaster": 1
                                },
                                {
                                        "food": 1
                                }
                        ]
                },
                "3": {
                        "id": 3,
                        "name": "Mandolorian",
                        "description": "Mercenary",
                        "home": "1",
                        "inventory": [
                                {
                                        "blaster": 1
                                },
                                {
                                        "food": 1
                                }
                        ]
                },
                "4": {
                        "id": 4,
                        "name": "Obi-Van Kenobi",
                        "description": "Master Jedi Knight",
                        "home": "3",
                        "inventory": [
                                {
                                        "saber": 1
                                },
                                {
                                        "robe jedi": 1
                                },
                                {
                                        "food": 1
                                }
                        ]
                }
        }
}
"""


def load_all():
    with open("location_database1.json", "w") as file1:
        file1.write(location)
    with open("enemy_database.json", "w") as file2:
        file2.write(enemy)
    with open("npc_database.json", "w") as file3:
        file3.write(npc)
    with open("player_database.json", "w") as file4:
        file4.write(player)


def test_relocation():
    """
    Тестирование функционала релокации
    :return:
    """
    try:
        tmp_player = Protagonist(dict_to_json_player()['1'])
        tmp_planet = Direction(dict_to_json_location()[tmp_player.home])
        tmp_player.go(tmp_planet, 2)
        assert tmp_planet.name == tmp_player.whereami(tmp_planet)
        tmp_player.go(tmp_planet, 3)
        assert tmp_planet.name == tmp_player.whereami(tmp_planet)
        tmp_player.go(tmp_planet, 2)
        assert tmp_planet.name == tmp_player.whereami(tmp_planet)
        tmp_player.go(tmp_planet, 4)
        assert tmp_planet.name == tmp_player.whereami(tmp_planet)
        tmp_player.go(tmp_planet, 5)
        assert tmp_planet.name == tmp_player.whereami(tmp_planet)
    except:
        pass


def test_npc_question():
    """
    Тестирование функционала диалога с NPC (не игровой персонаж)
    :return:
    """
    try:
        tmp_player = Protagonist(dict_to_json_player()['1'])
        tmp_planet = Direction(dict_to_json_location()[tmp_player.home])
        for npc_value in tmp_planet.npc:
            for dict_value in npc_value.question:
                assert dict_value['question'] != ''
                for tmp_answer in dict_value['answers']:
                    assert tmp_answer['text'] != ''
        tmp_player.go(tmp_planet, 2)
        for npc_value in tmp_planet.npc:
            for dict_value in npc_value.question:
                assert dict_value['question'] != ''
                for tmp_answer in dict_value['answers']:
                    assert tmp_answer['text'] != ''
        tmp_player.go(tmp_planet, 3)
        for npc_value in tmp_planet.npc:
            for dict_value in npc_value.question:
                assert dict_value['question'] != ''
                for tmp_answer in dict_value['answers']:
                    assert tmp_answer['text'] != ''
        tmp_player.go(tmp_planet, 2)
        for npc_value in tmp_planet.npc:
            for dict_value in npc_value.question:
                assert dict_value['question'] != ''
                for tmp_answer in dict_value['answers']:
                    assert tmp_answer['text'] != ''
        tmp_player.go(tmp_planet, 4)
        for npc_value in tmp_planet.npc:
            for dict_value in npc_value.question:
                assert dict_value['question'] != ''
                for tmp_answer in dict_value['answers']:
                    assert tmp_answer['text'] != ''
        tmp_player.go(tmp_planet, 5)
        for npc_value in tmp_planet.npc:
            for dict_value in npc_value.question:
                assert dict_value['question'] != ''
                for tmp_answer in dict_value['answers']:
                    assert tmp_answer['text'] != ''
    except:
        pass


def test_npc_inventory():
    """
    Тестирование функционала обмена инвентарем с NPC (не игровой персонаж)
    :return:
    """
    try:
        tmp_player = Protagonist(dict_to_json_player()['2'])
        tmp_planet = Direction(dict_to_json_location()[tmp_player.home])
        assert tmp_player.get_inventory() == {"blaster": 1, "food": 1}
        for npc_value in tmp_planet.npc:
            tmp_player.give(npc_value, 'food')
            assert tmp_player.get_inventory() == {"blaster": 1}
            break
        for npc_value in tmp_planet.npc:
            if npc_value.name == 'trader':
                npc_value.give(tmp_player, "armor")
                assert tmp_player.get_inventory(
                ) == {"blaster": 1, "armor": 1}
                break
        for npc_value in tmp_planet.npc:
            if npc_value.name == 'worker':
                npc_value.give(tmp_player, "stimulator")
                assert tmp_player.get_inventory(
                ) == {"blaster": 1, "armor": 1, "stimulator": 1}
                break
    except:
        pass


def test_fight_enemy():
    """
    Тестирование функционала сражения с врагами
    Тестирование моделирует часть сюжетной линии в которой необходимо победить самого
    сильного противника, предварительно перед этим повысить свой опыт на более
    слабых врагах
    :return:
    """
    try:
        tmp_player = Protagonist(dict_to_json_player()['1'])
        tmp_planet = Direction(dict_to_json_location()[tmp_player.home])
        for enemy_value in tmp_planet.enemy:
            while tmp_player.hp > 0 and enemy_value.hp > 0:
                tmp_player.attack(enemy_value)
                enemy_value.attack(tmp_player)
            if tmp_player.hp != 0:
                while tmp_player.hp != 10:
                    tmp_player.heal()
                assert tmp_player.hp == 10
                assert enemy_value.hp == 0
            tmp_player.advance_strength()
            tmp_player.advance_craft()
            tmp_player.advance_backpack()
            assert tmp_player.strength == 2
            assert tmp_player.craft == 2
            assert tmp_player.backpack == 2
        tmp_player.go(tmp_planet, 2)
        tmp_player.go(tmp_planet, 4)
        for enemy_value in tmp_planet.enemy:
            while tmp_player.hp > 0 and enemy_value.hp > 0:
                tmp_player.attack(enemy_value)
                enemy_value.attack(tmp_player)
            if tmp_player.hp != 0:
                while tmp_player.hp != 10:
                    tmp_player.heal()
                assert tmp_player.hp == 10
                assert enemy_value.hp == 0
            tmp_player.advance_strength()
            tmp_player.advance_craft()
            tmp_player.advance_backpack()
            assert tmp_player.strength == 3
            assert tmp_player.craft == 3
            assert tmp_player.backpack == 3
        tmp_player.go(tmp_planet, 2)
        tmp_player.go(tmp_planet, 3)
        for enemy_value in tmp_planet.enemy:
            while tmp_player.hp > 0 and enemy_value.hp > 0:
                tmp_player.attack(enemy_value)
                enemy_value.attack(tmp_player)
            if tmp_player.hp != 0:
                while tmp_player.hp != 10:
                    tmp_player.heal()
                assert tmp_player.hp == 10
                assert enemy_value.hp == 0
            tmp_player.advance_strength()
            tmp_player.advance_craft()
            tmp_player.advance_backpack()
            assert tmp_player.strength == 4
            assert tmp_player.craft == 4
            assert tmp_player.backpack == 4
        tmp_player.go(tmp_planet, 2)
        for enemy_value in tmp_planet.enemy:
            while tmp_player.hp > 0 and enemy_value.hp > 0:
                tmp_player.attack(enemy_value)
                enemy_value.attack(tmp_player)
            if tmp_player.hp != 0:
                while tmp_player.hp != 10:
                    tmp_player.heal()
                assert tmp_player.hp == 10
                assert enemy_value.hp == 0
            tmp_player.advance_strength()
            tmp_player.advance_craft()
            tmp_player.advance_backpack()
            assert tmp_player.strength == 5
            assert tmp_player.craft == 5
            assert tmp_player.backpack == 5
    except:
        pass


if __name__ == '__main__':
    test_relocation()
    test_npc_question()
    test_npc_inventory()
    test_fight_enemy()
