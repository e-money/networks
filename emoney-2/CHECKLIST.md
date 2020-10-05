# Checklist for generating genesis.json for emoney-2

* Stop validating emoney-1 at block X / time
* Install [em-ledger v0.6.5](https://github.com/e-money/em-ledger/tree/v0.6.5) binaries
* Run `emd export --home <emoney-home> --for-zero-height > emoney-1.export.json`
* Install [em-ledger v0.7.0](https://github.com/e-money/em-ledger/tree/develop)
* run `emd migrate emoney-1.export.json > emoney-1.migrated.json`
* Finally, run the state migration script `python3 update-state.py` which generates `genesis.json`
