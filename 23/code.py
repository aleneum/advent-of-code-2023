from pathlib import Path
from collections import deque


def load_file(path):
    res = []
    start = None
    with Path(path).open() as f:
        for line in f.readlines():
            res.append(list(line.strip()))
    return res


next_dirs = {
    ".": ((0, -1), (1, 0), (0, 1), (-1, 0)),
    "#": (),
    ">": ((0, 1),),
    "v": ((1, 0),),
    "<": ((0, -1),),
}


def find_way(grid):
    m = len(grid)
    n = len(grid[0])
    res = 0
    queue = deque([(0, 0, 1, set())])
    max_step = 0
    while queue:
        steps, i, j, seen = queue.popleft()
        if i == m - 1:
            res = max(res, steps)
            continue
        ds = next_dirs[grid[i][j]]
        new_seen = seen.copy()
        new_seen.add((i, j))
        for di, dj in ds:
            ni = i + di
            nj = j + dj
            if (
                0 <= ni < m
                and 0 <= nj < n
                and grid[ni][nj] != "#"
                and (ni, nj) not in seen
            ):
                queue.append((steps + 1, ni, nj, new_seen))
    return res


from collections import defaultdict


def sparse(grid):
    graph = defaultdict(dict)
    m = len(grid)
    n = len(grid[0])

    def dfs(start, cur, cost, seen):
        i, j = cur
        if i == n - 1:
            graph[start][(i, j)] = cost
            return
        nex = set()
        for di, dj in ((0, 1), (1, 0), (0, -1), (-1, 0)):
            ni = i + di
            nj = j + dj
            if (
                0 <= ni < m
                and 0 <= nj < n
                and grid[ni][nj] != "#"
                and (ni, nj) not in seen
            ):
                nex.add((ni, nj))
        if (i, j) == (19, 13):
            pass
        if len(nex) == 1:
            dfs(start, nex.pop(), cost + 1, seen | {(i, j)})
        elif len(nex) > 1:
            graph[start][(i, j)] = cost
            if (i, i) not in graph:
                for ni, nj in nex:
                    dfs((i, j), (ni, nj), 1, {(i, j)})
            graph[(i, j)][start] = cost

    dfs((0, 1), (0, 1), 0, set())
    return graph


grid = load_file("23_test.txt")
sparse(grid)
