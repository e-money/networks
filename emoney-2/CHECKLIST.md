# Checklist for generating genesis.json for emoney-2

* Stop validating emoney-1 at block X / time
* Install [em-ledger v0.6.5](https://github.com/e-money/em-ledger/tree/v0.6.5) binaries
* Run `emd export --home <emoney-home> --for-zero-height > emoney-1.export.json`
* Install [em-ledger v0.7.0](https://github.com/e-money/em-ledger/tree/develop)
* Run `emd migrate emoney-1.export.json > emoney-1.migrated.json`
* Run the state migration script `python3 update-state.py` which generates `genesis.json`
* Finally commit new genesis using `git add -f emoney-1.export.json emoney-1.migrated.json genesis.json && git commit -m "Add emoney-2 genesis"`