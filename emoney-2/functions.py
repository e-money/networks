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


def get_vesting_amount(account):
    if account["type"] != "cosmos-sdk/ContinuousVestingAccount":
        raise ValueError("unsupported account type")
    for coin in account["value"]["original_vesting"]:
        if coin["denom"] == "ungm":
            return int(coin["amount"])
    return 0


def next_account_number(genesis):
    highest_number = 0
    for account in genesis["app_state"]["auth"]["accounts"]:
        highest_number = max(highest_number, int(
            account["value"]["account_number"]))
    return highest_number + 1


def migrate_seed_round_account(account, original_amount, vesting_start, vesting_end):
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


def update_private_sale_account(account, vesting_amount, vesting_start, vesting_end):
    account["_comment_2"] = "Private Sale Delivery: ungm " + \
        str(vesting_amount)
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
