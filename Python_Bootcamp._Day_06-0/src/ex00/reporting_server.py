import grpc
import random
import ship_pb2
import ship_pb2_grpc
import names
from concurrent import futures

Officers = (
    "Professor",
    "Miner_foreman",
    "Attack_Aircraft",
    "Oracle",
    "Mayor",
    "Mercenary",
    "Annihilator",
    "Recruiter",
    "Laser_drill",
    "Trader"
)

Enemies = (
    "Mystic",
    "Kraken",
    "Shadow_hound",
    "Mutant",
    "Shadow",
    "Chthonian",
    "Fury",
    "Bot",
    "Ghost",
    "Reaper"
)


def initialization_ship():
    temp = {
        "first_name": random.choice(Officers),
        "last_name": names.get_last_name(),
        "rank": str(random.randint(1, 10))
    }
    ship_value = ship_pb2.SpaceShip()
    ship_value.alignment = random.randint(0, 1)
    if ship_value.alignment == 0:
        ship_value.name = f"Ship_{random.choice(Enemies)}"
        officer_range = random.randint(0, 10)
    else:
        officer_range = random.randint(1, 10)
    ship_value.class_ship = random.randint(0, 6)
    ship_value.length = round(random.uniform(80.0, 20_000.0), 1)
    ship_value.crew_size = random.randint(4, 500)
    ship_value.armed = random.randint(0, 1)
    print('chekc')
    result_value = {
        'alignment': ship_value.alignment,
        'name': ship_value.name,
        'class_ship': ship_value.class_ship,
        'length': ship_value.length,
        'crew_size': ship_value.crew_size,
        'armed': ship_value.armed,
        'officers': [temp for _ in range(officer_range)]
    }
    return result_value


class MyUnaryService(ship_pb2_grpc.UnaryServicer):
    def GetServerResponse(self, request, context):
        for _ in range(random.randint(0, 10)):
            yield ship_pb2.SpaceShip(**initialization_ship())


def main():
    try:
        server = grpc.server(futures.ThreadPoolExecutor(max_workers=5))
        ship_pb2_grpc.add_UnaryServicer_to_server(MyUnaryService(), server)
        server.add_insecure_port('[::]:8080')
        print('Server Started')
        server.start()
        server.wait_for_termination()
    except KeyboardInterrupt:
        print()


if __name__ == '__main__':
    main()
