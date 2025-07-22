# /// script
# requires-python = ">=3.13"
# dependencies = [
#     "faker",
# ]
# ///

#!/usr/bin/env python3
"""
Deterministic fake company‑hierarchy generator.
"""

import csv
import random
from faker import Faker

SEED = 0
N_ROOTS = 15
MAX_DEPTH = 5
LEAF_PROB = 0.35
CHILDREN_B = (3, 6)

random.seed(SEED)
faker = Faker()
faker.seed_instance(SEED)

seen = set()


def gen_name():
    while True:
        name = faker.company()
        if name not in seen:
            seen.add(name)
            return name


rows = []


def grow(node, parent, root, depth):
    rows.append({"company": node, "parent": parent, "root": root})
    if depth == MAX_DEPTH or (parent and random.random() < LEAF_PROB):
        return
    for _ in range(random.randint(*CHILDREN_B)):
        grow(gen_name(), node, root, depth + 1)


for _ in range(N_ROOTS):
    root = gen_name()
    grow(root, None, root, 1)

with open("companies.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, ["company", "parent", "root"])
    w.writeheader()
    w.writerows(rows)

print(f"Generated {len(rows)} rows (seed={SEED}) → companies.csv")
