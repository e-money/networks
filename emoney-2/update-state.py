import json
import datetime
from functions import *

genesis_time = datetime.datetime.utcnow()

with open("emoney-1.migrated.json") as importfile:
    # Load emoney-1 export file
    genesis = json.load(importfile)

    # Update chain-id and genesis time
    # genesis["chain_id"] = "emoney-2"
    genesis["chain_id"] = "lilmermaid-6"
    genesis["genesis_time"] = genesis_time.isoformat() + "Z"

    # Increase max validators to 50
    genesis["app_state"]["staking"]["params"]["max_validators"] = 50

    # Lift non-transferability restriction on NGM
    remove_restricted_denoms(genesis)

    # Set NGM inflation to 10%
    set_ngm_inflation(genesis)

    # Key rotation
    replace_addresses(genesis, "key-rotation.csv")

    # Change treasury account to 3 year vesting
    migrate_treasury_account(genesis, genesis_time,
                             genesis_time + datetime.timedelta(days=3*365))

    # Change ecosystem account to 3 year vesting
    migrate_grants_account(genesis, genesis_time,
                           genesis_time + datetime.timedelta(days=3*365))

    # Add Customer Acquisition account
    add_customer_acquisition_account(genesis, genesis_time,
                                     genesis_time + datetime.timedelta(days=2*365))

    # Change allocation for seed round participants and introduce vesting
    migrate_seed_round_accounts(genesis, "seed-round.csv", genesis_time)

    # Deliver tokens to vesting accounts
    update_vesting_accounts(genesis, "vesting.csv", genesis_time)

    # Adjust Liquidity Provisioning account
    migrate_liquidity_pool_account(
        genesis, genesis_time,
        genesis_time + datetime.timedelta(days=365))

    # Create emoney-2 genesis file
    with open("genesis.json", "w", encoding="utf-8") as exportfile:
        json.dump(genesis, exportfile,
                  indent=2, sort_keys=True, ensure_ascii=False)

    # Perform sanity checks
    sanity_check(genesis)
