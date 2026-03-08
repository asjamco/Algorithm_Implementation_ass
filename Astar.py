import heapq

# ─────────────────────────────────────────────
# EXAMPLE 1: Weighted Terrain Grid
# 1 = Road (Cost: 1), 5 = Forest (Cost: 5), 9 = Swamp (Cost: 9)
# ─────────────────────────────────────────────

def astar_weighted(grid, start, goal):
    rows, cols = len(grid), len(grid[0])
    
    def heuristic(a, b):
        # Manhattan distance
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    open_set = []
    heapq.heappush(open_set, (0, start))
    came_from = {}
    g_score = {start: 0}

    while open_set:
        _, current = heapq.heappop(open_set)

        if current == goal:
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.append(start)
            return path[::-1], g_score[goal]

        r, c = current
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols:
                # The 'weight' is the value in the grid
                weight = grid[nr][nc]
                tentative_g = g_score[current] + weight

                if (nr, nc) not in g_score or tentative_g < g_score[(nr, nc)]:
                    came_from[(nr, nc)] = current
                    g_score[(nr, nc)] = tentative_g
                    f = tentative_g + heuristic((nr, nc), goal)
                    heapq.heappush(open_set, (f, (nr, nc)))

    return None, float('inf')

print("\n" + "=" * 55)
print("  A* ALGORITHM — EXAMPLE 1: Weighted Terrain (RTS Path)")
print("=" * 55)

# Map: 1=Easy, 5=Medium, 9=Hard (Swamp)
terrain_map = [
    [1, 1, 1, 9, 1],
    [1, 9, 1, 9, 1],
    [1, 9, 1, 1, 1],
    [1, 9, 9, 9, 1],
    [1, 1, 1, 1, 1],
]

start_pos = (0, 0)
goal_pos  = (0, 4)
path, total_cost = astar_weighted(terrain_map, start_pos, goal_pos)

if path:
    print(f"\n  Start: {start_pos} → Goal: {goal_pos}")
    print(f"  Path taken avoids the swamp (9s) where possible.")
    print(f"  Total Movement Cost: {total_cost}")
    # Visualizing path with 'X'
    for r, row in enumerate(terrain_map):
        line = "  "
        for c, val in enumerate(row):
            if (r, c) == start_pos: line += "S "
            elif (r, c) == goal_pos: line += "G "
            elif (r, c) in path: line += "X "
            else: line += ". "
        print(line)

# ─────────────────────────────────────────────
# EXAMPLE 2: Word Ladder Game
# Finding the shortest transformation between words
# ─────────────────────────────────────────────

def astar_word_ladder(start, goal, word_list):
    def get_h(word, target):
        # Hamming distance: count differing letters
        return sum(1 for a, b in zip(word, target) if a != b)

    open_set = []
    heapq.heappush(open_set, (0, start))
    came_from = {}
    g_score = {start: 0}

    while open_set:
        _, current = heapq.heappop(open_set)

        if current == goal:
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.append(start)
            return path[::-1]

        # Find "neighbors" (words that differ by 1 letter)
        for word in word_list:
            if get_h(current, word) == 1:
                tentative_g = g_score[current] + 1
                if word not in g_score or tentative_g < g_score[word]:
                    came_from[word] = current
                    g_score[word] = tentative_g
                    f = tentative_g + get_h(word, goal)
                    heapq.heappush(open_set, (f, word))

    return None

print("\n" + "=" * 55)
print("  A* ALGORITHM — EXAMPLE 2: Word Ladder")
print("=" * 55)

words = ["COLD", "CORD", "CARD", "WARD", "WARM", "WORM", "WORD", "BOLD", "BARK"]
start_w = "COLD"
goal_w  = "WARM"

ladder = astar_word_ladder(start_w, goal_w, words)

if ladder:
    print(f"\n  Transformation: {' → '.join(ladder)}")
    print(f"  Steps: {len(ladder) - 1}")
else:
    print("  No transformation found.")