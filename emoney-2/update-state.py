import json
import csv
import datetime
from functions import *

genesis_time = datetime.datetime.utcnow()

with open("emoney-1.migrated.json") as importfile:
    # Load emoney-1 export file
    genesis = json.load(importfile)

    # Update chain-id and genesis time
    genesis["chain_id"] = "emoney-2"
    genesis["genesis_time"] = genesis_time.isoformat() + "Z"

    # Lift non-transferability restriction on NGM
    remove_restricted_denoms(genesis)

    # Change treasury account to 3 year vesting
    # account = find_account(
    #     "emoney1cs4323dyzu0wxfj4vc62m8q3xsczfavqx9x3zd", genesis)
    # migrate_treasury_account(account, genesis_time,
    #                          genesis_time + datetime.timedelta(days=3*365))

    # Change allocation for seed round participants and introduce vesting
    with open("seed-round.csv") as csvfile:
        csv_reader = csv.DictReader(csvfile)
        for row in csv_reader:
            address = row["address"]

            # Original amount as ungm
            original_amount = int(row["amount"]) * 1000000

            account = find_account(address, genesis)
            if account is None:
                raise ValueError("seed account missing")

            account = migrate_seed_round_account(
                account, original_amount, genesis_time, genesis_time + datetime.timedelta(days=365))
            update_account(account, genesis)

    # Deliver tokens to private sale participants
    with open("private-sale.csv") as csvfile:
        csv_reader = csv.DictReader(csvfile)
        for row in csv_reader:
            address = row["address"]
            # Amount as ungm
            amount = int(row["amount"]) * 1000000
            # 20% unlocked, 80% vesting for 6 months
            available_amount = int(0.20 * amount)
            vesting_amount = amount - available_amount
            vesting_period = datetime.timedelta(days=365/2)

            account = find_account(address, genesis)
            if account is None:
                print("Delivering private sale tokens to new account: " + address)
                account = new_account(address, next_account_number(genesis))
                genesis["app_state"]["auth"]["accounts"].append(account)
            else:
                print("Delivering private sale tokens to existing account: " + address)

            account = update_private_sale_account(
                account, available_amount, vesting_amount, genesis_time, genesis_time + vesting_period)
            update_account(account, genesis)

    # Sanity check (total supply)
    # TODO
    totalSupply = calculate_total_token_supply(genesis)
    if totalSupply["ungm"] != 100000000 * 1000000:
        print("WARN: sanity check failed. Unexpected supply of NGM token",
              totalSupply["ungm"])

    # Create emoney-2 genesis file
    with open("genesis.json", "w", encoding="utf-8") as exportfile:
        json.dump(genesis, exportfile,
                  indent=2, sort_keys=True)


# Open migrated Genesis
# 1. Private sale delivery
# 2. Apply updated token distribution
# 3. Adjust seed round amounts

# 4. Verifications and sanity checks.
#     - Supply check
