import random


def turrets_generator():
    values = [0, 0, 0, 0, 100]
    for i in range(4):
        val = random.randint(0, 101)
        if val < values[4]:
            values[i] += val
            values[4] -= val
    return type("Turret", (object,),
                dict(
                    neuroticism=values[0],
                    openness=values[1],
                    conscientiousness=values[2],
                    extraversion=values[3],
                    agreebleness=values[4],
                    shoot=lambda: print("Shooting"),
                    search=lambda: print("Searching"),
                    talk=lambda: print("Talking"))
                )


if __name__ == "__main__":
    temp = turrets_generator()
    temp.shoot()
    temp.search()
    temp.talk()
    print(temp.neuroticism, temp.openness, temp.conscientiousness, temp.extraversion, temp.agreebleness)
