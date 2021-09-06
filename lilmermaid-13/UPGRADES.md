# Upgrade History

The below table can be used with [Cosmovisor](https://github.com/cosmos/cosmos-sdk/tree/master/cosmovisor) to ensure a node can sync from genesis.

| Upgrade Name   | Version                                                                      | Install Path                       | Notes                                                          |
| -------------- | ---------------------------------------------------------------------------- | ---------------------------------- | -------------------------------------------------------------- |
| -              | [v1.0.0-RC6](https://github.com/e-money/em-ledger/releases/tag/v1.0.0-RC6)   | cosmovisor/genesis/bin             | Used at genesis                                                |
| **v1.0.0-RC7** | [v1.0.0-RC9](https://github.com/e-money/em-ledger/releases/tag/v1.0.0-RC9)   | cosmovisor/upgrades/v1.0.0-RC7/bin | The upgrade-plan was named `v1.0.0-RC7` for historical reasons |
| **hotfix-2**   | [v1.0.0-RC10](https://github.com/e-money/em-ledger/releases/tag/v1.0.0-RC10) | cosmovisor/upgrades/hotfix-2/bin   | Minor fix to get IBC working                                   |
