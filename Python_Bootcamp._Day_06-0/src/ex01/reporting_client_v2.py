import grpc
import argparse
import ships_pb2
import ships_pb2_grpc
from pydantic import BaseModel, root_validator
from google.protobuf.json_format import MessageToJson


class MyModelJson(BaseModel):
    alignment: str
    name: str
    class_ship: str
    length: float
    crew_size: int
    armed: int
    officers: list

    @root_validator
    def check_ship(cls, values):
        if values['class_ship'] == 'Corvette' \
            and 80 <= values['length'] <= 250 \
                and 4 <= values['crew_size'] <= 10 \
                and values['armed'] == 1 \
                and values['alignment'] == 'Enemy':
            return values
        if values['class_ship'] == 'Frigate' \
                and 300 <= values['length'] <= 600 \
        and  10 <= values['crew_size'] <= 15 \
            and values['armed'] == 1 \
        and values['alignment'] == 'Ally':
            return values
        if values['class_ship'] == 'Cruiser' \
                and 500 <= values['length'] <= 1000 \
        and  15 <= values['crew_size'] <= 30 \
            and values['armed'] == 1 \
        and values['alignment'] == 'Enemy':
            return values
        if values['class_ship'] == 'Destroyer' \
                and 800 <= values['length'] <= 2000 \
        and  50 <= values['crew_size'] <= 80 \
            and values['armed'] == 1 \
        and values['alignment'] == 'Ally':
            return values
        if values['class_ship'] == 'Carrier' \
                and 1000 <= values['length'] <= 4000 \
        and  120 <= values['crew_size'] <= 250 \
            and values['armed'] == 0 \
        and values['alignment'] == 'Enemy':
            return values
        if values['class_ship'] == 'Dreadnought' \
                and 5000 <= values['length'] <= 20000 \
        and  300 <= values['crew_size'] <= 500 \
            and values['armed'] == 1 \
        and values['alignment'] == 'Enemy':
            return values


class MyUnaryClient(object):

    def __init__(self):
        self.host = 'localhost'
        self.port = 50051
        self.channel = grpc.insecure_channel(f'{self.host}:{self.port}')
        self.stub = ships_pb2_grpc.UnaryStub(self.channel)

    def get_response(self,
                     args_hour, args_minute,
                     args_seconds, args_degrees,
                     args_minut, args_sec):
        response_value = {
            'cord_1': args_hour,
            'cord_2': args_minute,
            'cord_3': args_seconds,
            'cord_4': args_degrees,
            'cord_5': args_minut,
            'cord_6': args_sec
        }
        message = self.stub.GetServerResponse(
            ships_pb2.Message(**response_value))
        for message_value in message:
            message_json = MessageToJson(message_value, indent=4,
                                         preserving_proto_field_name=True,
                                         including_default_value_fields=True)
            try:
                ship_value = MyModelJson.parse_raw(message_json)
                print(ship_value.json())
            except BaseException:
                pass


def main():
    try:
        parser = argparse.ArgumentParser(description='grpc client')
        parser.add_argument("hour", type=int, help="hours.")
        parser.add_argument("minute", type=int, help="minutes.")
        parser.add_argument("seconds", type=float, help="seconds.")
        parser.add_argument("degrees", type=int, help="degrees.")
        parser.add_argument("minut", type=int, help="minutes.")
        parser.add_argument("sec", type=float, help="seconds.")
        args = parser.parse_args()
        client_value = MyUnaryClient()
        client_value.get_response(args.hour, args.minute,
                                  args.seconds, args.degrees,
                                  args.minut, args.sec)
    except BaseException:
        pass


if __name__ == '__main__':
    main()
