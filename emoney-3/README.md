# Preparing for emoney-2 upgrade

* Install em-ledger [v0.9.6](https://github.com/e-money/em-ledger/releases/tag/v0.9.6) binaries
* Restart emd with `--halt-time <TBD>` to stop the emoney-2 chain on YYYY-MM-DD at HH:MM:SS UTC
* Install Cosmovisor in preparation for future emoney-3 upgrades
* Signal readiness in [PARTICIPANTS.md](PARTICIPANTS.md)

# Generating genesis.json for emoney-3

* Make sure you followed the preparation steps above
* Wait until the halt time has passed and the chain has stopped
* Run `emd export --home <emoney-home> --for-zero-height > emoney-2.export.json`
* Install em-ledger [v<TBD>](https://github.com/e-money/em-ledger/releases/tag/v<TBD>)
* Run `emd migrate v0.9 emoney-2.export.json --chain-id emoney-3 > genesis.json`

# Optional: Update git reposority
* Finally commit new genesis using `git add -f emoney-2.export.json genesis.json && git commit -m "Add emoney-3 genesis"`

# See