import grpc
import argparse
import ship_pb2
import ship_pb2_grpc
from google.protobuf.json_format import MessageToJson


class MyUnaryClient(object):

    def __init__(self):
        self.host = 'localhost'
        self.port = 8080
        self.channel = grpc.insecure_channel(f'{self.host}:{self.port}')
        self.stub = ship_pb2_grpc.UnaryStub(self.channel)

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
            ship_pb2.Message(**response_value))
        for tmp_value in message:
            print(MessageToJson(tmp_value, indent=4,
                                preserving_proto_field_name=True,
                                including_default_value_fields=True))


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
    except BaseException as b:
        print(b)


if __name__ == '__main__':
    main()
