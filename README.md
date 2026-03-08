1. A* (A-Star) Search Algorithm
   
The "Smart GPS"
A* is a pathfinding and graph traversal algorithm. While other algorithms might blindly explore every possible direction (like a vacuum cleaner hitting walls), A* uses a "heuristic" (a smart guess) to prioritize the path that looks most promising.
The Formula
A* makes decisions based on the equation:
$$f(n) = g(n) + h(n)$$
•	$g(n)$: The actual cost to get from the start to the current node (how far we've already walked).
•	$h(n)$: The estimated cost to get from the current node to the goal (the "as-the-crow-flies" distance).
•	$f(n)$: The total estimated cost of the path through node $n$.
Why it’s cool: It is "optimally efficient," meaning no other algorithm using the same heuristic will find the shortest path while exploring fewer nodes.

2. Apriori Algorithm
   
The "Market Basket" Expert
The Apriori algorithm is used for Association Rule Learning. It identifies frequent items in a dataset and predicts what else a user might want based on what they already have. This is exactly how Amazon or Netflix knows what to recommend to you.
Core Metrics
To decide if a pattern is worth keeping, it uses three scores:
<img width="575" height="198" alt="image" src="https://github.com/user-attachments/assets/90b8162c-7271-4028-ae25-56ccfb47887e" />

3. Genetic Algorithm (GA)
   
The "Survival of the Fittest" Optimizer
Genetic Algorithms are used to find solutions to problems that are too big for a computer to check every possibility. It mimics the process of biological evolution to "breed" a perfect solution.
The Evolutionary Cycle
1.	Population: Start with a bunch of random "candidate" solutions (chromosomes).
2.	Fitness Function: Score each solution. How close is it to being perfect?
3.	Selection: Kill off the weak ones; keep the best ones to be "parents."
4.	Crossover: Mix the traits of the parents to create "children" (new solutions).
5.	Mutation: Occasionally flip a random bit to keep the population diverse and prevent "stagnation."
Why it’s cool: It’s great for "black box" problems where we don't know the exact math, but we know a good result when we see one (like designing the shape of an airplane wing for maximum lift).

