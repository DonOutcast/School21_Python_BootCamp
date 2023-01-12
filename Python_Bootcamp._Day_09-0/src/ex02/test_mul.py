from itertools import tee
from random import choices
from multiply import mul
import time


def mul_python(a, b):
    b_iter = tee(zip(*b), len(a))
    return [
        [
            sum(ele_a * ele_b for ele_a, ele_b in zip(row_a, col_b))
            for col_b in b_iter[i]
        ] for i, row_a in enumerate(a)
    ]


def create_random_martix(rows, collumns):
    return [choices(range(0, 1000), k=collumns) for _ in range(rows)]


if __name__ == '__main__':
    print('TEST 1 Matrix[1,1]')
    fisrt = create_random_martix(1, 1)
    second = create_random_martix(1, 1)
    start = time.monotonic()
    mul_python(fisrt, second)
    finish = time.monotonic()
    print(f'Speed Python function: {finish - start} seconds')
    start = time.monotonic()
    mul(fisrt, second)
    finish = time.monotonic()
    print(f'Speed Cython function: {finish - start} seconds')
    # ----------------------------------------------------------------
    print('TEST 2 Matrix[2,2]')
    fisrt = create_random_martix(2, 2)
    second = create_random_martix(2, 2)
    start = time.monotonic()
    mul_python(fisrt, second)
    finish = time.monotonic()
    print(f'Speed Python function: {finish - start} seconds')
    start = time.monotonic()
    mul(fisrt, second)
    finish = time.monotonic()
    print(f'Speed Cython function: {finish - start} seconds')
    # ----------------------------------------------------------------
    print('TEST 3 Matrix[5,5]')
    fisrt = create_random_martix(5, 5)
    second = create_random_martix(5, 5)
    start = time.monotonic()
    mul_python(fisrt, second)
    finish = time.monotonic()
    print(f'Speed Python function: {finish - start} seconds')
    start = time.monotonic()
    mul(fisrt, second)
    finish = time.monotonic()
    print(f'Speed Cython function: {finish - start} seconds')
    # ----------------------------------------------------------------
    print('TEST 4 Matrix[10,10]')
    fisrt = create_random_martix(10, 10)
    second = create_random_martix(10, 10)
    start = time.monotonic()
    mul_python(fisrt, second)
    finish = time.monotonic()
    print(f'Speed Python function: {finish - start} seconds')
    start = time.monotonic()
    mul(fisrt, second)
    finish = time.monotonic()
    print(f'Speed Cython function: {finish - start} seconds')
    # ----------------------------------------------------------------
    print('TEST 5 Matrix[50,50]')
    fisrt = create_random_martix(50, 50)
    second = create_random_martix(50, 50)
    start = time.monotonic()
    mul_python(fisrt, second)
    finish = time.monotonic()
    print(f'Speed Python function: {finish - start} seconds')
    start = time.monotonic()
    mul(fisrt, second)
    finish = time.monotonic()
    print(f'Speed Cython function: {finish - start} seconds')
    # ----------------------------------------------------------------
    print('TEST 5 Matrix[100,100]')
    fisrt = create_random_martix(100, 100)
    second = create_random_martix(100, 100)
    start = time.monotonic()
    mul_python(fisrt, second)
    finish = time.monotonic()
    print(f'Speed Python function: {finish - start} seconds')
    start = time.monotonic()
    mul(fisrt, second)
    finish = time.monotonic()
    print(f'Speed Cython function: {finish - start} seconds')
