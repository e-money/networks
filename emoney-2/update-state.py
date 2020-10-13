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
    account = get_account(
        "emoney1cs4323dyzu0wxfj4vc62m8q3xsczfavqx9x3zd", genesis)
    migrate_treasury_account(account, genesis_time,
                             genesis_time + datetime.timedelta(days=3*365))

    # Change ecosystem account to 3 year vesting
    account = get_account(
        "emoney14r5rva8qk5ee6rvk5sdtmxea40uf74k7uh4yjv", genesis)
    migrate_ecosystem_account(account, genesis_time,
                              genesis_time + datetime.timedelta(days=3*365))

    # Add Customer Acquisition account
    account = new_account(
        "TBD", next_account_number(genesis))
    genesis["app_state"]["auth"]["accounts"].append(account)
    add_customer_acquisition_account(account, genesis_time,
                                     genesis_time + datetime.timedelta(days=2*365))

    # Change allocation for seed round participants and introduce vesting
    seed_round_purchase_amount = migrate_seed_round_accounts(
        genesis, "seed-round.csv", genesis_time)

    # Deliver tokens to private sale participants
    private_sale_purchase_amount = update_private_sale_accounts(
        genesis, "private-sale.csv", genesis_time)

    # Adjust Liquidity Provisioning account
    account = get_account(
        "emoney147verqcxwdkgrn663x2qj66zyqc5mu479afw9n", genesis)
    migrate_liquidity_provisioning_account(
        account, seed_round_purchase_amount + private_sale_purchase_amount, genesis_time,
        genesis_time + datetime.timedelta(days=365))

    # Sanity check (total supply)
    total_supply = calculate_total_token_supply(genesis)
    if total_supply["ungm"] != 100000000 * 1000000:
        print("WARN: sanity check failed. Unexpected supply of ungm token:",
              total_supply["ungm"], total_supply["ungm"] / 1000000)

    # Create emoney-2 genesis file
    with open("genesis.json", "w", encoding="utf-8") as exportfile:
        json.dump(genesis, exportfile,
                  indent=2, sort_keys=True, ensure_ascii=False)
