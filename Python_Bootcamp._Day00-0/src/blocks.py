import sys
if len(sys.argv) == 2:
    for _ in range(int(sys.argv[1])):
        temp = sys.stdin.readline().strip()
        if temp[:5] == "00000" and temp[5] != "0" and len(temp) == 32:
            print(temp)
else:
    print("Usage: blocks.py need number_of_lines")



