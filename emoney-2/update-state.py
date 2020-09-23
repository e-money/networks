import json
import csv
import datetime
from functions import *

# TODO Currently genesis time of emoney-1 plus one year
genesis_time = datetime.datetime(2021, 3, 25, 12, 0, 0, tzinfo=None)

with open("emoney-1.export.json") as importfile:
    # Load emoney-1 export file
    genesis = json.load(importfile)
    genesis["genesis_time"] = genesis_time.isoformat() + "Z"

    # Lift non-transferability restriction on NGM
    remove_restricted_denoms(genesis)

    # Change allocation for seed round participants and introduce vesting
    with open("seed-round.csv") as csvfile:
        csv_reader = csv.DictReader(csvfile)
        for row in csv_reader:
            address = row["address"]
            # Original amount as ungm
            original_amount = int(row["amount"]) * 1000000
            # Adjusted amount which must now be vested
            vesting_amount = int(
                (original_amount * 2285000 / 387000)) - original_amount
            account = find_account(address, genesis)
            if account is None:
                raise ValueError("seed account missing")
            account = migrate_seed_account(
                account, original_amount, vesting_amount, genesis_time, genesis_time + datetime.timedelta(days=365))
            update_account(account, genesis)

    # Deliver tokens to private sale participants
    # with open("private-sale.csv") as csvfile:
    #     csv_reader = csv.DictReader(csvfile)
    #     for row in csv_reader:
    #         # TODO
    #         print(row)

    # Adjust token distribution (Treasury, Ecosystem fund etc.)
    # TODO

    # Sanity check (total supply)
    # TODO

    # Create emoney-2 genesis file
    with open("emoney-2.genesis.json", "w", encoding="utf-8") as exportfile:
        json.dump(genesis, exportfile,
                  indent=2, sort_keys=True)


# Open migrated Genesis
# 1. Private sale delivery
# 2. Apply updated token distribution
# 3. Adjust seed round amounts

# 4. Verifications and sanity checks.
#     - Supply check
