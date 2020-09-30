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


def find_account(address, genesis):
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


def next_account_number(genesis):
    highest_number = 0
    for account in genesis["app_state"]["auth"]["accounts"]:
        highest_number = max(highest_number, int(
            account["value"]["account_number"]))
    return highest_number + 1


def migrate_seed_round_account(account, original_amount, vesting_start, vesting_end):
    # TODO original_amount should be deducted from available amount
    available_amount = get_amount(account["value"]["coins"], "ungm")
    if available_amount < original_amount:
        print("low balance: ", available_amount, original_amount, account)
    else:
        print("available: ", available_amount)

    # Adjusted amount which must now be vested
    vesting_amount = int(
        (original_amount * 2285000 / 387000)) - original_amount

    account["_comment_1"] = "Seed Round Migration: ungm " + \
        str(original_amount)
    account["type"] = "cosmos-sdk/ContinuousVestingAccount"
    account["value"].update({
        "delegated_free": [],
        "delegated_vesting": [],
        "start_time": str(int(vesting_start.timestamp())),
        "end_time": str(int(vesting_end.timestamp())),
        "original_vesting": [
            {"amount": str(vesting_amount), "denom": "ungm"}
        ]})
    return account


def migrate_seed_round_accounts(genesis, filename, vesting_start):
    with open(filename) as csvfile:
        csv_reader = csv.DictReader(csvfile)
        for row in csv_reader:
            address = row["address"]

            # Original amount as ungm
            original_amount = int(row["amount"]) * 1000000

            account = find_account(address, genesis)
            if account is None:
                raise ValueError("seed account missing")

            account = migrate_seed_round_account(
                account, original_amount, vesting_start, vesting_start + datetime.timedelta(days=365))
            update_account(account, genesis)


def update_private_sale_account(account, available_amount, vesting_amount, vesting_start, vesting_end):
    account["_comment_2"] = "Private Sale Delivery: ungm " + \
        str(available_amount + vesting_amount)

    # Consider existing amounts
    available_amount = available_amount + \
        get_amount(account["value"]["coins"], "ungm")
    if account["type"] == "cosmos-sdk/ContinuousVestingAccount":
        vesting_amount = vesting_amount + \
            get_amount(account["value"]["original_vesting"], "ungm")

    # Set available amount
    set_amount(account["value"]["coins"], "ungm", available_amount)

    # Update vesting
    account["type"] = "cosmos-sdk/ContinuousVestingAccount"
    account["value"].update({
        "delegated_free": [],
        "delegated_vesting": [],
        "start_time": str(int(vesting_start.timestamp())),
        "end_time": str(int(vesting_end.timestamp())),
        "original_vesting": [
            {"amount": str(vesting_amount), "denom": "ungm"}
        ]})
    return account


def update_private_sale_accounts(genesis, filename, vesting_start):
    with open(filename) as csvfile:
        csv_reader = csv.DictReader(csvfile)
        for row in csv_reader:
            address = row["address"]
            # Amount as ungm
            amount = int(row["amount"]) * 1000000
            # 20% unlocked, 80% vesting for 6 months
            available_amount = int(0.20 * amount)
            vesting_amount = amount - available_amount

            account = find_account(address, genesis)
            if account is None:
                print("Delivering private sale tokens to new account: " + address)
                account = new_account(address, next_account_number(genesis))
                genesis["app_state"]["auth"]["accounts"].append(account)
            else:
                print("Delivering private sale tokens to existing account: " + address)

            account = update_private_sale_account(
                account, available_amount, vesting_amount, vesting_start, vesting_start + datetime.timedelta(days=365/2))
            update_account(account, genesis)


def migrate_treasury_account(account, vesting_start, vesting_end):
    print(json.dumps(account, indent=2, sort_keys=True))
    account["_comment_0"] = "Treasury"

    # Account on emoney-1 chain contained 50M "e-Money A/S" + 15M "Fundraiser"
    available_amount = get_amount(account["value"]["coins"], "ungm")

    # Decrease by 5M to reach 60M "Treasury" allocation for emoney-2 and adjust vesting amount and period
    available_amount = available_amount - (5000000 * 1000000)
    set_amount(account["value"]["coins"], "ungm", available_amount)
    delegated_amount = get_amount(
        account["value"]["delegated_vesting"], "ungm")
    account["value"].update({
        "start_time": str(int(vesting_start.timestamp())),
        "end_time": str(int(vesting_end.timestamp())),
        "original_vesting": [
            {"amount": str(available_amount + delegated_amount),
             "denom": "ungm"}
        ]})
    print(json.dumps(account, indent=2, sort_keys=True))


def calculate_total_token_supply(genesis):
    total_supply = {}
    for account in genesis["app_state"]["auth"]["accounts"]:
        if "coins" not in account["value"]:
            # Module accounts do not have a direct balance.
            continue

        for coin in account["value"]["coins"]:
            balance = int(coin["amount"])
            denom = coin["denom"]
            if denom in total_supply:
                total_supply[denom] += balance
            else:
                total_supply[denom] = balance

    return total_supply
