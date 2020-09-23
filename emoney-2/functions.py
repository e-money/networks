import json


def removeRestrictedDenoms(genesis):
    genesis["app_state"]["authority"]["restricted_denoms"] = []


def findAccount(address, genesis):
    for acc in genesis["app_state"]["auth"]["accounts"]:
        print()