# Preparing for emoney-1 upgrade

* Install [em-ledger v0.6.5](https://github.com/e-money/em-ledger/tree/v0.6.5) binaries
* Restart emd with `--halt-time 1604494800` to stop the emoney-1 chain on 2020-11-04 at 13:00:00 UTC
* Signal readiness in [PARTICIPANTS.md](PARTICIPANTS.md)

# Generating genesis.json for emoney-2

* Make sure you followed the preparation steps above
* Run `emd export --home <emoney-home> --for-zero-height > emoney-1.export.json`
* Install [em-ledger v0.7.0](https://github.com/e-money/em-ledger/tree/v0.7.0)
* Run `emd migrate emoney-1.export.json > emoney-1.migrated.json`
* Run the state migration script `python3 update-state.py` which generates `genesis.json`

# Optional: Update git reposority
* Finally commit new genesis using `git add -f emoney-1.export.json emoney-1.migrated.json genesis.json && git commit -m "Add emoney-2 genesis"`