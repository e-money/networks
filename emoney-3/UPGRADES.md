# Upgrade History

The below table can be used with [Cosmovisor](https://github.com/cosmos/cosmos-sdk/tree/main/tools/cosmovisor) to ensure a node can sync from genesis.

| Upgrade Plan | Earliest Deployment Time | Version                                                            | Install Path           | Notes           |
| ------------ | ------------------------ | ------------------------------------------------------------------ | ---------------------- | --------------- |
| -            | Genesis                  | [v1.1.0](https://github.com/e-money/em-ledger/releases/tag/v1.1.0) | cosmovisor/genesis/bin | Run with --halt-height=1485285 |
| -            | Height 1485286           | [v1.2.0](https://github.com/e-money/em-ledger/releases/tag/v1.2.0) | cosmovisor/genesis/bin | Addresses [Dragonberry](https://forum.cosmos.network/t/ibc-security-advisory-dragonberry/7702) security advisory. |