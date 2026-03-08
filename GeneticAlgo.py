import random
import math

random.seed(42)  # For reproducibility


# ─────────────────────────────────────────────
# EXAMPLE 1: String Evolution
# Target: Evolve a random string to match a goal
# ─────────────────────────────────────────────

def ga_string_evolution():
    print("\n" + "=" * 58)
    print("  GENETIC ALGORITHM — EXAMPLE 1: String Evolution")
    print("  Goal: Evolve random text into 'EVOLUTIONARY AI'")
    print("=" * 58)

    TARGET = "EVOLUTIONARY AI"
    CHARSET = " ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    POP_SIZE = 100
    MUTATION_RATE = 0.02

    def fitness(individual):
        # Score = number of characters matching target at the same index
        return sum(1 for a, b in zip(individual, TARGET) if a == b)

    def mutate(individual):
        res = list(individual)
        for i in range(len(res)):
            if random.random() < MUTATION_RATE:
                res[i] = random.choice(CHARSET)
        return "".join(res)

    def crossover(p1, p2):
        point = random.randint(0, len(TARGET) - 1)
        return p1[:point] + p2[point:]

    # Initialize random population
    population = ["".join(random.choice(CHARSET) for _ in range(len(TARGET))) 
                  for _ in range(POP_SIZE)]

    generation = 0
    while True:
        generation += 1
        population = sorted(population, key=fitness, reverse=True)
        best = population[0]
        
        if generation % 20 == 0 or fitness(best) == len(TARGET):
            print(f"  Gen {generation:>4} | Best: '{best}' | Fitness: {fitness(best)}")
        
        if fitness(best) == len(TARGET):
            break

        # Generate next generation
        new_pop = population[:10] # Elitism: keep top 10
        while len(new_pop) < POP_SIZE:
            p1, p2 = random.sample(population[:50], 2) # Select from top 50
            child = mutate(crossover(p1, p2))
            new_pop.append(child)
        population = new_pop

ga_string_evolution()

# ─────────────────────────────────────────────
# EXAMPLE 2: Knapsack Problem
# Goal: Maximize value while staying under weight limit
# ─────────────────────────────────────────────

def ga_knapsack():
    print("\n" + "=" * 58)
    print("  GENETIC ALGORITHM — EXAMPLE 2: Knapsack Problem")
    print("  Constraint: Max Weight = 15kg")
    print("=" * 58)

    # (Value, Weight)
    ITEMS = [
        ("Laptop", 500, 3), ("Camera", 300, 2), ("Gold Bar", 1000, 10),
        ("Food", 200, 1),   ("Tent", 400, 5),   ("Book", 50, 0.5),
        ("First Aid", 150, 1)
    ]
    MAX_WEIGHT = 15
    POP_SIZE = 20
    GENS = 50

    def fitness(chromosome):
        total_val = 0
        total_weight = 0
        for i, bit in enumerate(chromosome):
            if bit == 1:
                total_val += ITEMS[i][1]
                total_weight += ITEMS[i][2]
        
        # Penalty: If over weight, fitness is extremely low
        return total_val if total_weight <= MAX_WEIGHT else 0

    def get_weight(chromosome):
        return sum(ITEMS[i][2] for i, bit in enumerate(chromosome) if bit == 1)

    # Initialize random population (bitstrings)
    population = [[random.randint(0, 1) for _ in range(len(ITEMS))] for _ in range(POP_SIZE)]

    for gen in range(1, GENS + 1):
        population = sorted(population, key=fitness, reverse=True)
        
        if gen % 10 == 0:
            best = population[0]
            print(f"  Gen {gen:>2} | Value: {fitness(best):>4} | Weight: {get_weight(best):>4}kg")

        # Reproduce
        new_pop = population[:4] # Elitism
        while len(new_pop) < POP_SIZE:
            p1, p2 = random.sample(population[:10], 2)
            # Simple single-point crossover
            point = random.randint(1, len(ITEMS)-1)
            child = p1[:point] + p2[point:]
            # Mutation (flip a bit)
            if random.random() < 0.1:
                idx = random.randint(0, len(ITEMS)-1)
                child[idx] = 1 - child[idx]
            new_pop.append(child)
        population = new_pop

    best_final = population[0]
    chosen = [ITEMS[i][0] for i, bit in enumerate(best_final) if bit == 1]
    print(f"\n  ✔ Best Solution: {', '.join(chosen)}")
    print(f"  ✔ Final Value: {fitness(best_final)} | Total Weight: {get_weight(best_final)}kg")

ga_knapsack()