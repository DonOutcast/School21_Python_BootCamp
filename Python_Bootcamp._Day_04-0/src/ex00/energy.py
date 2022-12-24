import itertools
from itertools import zip_longest
from typing import List

# plugs = ['plug1', 'plug2', 'plug3']
# sockets = ['socket1', 'socket2', 'socket3', 'socket4']
# cables = ['cable1', 'cable2', 'cable3', 'cable4']

plugs = ['plugZ', None, 'plugY', 'plugX']
sockets = [1, 'socket1', 'socket2', 'socket3', 'socket4']
cables = ['cable2', 'cable1', False]
def fix_wiring(plugs: list, socket: list, cables: list):

    return [f"plug {i[-1]} into {i[1]} {'using ' + i[0] if i[0] else 'without plug'}" if any(list(map(lambda x: str(x) != "None" and str(x).startswith(("socket", "cable")), i))) else "error" for i in
            itertools.zip_longest(filter(lambda x: str(x).startswith('plug'), plugs), filter(lambda x: str(x).startswith("socket"), socket),
                                  filter(lambda x: str(x).startswith("cable"), cables))]



    # return [any(list(map(lambda x: str(x) != "None" and str(x).startswith(("socket", "cable")), i))) for i in
    #         itertools.zip_longest(filter(lambda x: str(x).startswith('plug'), plugs), filter(lambda x: str(x).startswith("socket"), socket),
    #                               filter(lambda x: str(x).startswith("cable"), cables))]

    # return filter(lambda x: isinstance(x, str) and x.startswith(('socket', 'cable', 'plug')), plugs)
    # print([plugs, sockets, cables])
    # return filter(lambda x: str(x[0]).startswith("plug")
    #                               and str(x[1]).startswith("socket")
    #                               and str(x[2]).startswith("cable"),
    #               itertools.zip_longest(plugs, sockets, cables, fillvalue=''))

# print(list(list(fix_wiring(plugs, sockets, cables))[0]))
# for i in fix_wiring(plugs, sockets, cables):
#     print(list(str(i)))
print(*fix_wiring(plugs, sockets, cables), sep="\n")