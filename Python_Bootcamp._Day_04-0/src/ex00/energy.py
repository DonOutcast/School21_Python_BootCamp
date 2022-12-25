import itertools

def fix_wring(cable, socket, plug):
    return map(lambda x: f"plug {x[-1]} into {x[1]} {'using ' + x[0] if x[0] else 'without plug'}" ,[p for p in itertools.zip_longest(
        [
            cab for cab in cable if str(cab).startswith("cable")
        ],
        [
            soc for soc in socket if str(soc).startswith("socket")
        ],
        [
            plg for plg in plug if str(plg).startswith("plug")
        ])

    if p[0] and p[1]])



def check_1():
    plugs = ['plugZ', None, 'plugY', 'plugX']
    sockets = [1, 'socket1', 'socket2', 'socket3', 'socket4']
    cables = ['cable2', 'cable1', False]

    print(*fix_wring(cables, sockets, plugs), sep="\n")


def check_2():
    plugs = ['plug1', 'plug2', 'plug3']
    sockets = ['socket1', 'socket2', 'socket3', 'socket4']
    cables = ['cable1', 'cable2', 'cable3', 'cable4']
    print(*fix_wring(cables, sockets, plugs), sep="\n")

if name == "main":
    print("Test_1", "*" * 29)
    check_1()
    print("Test_2", "*" * 29)
    check_2()
