import json
import csv
from functions import *


with open('emoney-1.export.json') as importfile:
    genesis = json.load(importfile)

    removeRestrictedDenoms(genesis)

    with open('emoney-2.genesis.json', 'w', encoding='utf-8') as exportfile:
        json.dump(genesis, exportfile, ensure_ascii=False, indent=4)


# with open('sale.csv') as csv_file:
#   csv_reader = csv.DictReader(csv_file)
#   for row in csv_reader:
#     print(row)


# Open migrated Genesis
# 1. Private sale delivery
# 2. Apply updated token distribution
# 3. Adjust seed round amounts

# 4. Verifications and sanity checks.
#     - Supply check
