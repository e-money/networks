# osclone-1 Testnet

osclone-1 is an internal testnet used to test IBC integration with Osmosis.

The genesis file is based on an [export from the existing osmosis-1 mainnet](osmosis-1.export.json) with modifications to launch it with a single validator.

Note: osmosisd must be run with `--x-crisis-skip-assert-invariants`. 