from itertools import combinations

def smart_home_rules(transactions, min_support, min_confidence):
    # Count item frequencies
    item_counts = {}
    for t in transactions:
        for item in t:
            item_counts[item] = item_counts.get(item, 0) + 1

    min_count = min_support * len(transactions)
    frequent_items = {item for item, count in item_counts.items() if count >= min_count}
    
    # Generate rules
    rules = []
    for itemset_size in range(2, len(frequent_items) + 1):
        # Generate candidate itemsets
        candidates = list(combinations(frequent_items, itemset_size))
        for candidate in candidates:
            candidate_set = set(candidate)
            # Check support
            support_count = sum(1 for t in transactions if candidate_set.issubset(t))
            if support_count < min_count:
                continue
            
            # Generate rules from this itemset
            for i in range(1, len(candidate_set)):
                for antecedent in combinations(candidate_set, i):
                    antecedent_set = set(antecedent)
                    consequent_set = candidate_set - antecedent_set
                    
                    # Calculate confidence
                    antecedent_support = sum(1 for t in transactions if antecedent_set.issubset(t))
                    if antecedent_support == 0: continue
                    
                    confidence = support_count / antecedent_support
                    if confidence >= min_confidence:
                        rules.append({
                            'antecedent': antecedent_set,
                            'consequent': consequent_set,
                            'support': support_count / len(transactions),
                            'confidence': confidence
                        })
    return rules

# IoT Data: Each list is a time window of triggered sensors
iot_logs = [
    {'motion', 'light_on'},
    {'motion', 'light_on', 'thermostat'},
    {'motion', 'light_off'},
    {'motion', 'light_on'},
    {'motion', 'light_on', 'thermostat'},
    {'motion', 'light_on'},
    {'motion', 'light_on', 'thermostat'}
]

rules = smart_home_rules(iot_logs, min_support=0.5, min_confidence=0.8)
for rule in rules:
    print(f"IF {rule['antecedent']} THEN {rule['consequent']} (Conf: {rule['confidence']:.2f})")
from itertools import combinations
from collections import defaultdict


def get_frequent_itemsets(transactions, min_support):
    """Find all frequent itemsets using the Apriori algorithm."""
    item_counts = defaultdict(int)
    n = len(transactions)

    # Count individual item frequencies (1-itemsets)
    for transaction in transactions:
        for item in transaction:
            item_counts[frozenset([item])] += 1

    # Filter by min_support
    frequent = {k: v for k, v in item_counts.items()
                if v / n >= min_support}

    all_frequent = dict(frequent)
    current_frequent = list(frequent.keys())
    k = 2

    while current_frequent:
        # Generate candidate k-itemsets
        candidates = set()
        for i in range(len(current_frequent)):
            for j in range(i + 1, len(current_frequent)):
                union = current_frequent[i] | current_frequent[j]
                if len(union) == k:
                    candidates.add(union)

        # Count candidate frequencies
        candidate_counts = defaultdict(int)
        for transaction in transactions:
            t_set = frozenset(transaction)
            for candidate in candidates:
                if candidate.issubset(t_set):
                    candidate_counts[candidate] += 1

        # Filter by min_support
        new_frequent = {k_: v for k_, v in candidate_counts.items()
                        if v / n >= min_support}

        all_frequent.update(new_frequent)
        current_frequent = list(new_frequent.keys())
        k += 1

    return all_frequent, n


def generate_rules(frequent_itemsets, n_transactions, min_confidence):
    """Generate association rules from frequent itemsets."""
    rules = []
    for itemset in frequent_itemsets:
        if len(itemset) < 2:
            continue
        for size in range(1, len(itemset)):
            for antecedent in combinations(itemset, size):
                antecedent = frozenset(antecedent)
                consequent = itemset - antecedent

                support_itemset   = frequent_itemsets[itemset] / n_transactions
                support_antecedent = frequent_itemsets[antecedent] / n_transactions
                support_consequent = frequent_itemsets[consequent] / n_transactions

                if support_antecedent == 0:
                    continue

                confidence = support_itemset / support_antecedent
                lift       = confidence / support_consequent if support_consequent else 0

                if confidence >= min_confidence:
                    rules.append({
                        "antecedent": set(antecedent),
                        "consequent": set(consequent),
                        "support":    round(support_itemset, 3),
                        "confidence": round(confidence, 3),
                        "lift":       round(lift, 3),
                    })
    return rules

# ─────────────────────────────────────────────
# EXAMPLE 1: Streaming Service (Movie Watch History)
# Identify "Because you watched..." patterns
# ─────────────────────────────────────────────

