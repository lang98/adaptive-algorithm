from grid import grid
from helper import get_start_end
from collections import deque

def solve():
    M, N = len(grid), len(grid[0])
    start_node, end_node = get_start_end()
    start_m, start_n = start_node
    Q = deque([(start_m, start_n, [])])
    visited = [[False]*N for _ in range(M)]

    while Q:
        m, n, p = Q.pop()
        visited[m][n] = True
        for (x, y) in [(m-1, n),(m, n-1),(m+1, n),(m, n+1)]:
            if x >= 0 and y >= 0 and x < M and y < N:
                if grid[x][y] == 2:
                    return p + [(x,y)]
                if grid[x][y] == 0 and not visited[x][y]:
                    Q.append((x, y, p + [(x,y)]))
                    
    return -1

res = solve()
print(res, len(res))
