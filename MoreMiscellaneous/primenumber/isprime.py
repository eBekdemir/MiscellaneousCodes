__author__ = "Kömen - Enes Bekdemir | 2024"

def isPrime(number:int) -> bool:
    
    if number <= 1: return False
    elif number in [2,3]: return True
    elif number % 2 == 0: return False
    
    j = 5
    while j <= number:
        if number % j == 0 or number % (j+2) == 0 and j != number and j+2 != number:
            return False
        j += 6
        
    return True


def process() -> list:
    primes = [2, 3]
    inp = int(input('Max bound ::: '))
    if inp <= 1: return ['There is no prime!']
    elif inp == 2: return [2]
    elif inp < 5: return [2, 3]
    for num in range(5, inp + 1, 6):
        if isPrime(num): primes.append(num)
        if num + 2 <= inp and isPrime(num + 2): primes.append(num + 2)
        
    return primes


if __name__=='__main__':
    primes = process()
    print(*primes, f'\n{len(primes)}')
