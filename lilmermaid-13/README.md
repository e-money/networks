# lilmermaid-13 Testnet

lilmermaid-13 is an incentivised testnet for **existing validators** of the e-Money mainnet.

The goal of the testnet is to ensure that validators are prepared for the mainnet upgrade and are comfortable with the changes from the current mainnet.

There is a faucet account available, see [FAUCET.md](FAUCET.md).


# Testnet rewards

Validators who complete all of the task below will be rewarded with xxxx NGM, to be delivered after the mainnet upgrade to the validator operator account.

The genesis file is based on an [export from the existing emoney-2 mainnet](emoney-2.export.json) with modifications to launch it with a single validator.

Please provide participation proof by making a pull request with changes into the [REWARDS.md](REWARDS.md).


## Task 1: Installation

Check list:
* [ ] Install [Cosmovisor](https://github.com/cosmos/cosmos-sdk/tree/master/cosmovisor) and create the appropriate directory structure
* [ ] Install the [v1.0.0-RC7](https://github.com/e-money/em-ledger/releases/tag/v1.0.0-RC7) binaries
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


## Task X: Create a Market Limit Order


## Task X: Replace a Market Limit Order


## Task X: Cancel a Market Limit Order


## Task X: Participate in the mainnet upgrade

