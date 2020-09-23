import json


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


def migrate_seed_account(account, original_amount, vesting_amount, vestingStart, vestingEnd):
    account["_comment"] = "Seed Round Migration: ungm " + str(original_amount)
    account["type"] = "cosmos-sdk/ContinuousVestingAccount"
    account["value"]["start_time"] = vestingStart
    account["value"]["end_time"] = vestingEnd
    account["value"]["original_vesting"] = [
        {"amount": str(vesting_amount), "denom": "ungm"}]
    return account
