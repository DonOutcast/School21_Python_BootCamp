import load_data


class Direction(object):
    """
    Класс Direction
    """

    def __init__(self, dict_value: dict):
        """
        Конструктор класса Direction
        :param dict_value:
        """
        self.id = dict_value['id']
        self.name = dict_value['name']
        self.route = dict_value['route']
        self.description = dict_value['description']
        self.enemy = list([load_data.Enemy(load_data.dict_to_json_enemy()[tmp_value])
                           for tmp_value in dict_value['enemy']])
        self.npc = list([load_data.NPC(load_data.dict_to_json_npc()[tmp_value])
                         for tmp_value in dict_value['npc']])

    def go(self, dict_value):
        """
        Метод релокации с одной точки на другую (планету)
        :param dict_value:
        :return:
        """
        if dict_value['id'] not in self.route:
            Exception("No direction")
        else:
            self.set_description(dict_value)

    def set_description(self, dict_value: dict):
        """
        Метод перезаписи основных свойств локации на новую
        :param dict_value:
        :return:
        """
        self.id = dict_value['id']
        self.name = dict_value['name']
        self.route = dict_value['route']
        self.description = dict_value['description']
        self.enemy = list([load_data.Enemy(load_data.dict_to_json_enemy()[tmp_value])
                           for tmp_value in dict_value['enemy']])
        self.npc = list([load_data.NPC(load_data.dict_to_json_npc()[tmp_value])
                         for tmp_value in dict_value['npc']])

    def whereami(self):
        """
        Метод возвращающий текущий местонахождения (название локации)
        :return:
        """
        return self.name
