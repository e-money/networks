import json


def removeRestrictedDenoms(genesis):
    genesis["app_state"]["authority"]["restricted_denoms"] = []


def findAccount(address, genesis):
    for account in genesis["app_state"]["auth"]["accounts"]:
        if account["value"]["address"] == address:
            return account

    return None


def updateAccount(account, genesis):
    for target in genesis["app_state"]["auth"]["accounts"]:
        if target["value"]["address"] == account["value"]["address"]:
            target = account
            return

    raise Exception("account not found")
