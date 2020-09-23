import json
import time


def remove_restricted_denoms(genesis):
    genesis["app_state"]["authority"]["restricted_denoms"] = []


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
