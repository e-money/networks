# lilmermaid-13 Testnet

lilmermaid-13 is an incentivised testnet for **existing validators** of the e-Money mainnet.

The goal of the testnet is to ensure that validators are prepared for the mainnet upgrade and are comfortable with the changes from the current mainnet.

There is a faucet account available, see [FAUCET.md](FAUCET.md).


# Testnet rewards

Validators who complete all of the task below will be rewarded with 1000 NGM, to be delivered after the mainnet upgrade to the validator operator account.

The genesis file is based on an [export from the existing emoney-2 mainnet](emoney-2.export.json) with modifications to launch it with a single validator.

Please provide participation proof by making a pull request with changes into the [REWARDS.md](REWARDS.md) file.


## Task 1: Installation

Check list:
* [ ] Install [Cosmovisor](https://github.com/cosmos/cosmos-sdk/tree/master/cosmovisor) and create the appropriate directory structure
* [ ] Install the [v1.0.0-RC9](https://github.com/e-money/em-ledger/releases/tag/v1.0.0-RC9) binaries
* [ ] Initialise software: `emd init...`
* [ ] Copy the [genesis file](https://raw.githubusercontent.com/e-money/networks/master/lilmermaid-13/genesis.json) to `config/`
* [ ] Configure [peers](PEERS.md) in `config/config.toml`
* [ ] Run emd as a service using Cosmovisor

It is suggested to set the following Cosmosvisor environment variables:
```
DAEMON_RESTART_AFTER_UPGRADE=true
DAEMON_ALLOW_DOWNLOAD_BINARIES=false
```

## Task 2: Create validator

Check list:
* [ ] Prepare NGM funding using either the [faucet](FAUCET.md) or use your existing mainnet validator operator account (which was exported into the testnet).
* [ ] Use emd to create the transaction: `emd tx staking create-validator ...`

## Task 3: Create a Market Limit Order

Try `emd tx market add-limit ...` or use the [wallet](https://beta-wallet.e-money.com).

## Task 4: Replace a Market Limit Order

Try `emd tx market cancelreplace ...`.

## Task 5: Cancel a Market  Order

Try `emd tx market cancel ...` or use the [wallet](https://beta-wallet.e-money.com).

## Task 6: Conduct IBC token transfer

More details to follow.

## Task 7: Participate in Upgrade Module test

Check list:
* [ ] Participate in coordination of the upgrade in the [validator hangout group](https://t.me/joinchat/HBB5elfpWv8rADBFhhjbtg).
* [ ] Install the [TBD]() binaries to `cosmovisor/upgrades/upgrade-test-2/binaries`
* [ ] Monitor the validator during the upgrade and confirm it successfully completed at the scheduled height.

## Task 8: Participate in the mainnet upgrade

More details to follow.
