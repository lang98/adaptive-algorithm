from grid import grid
from helper import get_start_end
from queue import PriorityQueue

def solve():
    M, N = len(grid), len(grid[0])
    g_dist = [[float('inf')] * N for _ in range(M)]
    visited = [[False]*N for _ in range(M)]
    start_node, end_node = get_start_end()
    start_m, start_n = start_node

    Q = PriorityQueue()
    Q.put((0, start_m, start_n, []))
    g_dist[start_m][start_n] = 0
    
    while not Q.empty():
        prio, m, n, path = Q.get()
        visited[m][n] = True
        
        for (x, y) in [(m-1, n),(m, n-1),(m+1, n),(m, n+1)]:
            if x >= 0 and y >= 0 and x < M and y < N and not visited[x][y]:
                if grid[x][y] == 2:
                    return path + [(x, y)]
                elif grid[x][y] == 0:
                    g = g_dist[m][n] + 1
                    h = abs(x-end_node[0]) + abs(y-end_node[1])
                    if g < g_dist[x][y]:
                        g_dist[x][y] = g
                        f = g + h
                        Q.put((f, x, y, path + [(x, y)]))
        
    return -1
    
res = solve()
print(res, len(res))
