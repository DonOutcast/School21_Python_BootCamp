import sys
import grpc
import ships_pb2
import ships_pb2_grpc
import sqlalchemy as db
from pydantic import BaseModel, root_validator
from google.protobuf.json_format import MessageToJson
from sqlalchemy import create_engine, UniqueConstraint


SQLALCHEMY_DATABASE_URL = 'postgresql+psycopg2://postgres:postgres@localhost/sqlalchemy_lymondgl'


def is_psql(ship_value):
    engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=True)
    metadata = db.MetaData()
    ship = db.Table('SpaceShip', metadata, db.Column('id', db.Integer, primary_key=True),
                    db.Column('alignment', db.String),
                    db.Column('name', db.String),
                    db.Column('class_ship', db.String),
                    db.Column('length', db.Float),
                    db.Column('crew_size', db.Integer),
                    db.Column('armed', db.Boolean),
                    db.Column('officers_first_name', db.String),
                    db.Column('officers_last_name', db.String),
                    db.Column('officers_rank', db.String),
                    UniqueConstraint('name', 'officers_first_name', 'officers_last_name', 'officers_rank'))
    metadata.create_all(engine)
    print('check')
    try:
        for tmp_value in ship_value['officers']:
            ins = ship.insert().values(
                alignment=ship_value['alignment'],
                name=ship_value['name'],
                class_ship=ship_value['class_ship'],
                length=ship_value['length'],
                crew_size=ship_value['crew_size'],
                armed=ship_value['armed'],
                officers_first_name=tmp_value['first_name'],
                officers_last_name=tmp_value['last_name'],
                officers_rank=tmp_value['rank'])
            connect = engine.connect()
            connect.execute(ins)
    except TypeError:
        pass


def find_traitors():
    engine = create_engine(SQLALCHEMY_DATABASE_URL)
    metadata = db.MetaData()
    ship = db.Table('SpaceShip', metadata, db.Column('id', db.Integer, primary_key=True),
                    db.Column('alignment', db.String),
                    db.Column('name', db.String),
                    db.Column('class_ship', db.String),
                    db.Column('length', db.Float),
                    db.Column('crew_size', db.Integer),
                    db.Column('armed', db.Boolean),
                    db.Column('officers_first_name', db.String),
                    db.Column('officers_last_name', db.String),
                    db.Column('officers_rank', db.String),
                    UniqueConstraint('name', 'officers_first_name', 'officers_last_name', 'officers_rank'))
    dict_value = dict()
    select_value = ship.select()
    connect_value = engine.connect()
    result_value = connect_value.execute(select_value)
    for row_value in result_value:
        print(row_value)
        if row_value[-3:] in dict_value and row_value[1] != dict_value[row_value[-3:]]:
            print(row_value[-3])
        else:
            dict_value[tuple(row_value[-3:])] = row_value[1]


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
        and 10 <= values['crew_size'] <= 15 \
            and values['armed'] == 1 \
        and values['alignment'] == 'Ally':
            return values
        if values['class_ship'] == 'Cruiser' \
                and 500 <= values['length'] <= 1000 \
        and 15 <= values['crew_size'] <= 30 \
            and values['armed'] == 1 \
        and values['alignment'] == 'Enemy':
            return values
        if values['class_ship'] == 'Destroyer' \
                and 800 <= values['length'] <= 2000 \
        and 50 <= values['crew_size'] <= 80 \
            and values['armed'] == 1 \
        and values['alignment'] == 'Ally':
            return values
        if values['class_ship'] == 'Carrier' \
                and 1000 <= values['length'] <= 4000 \
        and 120 <= values['crew_size'] <= 250 \
            and values['armed'] == 0 \
        and values['alignment'] == 'Enemy':
            return values
        if values['class_ship'] == 'Dreadnought' \
                and 5000 <= values['length'] <= 20000 \
        and 300 <= values['crew_size'] <= 500 \
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
        print("I am here")
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

                print(message_json)
                return dict(MyModelJson.parse_raw(message_json))
            except BaseException:
                pass


def main(argv_value):
    print(argv_value)
    try:
        if argv_value[1] == 'list_traitors':
            find_traitors()
        elif len(argv_value) == 8 and 'scan' in argv_value:
            client_value = MyUnaryClient()
            is_psql(client_value.get_response(int(argv_value[2]),
                                              int(argv_value[3]),
                                              float(argv_value[4]),
                                              int(argv_value[5]),
                                              int(argv_value[6]),
                                              float(argv_value[7])))
    except BaseException as e:
        print(e)


if __name__ == '__main__':
    main(sys.argv)
