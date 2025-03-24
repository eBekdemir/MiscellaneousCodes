maze = [
    ['S', 0,  1,  0,  0,  0],
    [1,   0,  1,  1,  1,  0],
    [0,   0,  0,  0,  1,  0],
    [0,   1,  1,  0,  1,  0],
    [0,   1,  1,  0,  0,  'E']
]


def nextPos(currentPos: tuple[int, int], path: list) -> tuple[int, int]:
    x, y = currentPos
    
    if x < 0 or y < 0 or x >= len(maze[0]) or y >= len(maze):
        return None
    
    if maze[y][x] == 1: return None
    
    if currentPos in path: return None
    
    path.append(currentPos)
    
    if maze[y][x] == 'E': return path
    
    for next in [(x+1, y), (x-1, y), (x, y+1), (x, y-1)]:
        res = nextPos((next[1],next[0]), path)
        if res:
            return res
        
    path.pop()
    return None

nextPos((0,0),[])