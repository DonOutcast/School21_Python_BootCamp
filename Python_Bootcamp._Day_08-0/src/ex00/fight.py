import asyncio
import random

from enum import Enum, auto
from random import choice


class Action(Enum):
    HIGHKICK = auto()
    LOWKICK = auto()
    HIGHBLOCK = auto()
    LOWBLOCK = auto()


class Agent:

    def __aiter__(self, health=5):
        self.health = health
        self.actions = list(Action)
        return self

    async def __anext__(self):
        return choice(self.actions)

    async def fight(self):
        temp = Agent()
        neo = Agent()
        neo_attack_or_d = ""
        temp.__aiter__()
        neo.__aiter__()
        while temp.health:
            agent_action = await temp.__anext__()
            if agent_action is Action.HIGHKICK:
                neo_attack_or_d = "Action.HIGHBLOCK"
            elif agent_action is Action.LOWKICK:
                neo_attack_or_d = "Action.LOWBLOCK"
            elif agent_action is Action.HIGHBLOCK:
                neo_attack_or_d = "Action.LOWKICK"
                temp.health -= 1
            elif agent_action is Action.LOWBLOCK:
                neo_attack_or_d = "Action.HIGHKICK"
                temp.health -= 1
            print(f"AGENT: {agent_action}, NEO {neo_attack_or_d} AGENT Health: {temp.health}")

    async def fightmany(self, n):
        agents = {i: Agent().__aiter__() for i in range(n)}
        neo = Agent()
        neo.__aiter__()
        neo_attack_or_d = ""
        n -= 1
        keys = list(agents.keys())
        while keys:
            count = random.choice(keys)
            temp = agents[count]
            agent_action = await temp.__anext__()
            if agent_action is Action.HIGHKICK:
                neo_attack_or_d = "Action.HIGHBLOCK"
            elif agent_action is Action.LOWKICK:
                neo_attack_or_d = "Action.LOWBLOCK"
            elif agent_action is Action.HIGHBLOCK:
                neo_attack_or_d = "Action.LOWKICK"
                temp.health -= 1
            elif agent_action is Action.LOWBLOCK:
                neo_attack_or_d = "Action.HIGHKICK"
                temp.health -= 1
            if temp.health == 0 and count in keys:
                keys.pop(keys.index(count))
            print(f"AGENT {count + 1}: {agent_action} NEO {neo_attack_or_d} AGENT Health: {temp.health}")


if __name__ == "__main__":
    play = Agent()
    asyncio.run(play.fightmany(4))
