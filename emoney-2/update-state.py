import json
import datetime
from functions import *

genesis_time = datetime.datetime.utcnow()

with open("emoney-1.migrated.json") as importfile:
    # Load emoney-1 export file
    genesis = json.load(importfile)

    # Update chain-id and genesis time
    genesis["chain_id"] = "emoney-2"
    genesis["genesis_time"] = genesis_time.isoformat() + "Z"

    # Increase max validators to 50
    genesis["app_state"]["staking"]["params"]["max_validators"] = 50

    # Lift non-transferability restriction on NGM
    remove_restricted_denoms(genesis)

    # Change treasury account to 3 year vesting
    # account = find_account(
    #     "emoney1cs4323dyzu0wxfj4vc62m8q3xsczfavqx9x3zd", genesis)
    # migrate_treasury_account(account, genesis_time,
    #                          genesis_time + datetime.timedelta(days=3*365))

    # Change allocation for seed round participants and introduce vesting
    migrate_seed_round_accounts(
        genesis, "seed-round.csv", genesis_time)

    # Deliver tokens to private sale participants
    update_private_sale_accounts(
        genesis, "private-sale.csv", genesis_time)

    # Sanity check (total supply)
    # TODO
    total_supply = calculate_total_token_supply(genesis)
    if total_supply["ungm"] != 100000000 * 1000000:
        print("WARN: sanity check failed. Unexpected supply of NGM token:",
              total_supply["ungm"])

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
