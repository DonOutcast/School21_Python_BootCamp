import argparse
from collections import Counter


class Game(object):
    payout = {(True, True): (2, 2), (True, False): (-1, 3), (False, True): (3, -1), (False, False): (0, 0)}

    def __init__(self, matches=10):
        self.matches = matches
        self.registry = Counter()

    def play(self, player1, player2):
        for m in range(self.matches):
            response1 = player1.move()
            response2 = player2.move()
            player1.history.append(response2)
            player2.history.append(response1)
            result = self.payout[(response1, response2)]
            self.registry.update({player1.type: result[0], player2.type: result[1]})
        if player1.type in ['Detective', 'Copycat', 'Copykitten']:
            player1.clear_history()
        if player2.type in ['Detective', 'Copycat', 'Copykitten']:
            player2.clear_history()

    def top3(self):
        top_3 = self.registry.most_common(6)
        for player in top_3:
            print(player[0], player[1])


class Player(object):
    type: str

    def __init__(self):
        self.history = []

    def move(self):
        raise NotImplementedError

    def append_history(self, move):
        self.history.append(move)

    def clear_history(self):
        self.history.clear()


class Cheater(Player):
    def __init__(self):
        super().__init__()
        self.type = 'Cheater'

    def move(self):
        return False


class Grudger(Player):
    def __init__(self):
        super().__init__()
        self.type = 'Grudger'

    def move(self):
        if False not in self.history:
            return True
        else:
            return False


class Detective(Player):
    def __init__(self):
        super().__init__()
        self.type = 'Detective'

    def move(self):
        if len(self.history) in (0, 2, 3):
            return True
        elif len(self.history) == 1:
            return False
        else:
            if False in self.history:
                return self.history[-1]
            else:
                return False


class Copycat(Player):
    def __init__(self):
        super().__init__()
        self.type = 'Copycat'

    def move(self):
        if len(self.history) < 1:
            return True
        return self.history[-1]


class Cooperator(Player):
    def __init__(self):
        super().__init__()
        self.type = 'Cooperator'

    def move(self):
        return True


class Copykitten(Player):
    def __init__(self):
        super().__init__()
        self.type = 'Copykitten'

    def move(self):
        if len(self.history) < 2:
            return True
        elif (not self.history[-1]) and (not self.history[-2]):
            return False
        else:
            return True


def event_loop() -> None:
    # print(add_parse())
    players = [Detective, Copycat, Grudger, Cheater, Cooperator, Copykitten]
    game = Game(add_parse())
    for i in range(len(players)):
        for j in range(i + 1, len(players)):
            game.play(players[i](), players[j]())
    game.top3()


def add_parse() -> int:
    parse = argparse.ArgumentParser(description="For count of rounds in game")
    parse.add_argument("--integers", help="for function range",  required=False, metavar='N', type=int, default=10)
    args = parse.parse_args()
    return args.integers


if __name__ == "__main__":
    event_loop()
