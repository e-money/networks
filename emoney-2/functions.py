import csv
import datetime
import json
import time


def remove_restricted_denoms(genesis):
    genesis["app_state"]["authority"]["restricted_denoms"] = []


def new_account(address, account_number):
    return {
        "type": "cosmos-sdk/Account",
        "value": {
            "account_number": str(account_number),
            "address": address,
            "coins": [],
            "public_key": None,
            "sequence": "0"
        }
    }


def get_account(address, genesis):
    for account in genesis["app_state"]["auth"]["accounts"]:
        if account["value"]["address"] == address:
            return account
    return None


def update_account(account, genesis):
    for target in genesis["app_state"]["auth"]["accounts"]:
        if target["value"]["address"] == account["value"]["address"]:
            target = account
            return
    raise Exception("account not found")


def get_amount(coins, denom):
    for coin in coins:
        if coin["denom"] == denom:
            return int(coin["amount"])
    return 0


def remove_amount(coins, denom):
    for coin in coins:
        if coin["denom"] == denom:
            coins.remove(coin)
            return


def set_amount(coins, denom, amount):
    for coin in coins:
        if coin["denom"] == denom:
            coin["amount"] = str(amount)
            return
    coins.append(
        {"amount": str(amount), "denom": denom}
    )


def get_unbonding_amount(delegator_address, validator_address, genesis):
    for unbonding_delegation in genesis["app_state"]["staking"]["unbonding_delegations"]:
        if unbonding_delegation["delegator_address"] == delegator_address and unbonding_delegation["validator_address"] == validator_address:
            total_unbonding_amount = 0
            for entry in unbonding_delegation["entries"]:
                total_unbonding_amount += int(entry["balance"])
            return total_unbonding_amount
    return 0


def get_bonded_amount(shares, validator_address, genesis):
    for validator in genesis["app_state"]["staking"]["validators"]:
        if validator["operator_address"] == validator_address:
            total_shares = float(validator["delegator_shares"])
            total_tokens = float(validator["tokens"])
            return int(round(total_tokens * shares / total_shares))
    raise LookupError("validator missing")


def get_delegated_amount(delegator_address, genesis):
    delegated_amount = 0
    for delegation in genesis["app_state"]["staking"]["delegations"]:
        if delegation["delegator_address"] == delegator_address:
            validator_address = delegation["validator_address"]
            shares = float(delegation["shares"])
            delegated_amount += get_bonded_amount(
                shares, validator_address, genesis)
            delegated_amount += get_unbonding_amount(
                delegator_address, validator_address, genesis)
    return delegated_amount


def next_account_number(genesis):
    highest_number = 0
    for account in genesis["app_state"]["auth"]["accounts"]:
        highest_number = max(highest_number, int(
            account["value"]["account_number"]))
    return highest_number + 1


def migrate_treasury_account(account, vesting_start, vesting_end):
    account["_comment"] = "Treasury"

    delegated_amount = get_amount(
        account["value"]["delegated_vesting"], "ungm")

    original_vesting_amount = 60000000*1000000
    coins_amount = original_vesting_amount - delegated_amount
    set_amount(account["value"]["coins"], "ungm", coins_amount)

    account["value"].update({
        "start_time": str(int(vesting_start.timestamp())),
        "end_time": str(int(vesting_end.timestamp())),
        "original_vesting": [
            {"amount": str(original_vesting_amount),
             "denom": "ungm"}
        ]})


def migrate_ecosystem_account(account, vesting_start, vesting_end):
    account["_comment"] = "Ecosystem Fund (Grants)"

    original_vesting_amount = get_amount(account["value"]["coins"], "ungm")

    account["value"].update({
        "start_time": str(int(vesting_start.timestamp())),
        "end_time": str(int(vesting_end.timestamp())),
        "original_vesting": [
            {"amount": str(original_vesting_amount),
             "denom": "ungm"}
        ]})


def add_customer_acquisition_account(account, vesting_start, vesting_end):
    account["_comment"] = "Customer Acquisition"

    original_vesting_amount = 8000000*1000000

    account["type"] = "cosmos-sdk/ContinuousVestingAccount"
    account["value"].update({
        "coins": [
            {"amount": str(original_vesting_amount),
             "denom": "ungm"}
        ],
        "start_time": str(int(vesting_start.timestamp())),
        "end_time": str(int(vesting_end.timestamp())),
        "original_vesting": [
            {"amount": str(original_vesting_amount),
             "denom": "ungm"}
        ]})


def migrate_liquidity_provisioning_account(account, sold_amount, vesting_start, vesting_end):
    account["_comment"] = "Liquidity Provisioning"

    original_vesting_amount = 22000000*1000000 - sold_amount
    set_amount(account["value"]["coins"], "ungm", original_vesting_amount)

    account["value"].update({
        "start_time": str(int(vesting_start.timestamp())),
        "end_time": str(int(vesting_end.timestamp())),
        "original_vesting": [
            {"amount": str(original_vesting_amount),
             "denom": "ungm"}
        ]})


