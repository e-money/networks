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


def migrate_seed_account(account, original_amount, vesting_amount, vesting_start, vesting_end):
    account["_comment"] = "Seed Round Migration: ungm " + str(original_amount)
    account["type"] = "cosmos-sdk/ContinuousVestingAccount"
    account["value"]["start_time"] = str(
        int(time.mktime(vesting_start.timetuple())))
    account["value"]["end_time"] = str(
        int(time.mktime(vesting_end.timetuple())))
    account["value"]["original_vesting"] = [
        {"amount": str(vesting_amount), "denom": "ungm"}]
    return account


def nextAccountNumber(genesis):
    accountNo = 0
    for acc in genesis["app_state"]["auth"]["accounts"]:
        accountNo = max(accountNo, int(acc["value"]["account_number"]))

    return accountNo + 1

def newVestingAccount(addr, balance, accNo, genesisTime, vestingAmount, vestingPeriod):
    acc = newAccount(addr, balance, accNo)
    acc["type"] = "cosmos-sdk/ContinuousVestingAccount"

    start_time = int(genesisTime.timestamp())
    end_time = int((genesisTime + vestingPeriod).timestamp())

    acc["value"].update({
        "delegated_free": [],
        "delegated_vesting": [
            { "amount": str(vestingAmount * 1000000), "denom": "ungm" }
        ],
        "end_time": str(end_time),
        "original_vesting": [
            { "amount": str(vestingAmount * 1000000), "denom": "ungm" }
        ],
        "public_key": None,
        "sequence": "0",
        "start_time": str(start_time)
    })

    return acc


def newAccount(addr, balance, accNo):
    return {
        "type": "cosmos-sdk/Account",
        "value": {
            "account_number": str(accNo),
            "address": addr,
            "coins": [
                {
                    "amount": str(balance * 1000000),
                    "denom": "ungm"
                }
            ],
            "public_key": None,
            "sequence": "0"
        }
    }
