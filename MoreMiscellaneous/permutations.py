array = [0,1,2] # 3! = 6
"""
        0 1 2 
        0 2 1
        1 0 2
        1 2 0 
        2 0 1
        2 1 2
"""
array2 =    [0,1,2,3] # 4! = 24
"""
            0 1 2 3
            0 1 3 2
            0 2 1 3
            0 2 3 1
            0 3 1 2
            0 3 2 1
            1 0 2 3
            1 0 3 2
            1 2 0 3
            1 2 3 0
            1 3 0 2
            1 3 2 0
            2 0 1 3
            2 0 3 1
            2 1 0 3
            2 1 3 0
            2 3 0 1
            2 3 1 0
            3 0 1 2
            3 0 2 1
            3 1 0 2
            3 1 2 0
            3 2 0 1
            3 2 1 0
"""

def permutationPositions(length: int, pos: list = []) -> list[list]:
    if len(pos) == length:
        return [pos]
    else:
        result = []
        for i in range(length):
            if i not in pos:
                result += permutationPositions(length, pos + [i])
        return result
    
def permutation(array: list) -> list[list]:
    # print(permutationPositions(len([1,2,3,4])))
    return [[[1,2,3,4][j] for j in i] for i in permutationPositions(len([1,2,3,4]))]

permutation(array)