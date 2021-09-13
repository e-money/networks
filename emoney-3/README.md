# emoney-3 Mainnet

This directory will contain the official [genesis.json](genesis.json) file for the emoney-3 mainnet.

Below you'll find the instructions for upgrading from emoney-2.

## Preparing for the upgrade from emoney-2

* Install em-ledger [v0.9.6](https://github.com/e-money/em-ledger/releases/tag/v0.9.6) binaries
* Restart emd with `--halt-time 1632142800` to stop the emoney-2 chain on 2021-09-20 at 13:00:00 UTC
* Install Cosmovisor in preparation for future emoney-3 upgrades
* Signal readiness in [PARTICIPANTS.md](PARTICIPANTS.md)

## Generating genesis.json for emoney-3

* Make sure you followed the preparation steps above
* Wait until the halt time has passed and the chain has stopped
* Run `emd export --home <emoney-home> --for-zero-height > emoney-2.export.json`
* Install em-ledger [vX.Y.Z (to be determined)](https://github.com/e-money/em-ledger/releases/tag/vX.Y.Z)
* Run `emd migrate v0.9 emoney-2.export.json --chain-id emoney-3 > genesis.json`

## Optional: Update git reposority
* Finally commit new genesis using `git add -f emoney-2.export.json genesis.json && git commit -m "Add emoney-3 genesis"`

## Optional: Migrate keyring

Since emcli is deprecated the default location of the **file based keyring** has changed as well.

You'll need to copy your keyring from ~/.emcli to ~/.emd, e.g. `cp -vR ~/.emcli/keyring-e-money/ ~/.emd/keyring-file`
