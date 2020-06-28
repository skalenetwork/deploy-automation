# SM deployment automation

## Usage

`.env` file with variables should be placed in file in project root

### 🚀 FULL PROCEDURE

1) Set values in `.env`

```bash
ENDPOINT=
MANAGER_TAG=
ADDRESS=
ETH_PRIVATE_KEY=
GASPRICE=
PRODUCTION=true/false
NETWORK=mainnet
```

2) Deploy contracts

```bash
python main.py deploy
```

3) Set roles

```bash
python main.py set-roles
```

4) Check contstants

```bash
python main.py check-constants
```

5) Save `artifacts` folder and `role_keys-{DATE}.json` file somewhere!

### Deploy SM contracts

#### Required variables

- `ENDPOINT` - Ethereum network endpoint
- `ETH_PRIVATE_KEY` - Ethereum private key that will be used for deploy
- `MANAGER_TAG` - Tag of the skalenetwork/skale-manager:$MANAGER_TAG container
- `GAS_PRICE` - Gas price for truffle config
- `PRODUCTION` - true/false - type of contracts

```bash
python main.py deploy
```

#### Deployment artifacts

As a result of the successful deployment following files and folders will be generated:

- `abi.json` file with ABIs and addresses off deployed contracts
- `openzeppelin` folder with deployment info
- `build` folder with compiled contracts
- `deploy_data.json` file with info about latest deplyment

Files and folders will be available in the `artifacts` folder.
Save those artifacts to the SM repo after deployment!

### Check address balance

#### Required variables

- `ADDRESS` - Ethereum address

```bash
python main.py balance
```

### Set roles

#### Required variables

- `ENDPOINT` - Ethereum network endpoint
- `ETH_PRIVATE_KEY` - Ethereum private key that will be used for deploy

```bash
python main.py set-roles
```

### Build custom SM container

1. Go to skale-manager repo
2. Run:

```bash
MANAGER_TAG=x.x.x docker build -t skalenetwork/skale-mananager:$MANAGER_TAG .
```
