# Manager Provison Scripts

## Usage

### Prepare repo

-   Install dependencies:

```bash
pip install -r ../requirements.txt
```

-   Put manager ABI file to the `manager.json` file in the `manager-provision` folder

### List validators

Show validators on manager contract and Minimum Staking Requirement

```bash
python cli.py list-validators [ENDPOINT]
```

Required params:

-   ENDPOINT - RPC endpoint of the node in the network where SKALE Manager is deployed

Optional arguments:

-   `--wei` - Show balances in wei
-   `--all` - Show trusted & untrusted validators

