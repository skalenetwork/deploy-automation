# SM deployment automation

## 

## Usage

`.env` file with variables should be placed in file in project root

### Deploy SM contracts

#### Required variables

- `ENDPOINT` - Ethereum network endpoint
- `ETH_PRIVATE_KEY` - Ethereum private key that will be used for deploy
- `MANAGER_TAG` - Tag of the skalenetwork/skale-manager:$MANAGER_TAG container

```bash
python main.py deploy
```

### Check address balance

#### Required variables

- `ADDRESS` - Ethereum address

```bash
python main.py balance
```
