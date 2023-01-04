import grpc
import names
import ships_pb2
import ships_pb2_grpc
from concurrent import futures
from random import randint, uniform


def create_ships():
    ship_value = ships_pb2.SpaceShip()
    ship_value.alignment = randint(0, 1)
    if ship_value.alignment == 0:
        ship_value.name = f'Ship_{names.get_first_name()}'
    ship_value.class_ship = randint(0, 5)
    ship_value.length = int(round(uniform(80.0, 20_000.0), 1))
    ship_value.crew_size = randint(4, 500)
    ship_value.armed = randint(0, 1)
    list_officer = list()
    range_officers = ('Officer Cadet',
                      'Second Lieutenant',
                      'Lieutenant',
                      'Captain',
                      'Major')
    if ship_value.alignment == 1:
        officer_range = randint(1, 10)
    else:
        officer_range = randint(0, 10)
    for _ in range(officer_range):
        officer_value = ship_value.Officers()
        officer_value.first_name = names.get_first_name()
        officer_value.last_name = names.get_last_name()
        officer_value.rank = range_officers[randint(0, 4)]
        list_officer.append(officer_value)
    print('RESPONSE')
    result_value = {
        'alignment': ship_value.alignment,
        'name': ship_value.name,
        'class_ship': ship_value.class_ship,
        'length': ship_value.length,
        'crew_size': ship_value.crew_size,
        'armed': ship_value.armed,
        'officers': list_officer
    }
    return result_value


class MyUnaryService(ships_pb2_grpc.UnaryServicer):
    def GetServerResponse(self, request, context):
        while True:
            yield ships_pb2.SpaceShip(**create_ships())


def main():
    try:
        server = grpc.server(futures.ThreadPoolExecutor(max_workers=5))
        ships_pb2_grpc.add_UnaryServicer_to_server(MyUnaryService(), server)
        server.add_insecure_port('[::]:50051')
        print('Server Started')
        server.start()
        server.wait_for_termination()
    except KeyboardInterrupt:
        print()


if __name__ == '__main__':
    main()
