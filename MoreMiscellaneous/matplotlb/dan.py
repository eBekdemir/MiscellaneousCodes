from random import randint
from memory_profiler import profile


@profile
def f():
    lst = [0,0,0,0,0,0,0]
    for _ in range(1000):
            rnd = randint(1,6)
            lst[0]+=1
            lst[rnd]+=1
    while True:
            if lst[1] == lst[2] == lst[3] == lst[4] == lst[5] == lst[6]:
                    break
            rnd = randint(1,6)
            lst[0]+=1
            lst[rnd]+=1
    return lst

def process() -> None:
    lst = f()

    print(lst)


if __name__=='__main__':
    process()