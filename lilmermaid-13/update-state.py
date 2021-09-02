import json

# This script adapts a genesis file to contain only a single validator.

# Specify the single validator to launch the network (including key replacement)
old_validator_address = "2F872BA45A6E72C5D039E1867BEEC2022B73FEAE"
old_operator_address = "emoneyvaloper1sxx9mszve0gaedz5ld7qdkjkfv8z992atddr2y"
old_consensus_public_key = "512zQwG31iGhEAIzMwT8Yl6ZG29IGMaLMRoq0GI91/o="
new_validator_address = "7ADE63DE3DBFD3772927FDF319D23994B8323BC2"
new_operator_address = "emoneyvaloper1aw569wk7mhh45z8ecjur5w6q0rkcsk52p3wsh3"
new_consensus_public_key = "+3OXCRCOzcgDcCgLtZn75UVDNtMoV16KnlU6GDUTzxQ="

# Process intermediate (migrated) genesis file
with open("lilmermaid-13.migrated.json") as importfile:
    genesis = json.load(importfile)

    # Re-compute Tendermint validators
    del genesis["validators"]

    # Shorthands
    staking = genesis["app_state"]["staking"]
    distribution = genesis["app_state"]["distribution"]
    slashing = genesis["app_state"]["slashing"]

    # Validators
    for validator in staking["validators"]:
        if validator["operator_address"] == old_operator_address:
            validator["operator_address"] = new_operator_address
            validator["consensus_pubkey"]["key"] = new_consensus_public_key
            staking["validators"] = [validator]
            break

    # Last voting power
    for last_validator_power in staking["last_validator_powers"]:
        if last_validator_power["address"] == old_operator_address:
            last_validator_power["address"] = new_operator_address
            staking["last_validator_powers"] = [last_validator_power]
            staking["last_total_power"] = last_validator_power["power"]
            break

    # Delegations
    replacement_delegations = []
    for delegation in staking["delegations"]:
        if delegation["validator_address"] == old_operator_address:
            delegation["validator_address"] = new_operator_address
            replacement_delegations.append(delegation)
    staking["delegations"] = replacement_delegations

    # Redelegations
    staking["redelegations"] = []

    # Unbonding delegations
    replacement_unbonding_delegations = []
    for unbonding_delegation in staking["unbonding_delegations"]:
        if unbonding_delegation["validator_address"] == old_operator_address:
            unbonding_delegation["validator_address"] = new_operator_address
            replacement_unbonding_delegations.append(unbonding_delegation)
    staking["unbonding_delegations"] = replacement_unbonding_delegations

    # Delegator starting infos
    replacement_delegator_starting_infos = []
    for delegator_starting_info in distribution["delegator_starting_infos"]:
        if delegator_starting_info["validator_address"] == old_operator_address:
            delegator_starting_info["validator_address"] = new_operator_address
            replacement_delegator_starting_infos.append(
                delegator_starting_info)
    distribution["delegator_starting_infos"] = replacement_delegator_starting_infos

    # Outstanding rewards
    replacement_outstanding_rewards = []
    for outstanding_reward in distribution["outstanding_rewards"]:
        if outstanding_reward["validator_address"] == old_operator_address:
            outstanding_reward["validator_address"] = new_operator_address
            replacement_outstanding_rewards.append(
                outstanding_reward)
    distribution["outstanding_rewards"] = replacement_outstanding_rewards

    # Validator accumulated commissions
    replacement_validator_accumulated_commissions = []
    for validator_accumulated_commission in distribution["validator_accumulated_commissions"]:
        if validator_accumulated_commission["validator_address"] == old_operator_address:
            validator_accumulated_commission["validator_address"] = new_operator_address
            replacement_validator_accumulated_commissions.append(
                validator_accumulated_commission)
    distribution["validator_accumulated_commissions"] = replacement_validator_accumulated_commissions

    # Validator current rewards
    replacement_validator_current_rewards = []
    for validator_current_reward in distribution["validator_current_rewards"]:
        if validator_current_reward["validator_address"] == old_operator_address:
            validator_current_reward["validator_address"] = new_operator_address
            replacement_validator_current_rewards.append(
                validator_current_reward)
    distribution["validator_current_rewards"] = replacement_validator_current_rewards

    # Validator historical rewards
    replacement_validator_historical_rewards = []
    for validator_historical_reward in distribution["validator_historical_rewards"]:
        if validator_historical_reward["validator_address"] == old_operator_address:
            validator_historical_reward["validator_address"] = new_operator_address
            replacement_validator_historical_rewards.append(
                validator_historical_reward)
    distribution["validator_historical_rewards"] = replacement_validator_historical_rewards

    # Signing infos
    slashing["signing_infos"] = []

    # Create final genesis file
    with open("genesis.json", "w", encoding="utf-8") as exportfile:
        json.dump(genesis, exportfile, indent=2,
                  sort_keys=True, ensure_ascii=False)
