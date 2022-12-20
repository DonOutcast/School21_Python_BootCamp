import typing


def my_decorator(func):
    def squeak(purse: typing.Dict[str, int]):
        print('SQUEAK')
        return func(purse)

    return squeak


@my_decorator
def empty(purse: typing.Dict[str, int]) -> typing.Dict[str, int]:
    return purse if purse else {}


@my_decorator
def add_ingot(purse: typing.Dict[str, int], ) -> typing.Dict[str, int]:
    return {"gold_ingots": purse.get("gold_ingots", 0) + 1}


@my_decorator
def get_ingot(purse: typing.Dict[str, int]) -> typing.Dict[str, int]:
    return {} if purse.get("gold_ingots", 0) - 1 < 1 else {"gold_ingots": purse.get("gold_ingots") - 1}


def split_booty(*args: typing.Dict[str, int]) -> typing.Tuple[
        typing.Dict[str, int], typing.Dict[str, int], typing.Dict[str, int]]:
    result = 0
    res = []
    for purse in args:
        result += purse.get("gold_ingots", 0)
    for i in range(3):
        temp = int(result / (3 - i))
        result -= temp
        res.append({'gold_ingots': temp})
    return res[0], res[1], res[2]


if __name__ == "__main__":
    my_dict = {"gold_ingots": 1}
    my_dict_1 = {"gold_ingots": 1}
    my_dict_2 = {"gold_ingots": 3}
    print(add_ingot(get_ingot(add_ingot(empty(my_dict)))))
    print(split_booty(my_dict, my_dict_2, my_dict_1))
