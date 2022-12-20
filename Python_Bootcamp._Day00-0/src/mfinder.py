import sys


def check_m(image):
    if image.count('*') != 9:
        print("False")
    elif image[0] == image[-1] == image[-3] == '*' and \
            image[4:7] == image[8:11] == 3 * '*':
        print("True")
    else:
        print("False")

if len(sys.argv) == 1:
    image = ""
    for i, line in enumerate(sys.stdin):
        if i > 2 or len(line.rstrip()) != 5:
            print("Error")
            sys.exit()
        image += (line.rstrip())
    check_m(image)
else:
    print("Usage: mfinder.py need file")
