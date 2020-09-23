import json
import csv
from functions import *


with open("emoney-1.export.json") as importfile:
    # Load emoney-1 export file
    genesis = json.load(importfile)

    # Lift non-transferability restriction on NGM
    removeRestrictedDenoms(genesis)

    # Change allocation for seed round participants and introduce vesting
    with open("seed-round.csv") as csvfile:
        csv_reader = csv.DictReader(csvfile)
        for row in csv_reader:
            # TODO
            print(row)

    # Deliver tokens to private sale participants
    with open("private-sale.csv") as csvfile:
        csv_reader = csv.DictReader(csvfile)
        for row in csv_reader:
            # TODO
            print(row)

    # Adjust token distribution (Treasury, Ecosystem fund etc.)
    # TODO

    # Sanity check (total supply)
    # TODO

    # Create emoney-2 genesis file
    with open("emoney-2.genesis.json", "w", encoding="utf-8") as exportfile:
        json.dump(genesis, exportfile, ensure_ascii=False, indent=4)


# Open migrated Genesis
# 1. Private sale delivery
# 2. Apply updated token distribution
# 3. Adjust seed round amounts

# 4. Verifications and sanity checks.
#     - Supply check
