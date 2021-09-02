# lilmermaid-13 Testnet

This testnet is intended to exercise the em-ledger v1.0 releases, containing major changes such as IBC and an upgrade to Cosmos SDK v0.42.

It is based on an [export from the existing emoney-2 mainnet](emoney-2.export.json).

## Faucet

There is a faucet account available that is entirely self-service, with a few conditions:

1) Only take what you need
2) Return what you don't need
3) We'll top up as needed

Use `emd keys add --recover lilmermaid-faucet` to add the faucet account using the below mnemonic:
```
Mnemonic: satisfy select word swamp solar silver flavor sting screen novel deny win tape cement hole embark pact purpose goat latin gesture orange swift maple
Address:  emoney1j7sq6dadld46vruk92r0se0tv0f3uc4pvl4ntd
```

We suggest using the following command to transfer from the faucet:
```
emd tx send lilmermaid-faucet <your-validator> "500000000ungm" --gas-prices "1.0ungm"
```
