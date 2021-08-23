import json

# The single validator to launch the network
delegator_address = "emoney1aw569wk7mhh45z8ecjur5w6q0rkcsk52x3gyfu"
validator_address = "emoneyvaloper1aw569wk7mhh45z8ecjur5w6q0rkcsk52p3wsh3"


def update_gentxs(gentxs):
    gentxs = [
        {
            "body": {
                "messages": [
                    {
                        "@type": "/cosmos.staking.v1beta1.MsgCreateValidator",
                        "description": {
                            "moniker": "node0",
                            "identity": "",
                            "website": "",
                            "security_contact": "",
                            "details": ""
                        },
                        "commission": {
                            "rate": "0.150000000000000000",
                            "max_rate": "1.000000000000000000",
                            "max_change_rate": "1.000000000000000000"
                        },
                        "min_self_delegation": "1",
                        "delegator_address": "emoney1aw569wk7mhh45z8ecjur5w6q0rkcsk52x3gyfu",
                        "validator_address": "emoneyvaloper1aw569wk7mhh45z8ecjur5w6q0rkcsk52p3wsh3",
                        "pubkey": {
                            "@type": "/cosmos.crypto.ed25519.PubKey",
                            "key": "+3OXCRCOzcgDcCgLtZn75UVDNtMoV16KnlU6GDUTzxQ="
                        },
                        "value": {
                            "denom": "ungm",
                            "amount": "6000"
                        }
                    }
                ],
                "memo": "951dc30827c682bf99e99c08776429d8b900b22a@192.168.0.1:26656",
                "timeout_height": "0",
                "extension_options": [],
                "non_critical_extension_options": []
            },
            "auth_info": {
                "signer_infos": [
                    {
                        "public_key": {
                            "@type": "/cosmos.crypto.secp256k1.PubKey",
                            "key": "A3pWM2LN88gSCMxL3wip1m0tGM/7dx/zEWHCmjkGvYRz"
                        },
                        "mode_info": {
                            "single": {
                                "mode": "SIGN_MODE_DIRECT"
                            }
                        },
                        "sequence": "0"
                    }
                ],
                "fee": {
                    "amount": [],
                    "gas_limit": "0",
                    "payer": "",
                    "granter": ""
                }
            },
            "signatures": [
                "N2sLm6P1gY1qiaMc0wY6cfWAT/eZqePjzi3KnSs3Q5dak1o3Ri4uAnqkoLceGFibZ/ciBZAsDQyrzvwwf1LtPQ=="
            ]
        }
    ]


def update_slashing(slashing):
    slashing["signing_infos"] = []


def update_staking(staking):
    staking["last_total_power"] = "100"
    staking["last_validator_powers"] = {
        "address": validator_address,
        "power": "100"
    }
    staking["delegations"] = [
        {
            "delegator_address": delegator_address,
            "shares": "100",
            "validator_address": validator_address
        },
    ]
    staking["validators"] = []
    #     "commission": {
    #         "commission_rates": {
    #             "max_change_rate": "0.05",
    #             "max_rate": "0.50",
    #             "rate": "0.10"
    #         },
    #         "update_time": "2020-11-30T07:51:56.043783323Z"
    #     },
    #     "consensus_pubkey": {
    #         "@type": "/cosmos.crypto.ed25519.PubKey",
    #         "key": "J2YLZof1PIKXX/mrje0i26okqn8Y6t9mQauPjDSzL3I="
    #     },
    #     "delegator_shares": "100",
    #     "description": {
    #         "details": "",
    #         "identity": "",
    #         "moniker": "",
    #         "security_contact": "",
    #         "website": ""
    #     },
    #     "jailed": False,
    #     "min_self_delegation": "1",
    #     "operator_address": validator_address,
    #     "status": "BOND_STATUS_BONDED",
    #     "tokens": "100",
    #     "unbonding_height": "0",
    #     "unbonding_time": "2021-04-06T16:08:51.984393094Z"
    # }]
    staking["redelegations"] = []
    staking["unbonding_delegations"] = []


# Process intermediate (migrated) genesis file
with open("lilmermaid-10.migrated.json") as importfile:
    genesis = json.load(importfile)

    update_staking(genesis["app_state"]["staking"])
    update_slashing(genesis["app_state"]["slashing"])

    # Create final genesis file
    with open("genesis.json", "w", encoding="utf-8") as exportfile:
        json.dump(genesis, exportfile, indent=2,
                  sort_keys=True, ensure_ascii=False)