print("\n" + "=" * 60)
print("  APRIORI ALGORITHM — EXAMPLE 1: Streaming Watch History")
print("=" * 60)

# Each list represents a user's "Watched" list
streaming_transactions = [
    ["Interstellar", "Inception", "The Matrix"],
    ["Inception", "The Matrix", "Star Wars"],
    ["Interstellar", "Inception", "Arrival"],
    ["The Matrix", "Star Wars", "Dune"],
    ["Interstellar", "Arrival", "Dune"],
    ["Inception", "The Matrix", "Dune"],
    ["Interstellar", "Inception", "The Matrix", "Arrival"],
    ["The Matrix", "Star Wars"],
    ["Interstellar", "Inception"],
    ["Arrival", "Dune"],
]

# We want patterns that appear in at least 30% of user histories
MIN_SUPPORT    = 0.3 
# We want the rule to be reliable at least 70% of the time
MIN_CONFIDENCE = 0.7 

frequent_sets3, n3 = get_frequent_itemsets(streaming_transactions, MIN_SUPPORT)
rules3 = generate_rules(frequent_sets3, n3, MIN_CONFIDENCE)

print(f"\n  Users: {n3}  |  Min Support: {MIN_SUPPORT}  |  Min Confidence: {MIN_CONFIDENCE}")

print(f"\n  Frequent Movie Bundles Found ({len(frequent_sets3)}):")
for itemset, count in sorted(frequent_sets3.items(), key=lambda x: -len(x[0])):
    support = round(count / n3, 3)
    print(f"    {str(set(itemset)):<50}  support={support}  count={count}")

print(f"\n  Recommendation Rules Found ({len(rules3)}):")
print(f"  {'If they watched...':<30} → {'Recommend this':<20}  support  confidence  lift")
print("  " + "-" * 85)
for rule in sorted(rules3, key=lambda x: -x['confidence']):
    ant = str(rule['antecedent'])
    con = str(rule['consequent'])
    print(f"  {ant:<30} → {con:<20}  {rule['support']:<9} {rule['confidence']:<12} {rule['lift']}")

print("\n  Analysis Complete: Streaming patterns successfully identified.")


# ─────────────────────────────────────────────
# EXAMPLE 2: PC Hardware & Tech Components
# Identifying hardware compatibility/bundling
# ─────────────────────────────────────────────

print("\n" + "=" * 60)
print("  APRIORI ALGORITHM — EXAMPLE 2: PC Component Bundling")
print("=" * 60)

# Each list is a "Build" or a "Cart"
pc_transactions = [
    ["CPU", "Motherboard", "RAM", "SSD"],
    ["CPU", "Motherboard", "RAM", "GPU", "PowerSupply"],
    ["GPU", "PowerSupply", "Case"],
    ["CPU", "Motherboard", "RAM", "GPU", "PowerSupply", "Case", "SSD"],
    ["CPU", "RAM", "SSD"],
    ["GPU", "PowerSupply", "Case", "Monitor"],
    ["CPU", "Motherboard", "RAM", "PowerSupply"],
    ["Monitor", "Keyboard", "Mouse"],
    ["CPU", "Motherboard", "RAM", "GPU", "SSD"],
    ["GPU", "PowerSupply"],
]

# We want items appearing in 30% of builds
MIN_SUPPORT    = 0.3 
# We want a high accuracy (80%) for our "Frequently Bought Together" widget
MIN_CONFIDENCE = 0.8 

frequent_sets4, n4 = get_frequent_itemsets(pc_transactions, MIN_SUPPORT)
rules4 = generate_rules(frequent_sets4, n4, MIN_CONFIDENCE)

print(f"\n  Total Builds: {n4}  |  Min Support: {MIN_SUPPORT}  |  Min Confidence: {MIN_CONFIDENCE}")

print(f"\n  Frequent Component Groups ({len(frequent_sets4)}):")
for itemset, count in sorted(frequent_sets4.items(), key=lambda x: -len(x[0])):
    support = round(count / n4, 3)
    print(f"    {str(set(itemset)):<55}  support={support}")

print(f"\n  Dynamic Bundling Rules ({len(rules4)}):")
print(f"  {'If customer adds...':<35} → {'Suggest this':<20}  support  confidence  lift")
print("  " + "-" * 90)
for rule in sorted(rules4, key=lambda x: -x['confidence']):
    ant = str(rule['antecedent'])
    con = str(rule['consequent'])
    print(f"  {ant:<35} → {con:<20}  {rule['support']:<9} {rule['confidence']:<12} {rule['lift']}")

print("\n  Hardware patterns successfully mined for E-commerce optimization.")