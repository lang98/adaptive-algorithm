from grid import grid

def get_start_end():
    start_node = None
    end_node = None
    for m in range(len(grid)):
        for n in range(len(grid[m])):
            if grid[m][n] == -1:
                start_node = (m, n)
            elif grid[m][n] == 2:
                end_node = (m, n)
    return (start_node, end_node)