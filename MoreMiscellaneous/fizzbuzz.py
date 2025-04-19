def fizzbuzz(number: int) -> str:
    res = ''.join(word for key, word in {3: 'Fizz', 5: 'Buzz', 7: 'Bazz'}.items() if number % key == 0)
    return res or str(number)

for i in range(1,501): 
    print(i, '->', fizzbuzz(i))