import multiprocessing
import itertools

def func(x, y):
    return (x, y)

if __name__ == '__main__':

    result = multiprocessing.Pool().starmap(func, tuple(itertools.product(range(10), range(10))))
    print(result)