def migrate_seed_round_account(account, purchased_amount, original_vesting_amount, coins_amount, delegated_amount, vesting_start, vesting_end):
    # coins_amount + delegated_vesting_amount + delegated_free_amount = total account balance
    total_amount = coins_amount + delegated_amount
    shift_amount = total_amount - purchased_amount

    account["_comment"] = "Seed Migration: purchased_amount: {0}, total_amount: {1}, coins_amount: {2}, delegated_amount: {3}, shift_amount: {4}".format(
        purchased_amount, total_amount, coins_amount, delegated_amount, shift_amount)

    delegated_vesting_amount = min(delegated_amount, purchased_amount)
    delegated_free_amount = delegated_amount - delegated_vesting_amount

    total_amount = original_vesting_amount + shift_amount
    coins_amount = total_amount - delegated_free_amount - delegated_vesting_amount

    # account["_1_b_seed_migration"] = "original_vesting_amount: {0}, total_amount: {1}, coins_amount: {2}, delegated_vesting_amount: {3}, delegated_free_amount: {4}".format(
    #     original_vesting_amount, total_amount, coins_amount, delegated_vesting_amount, delegated_free_amount)

    if coins_amount < 0 or delegated_vesting_amount < 0 or delegated_free_amount < 0 or original_vesting_amount < 0:
        raise ValueError("negative amount")

    account["type"] = "cosmos-sdk/ContinuousVestingAccount"
    set_amount(account["value"]["coins"], "ungm", coins_amount)
    account["value"].update({
        "delegated_free": [
            {"amount": str(delegated_free_amount), "denom": "ungm"}
        ],
        "delegated_vesting": [
            {"amount": str(delegated_vesting_amount), "denom": "ungm"}
        ],
        "start_time": str(int(vesting_start.timestamp())),
        "end_time": str(int(vesting_end.timestamp())),
        "original_vesting": [
            {"amount": str(original_vesting_amount), "denom": "ungm"}
        ]})
    return account


def migrate_seed_round_accounts(genesis, filename, vesting_start):
    total_amount = 0
    with open(filename) as csvfile:
        csv_reader = csv.DictReader(csvfile)
        for row in csv_reader:
            address = row["address"]

            # Original purchased amount as ungm
            purchased_amount = int(float(row["amount"]) * 1000000)
            original_vesting_amount = int(
                round(purchased_amount * 2285000 / 387000))
            total_amount += original_vesting_amount

            account = get_account(address, genesis)
            if account is None:
                raise ValueError("seed account missing")

            coins_amount = get_amount(account["value"]["coins"], "ungm")
            delegated_amount = get_delegated_amount(
                account["value"]["address"], genesis)

            account = migrate_seed_round_account(
                account, purchased_amount, original_vesting_amount, coins_amount, delegated_amount, vesting_start, vesting_start + datetime.timedelta(days=365))
            update_account(account, genesis)
    return total_amount


def update_private_sale_account(account, purchased_amount, vesting_start, vesting_end):
    # 20% unlocked, 80% vesting for 6 months
    unlocked_amount = int(round(0.20 * purchased_amount))
    vesting_amount = purchased_amount - unlocked_amount

    account["_comment"] = "Private Sale Delivery: purchased_amount: {0}, unlocked_amount: {1}, vesting_amount: {2}".format(
        purchased_amount, unlocked_amount, vesting_amount)

    # Consider existing amounts
    coins_amount = purchased_amount + \
        get_amount(account["value"]["coins"], "ungm")

    original_vesting_amount = vesting_amount
    if account["type"] == "cosmos-sdk/ContinuousVestingAccount":
        original_vesting_amount += get_amount(
            account["value"]["original_vesting"], "ungm")

    # Set available amount
    set_amount(account["value"]["coins"], "ungm", coins_amount)

    # Update vesting
    account["type"] = "cosmos-sdk/ContinuousVestingAccount"
    account["value"].update({
        "start_time": str(int(vesting_start.timestamp())),
        "end_time": str(int(vesting_end.timestamp())),
        "original_vesting": [
            {"amount": str(original_vesting_amount), "denom": "ungm"}
        ]})
    return account


def update_private_sale_accounts(genesis, filename, vesting_start):
    total_amount = 0
    with open(filename) as csvfile:
        csv_reader = csv.DictReader(csvfile)
        for row in csv_reader:
            address = row["address"]

            # Purchased amount as ungm
            purchased_amount = int(float(row["amount"]) * 1000000)
            total_amount += purchased_amount

            account = get_account(address, genesis)
            if account is None:
                # print("Delivering private sale tokens to new account: " + address)
                account = new_account(address, next_account_number(genesis))
                genesis["app_state"]["auth"]["accounts"].append(account)
            else:
                print("Delivering private sale tokens to existing account: " + address)

            account = update_private_sale_account(
                account, purchased_amount, vesting_start, vesting_start + datetime.timedelta(days=365/2))
            update_account(account, genesis)
    return total_amount


def get_total_coins_amount(genesis):
    total_coins_amount = {}
    for account in genesis["app_state"]["auth"]["accounts"]:
        if "coins" not in account["value"]:
            continue

        for coin in account["value"]["coins"]:
            balance = int(coin["amount"])
            denom = coin["denom"]
            if denom in total_coins_amount:
                total_coins_amount[denom] += balance
            else:
                total_coins_amount[denom] = balance

    return total_coins_amount


def get_total_delegated_tokens(genesis):
    total_delegated = 0
    for account in genesis["app_state"]["auth"]["accounts"]:
        total_delegated += get_delegated_amount(
            account["value"]["address"], genesis)
    return total_delegated
