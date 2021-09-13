# lilmermaid-16 Testnet

lilmermaid-16 is an incentivised testnet for **existing validators** of the e-Money mainnet.

The goal of the testnet is to ensure that validators are prepared for the mainnet upgrade and are comfortable with the changes from the current mainnet. See [CHANGELOG.md](https://github.com/e-money/em-ledger/blob/develop/CHANGELOG.md) for major changes.

There is a faucet account available, see [FAUCET.md](FAUCET.md).


# Testnet Rewards

Validators who complete all of the task below will be rewarded with 1000 NGM, to be delivered after the mainnet upgrade to the validator operator account.

The genesis file is based on an [export from the existing emoney-2 mainnet](emoney-2.export.json) with modifications to launch it with a single validator.

Please provide participation proof by making a pull request with changes into the [REWARDS.md](REWARDS.md) file.


## Task 1: Installation

Check list:
* [ ] Install [Cosmovisor](https://github.com/cosmos/cosmos-sdk/tree/master/cosmovisor) and create the appropriate directory structure
* [ ] Use [UPGRADES.md](UPGRADES.md) to install the emd binaries in the appropriate location
* [ ] Initialise software: `cosmovisor/genesin/bin/emd init...`
* [ ] Copy the [genesis file](genesis.json) to `config/`
* [ ] Configure [peers](PEERS.md) in `config/config.toml`
* [ ] Run emd as a service using Cosmovisor with `--x-crisis-skip-assert-invariants`

It is suggested to set the following Cosmosvisor environment variables:
```
DAEMON_RESTART_AFTER_UPGRADE=true
DAEMON_ALLOW_DOWNLOAD_BINARIES=false
```

## Task 2: Create Validator

Check list:
* [ ] Prepare NGM funding using either the [faucet](FAUCET.md) or use your existing mainnet validator operator account (which was exported into the testnet).
* [ ] Use emd to create the transaction: `emd tx staking create-validator ...`

## Task 3: Create a Market Limit Order

Try `emd tx market add-limit ...` or use the [wallet](https://beta-wallet.e-money.com).

## Task 4: Replace a Market Limit Order

Try `emd tx market cancelreplace ...`.

## Task 5: Cancel a Market Order

Try `emd tx market cancel ...` or use the [wallet](https://beta-wallet.e-money.com).

## Task 6: Conduct IBC Transfer

Try sending tokens to [osclone-1 chain](../osclone-1/README.md) using `emd tx ibc-transfer transfer transfer channel-0 osmo1... 123456ungm`.

## Task 7: Participate in Upgrade Module Test

Check list:
* [ ] Await coordination of the upgrade in the [validator hangout group](https://t.me/joinchat/HBB5elfpWv8rADBFhhjbtg).
* [ ] Install the [TBD]() binaries to `cosmovisor/upgrades/upgrade-test-1/binaries`
* [ ] Monitor the validator during the upgrade and confirm it successfully completed at the scheduled height.

## Task 8: Participate in the Mainnet Upgrade

Check list:
* [ ] Perform the preparation steps in [emoney-3/README.md](../emoney-3/README.md#preparing-for-the-upgrade-from-emoney-2)
* [ ] Signal readiness in [emoney-3/PARTICIPANTS.md](../emoney-3/PARTICIPANTS.md)
* [ ] Participate in the emoney-3 mainnet upgrade on 2021-09-20 at 13:00:00 UTC
