import json

# This script adapts a genesis file to contain only a single validator.

# Specify the single validator to launch the network (including key replacement)
old_validator_address = "8D8CB9C26740BA74A2AA0ABF9D2BAF98226485A6"
old_operator_address = "osmovaloper1sxx9mszve0gaedz5ld7qdkjkfv8z992a3z2szp"
old_consensus_public_key = "uRUDzQd5POrn/+PUujTx0CvwO6sZxrw0MIEJcgFGCNU="
old_consensus_address = "osmovalcons13kxtnsn8gza8fg42p2le62a0nq3xfpdxxphd7r"
new_validator_address = "7ADE63DE3DBFD3772927FDF319D23994B8323BC2"
new_operator_address = "osmovaloper1sxx9mszve0gaedz5ld7qdkjkfv8z992a3z2szp"
new_consensus_public_key = "+3OXCRCOzcgDcCgLtZn75UVDNtMoV16KnlU6GDUTzxQ="
new_consensus_address = "osmovalcons10t0x8h3ahlfhw2f8lhe3n53ejjuryw7zqkxkyf"

# Process intermediate (migrated) genesis file
with open("osmosis-1.export.json") as importfile:
    genesis = json.load(importfile)

    # Change chain-id
    genesis["chain_id"] = "osclone-1"

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
    replacement_signing_infos = []
    for signing_info in slashing["signing_infos"]:
        if signing_info["address"] == old_consensus_address:
            signing_info["address"] = new_consensus_address
            signing_info["validator_signing_info"]["address"] = new_consensus_address
            replacement_signing_infos.append(signing_info)
    slashing["signing_infos"] = replacement_signing_infos

    # Missed blocks
    replacement_missed_blocks = []
    for missed_block_info in slashing["missed_blocks"]:
        if missed_block_info["address"] == old_consensus_address:
            missed_block_info["address"] = new_consensus_address
            replacement_missed_blocks.append(missed_block_info)
    slashing["missed_blocks"] = replacement_missed_blocks

    # Create final genesis file
    with open("genesis.json", "w", encoding="utf-8") as exportfile:
        json.dump(genesis, exportfile, indent=2,
                  sort_keys=True, ensure_ascii=False)
