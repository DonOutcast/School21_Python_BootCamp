import sys
if len(sys.argv) == 2:
	print("".join([sys.argv[1].split()[i][0] for i in range(len(sys.argv[1].split()))]))
else:
	print("Usage: decypher.py need some words")