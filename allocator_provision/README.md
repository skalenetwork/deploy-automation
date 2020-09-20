# Allocator Provison Scripts

## Usage

### Prepare repo

1) Install dependencies:

```bash
pip install -r ../requirements.txt
```

2) Download csv files with plans and beneficiates
3) Put allocator ABI file to the `allocator.json` file in the `allocator-provision` folder

### Create plans

Create plans from the provided CSV file

```bash
python cli.py create-plans [PK_FILE] [CSV_FILEPATH]
```

Required params:

1) PK_FILE - Path to file with private key
2) CSV_FILEPATH - Path to CSV file with plans

Optional arguments:

-   `--dry-run` - Show plans that will be created without actual trnasctions
-   `--endpoint` - RPC endpoint of the node in the network where SKALE Allocator is deployed

### Add beneficiates

Add beneficiates to the plans and deploy Escrows

```bash
python cli.py add-beneficiates [PK_FILE] [CSV_FILEPATH]
```

Required params:

1) PK_FILE - Path to file with private key
2) CSV_FILEPATH - Path to CSV file with beneficiates

Optional arguments:

-   `--dry-run` - Show plans that will be created without actual trnasctions
-   `--endpoint` - RPC endpoint of the node in the network where SKALE Allocator is deployed

### Approve transfers

Approve batch of transfers

> `manager.json` file should be in the `allocator_provision` folder!

```bash
python cli.py approve-transfers --endpoint [ENDPOINT] [CHUNK_LENGTH] [PK_FILEPATH] [CSV_FILEPATH]
```

Required params:

1) PK_FILE - Path to file with private key
2) CSV_FILEPATH - Path to CSV file with beneficiates

Arguments:

-  `--endpoint` - RPC endpoint of the node in the network where SKALE Manager is deployed

### Verify transfers

Verify complete transfers

> `manager.json` file should be in the `allocator_provision` folder!

```bash
cli.py verify-transfers --endpoint [ENDPOINT] [CSV_FILEPATH]
```

Required params:

1) CSV_FILEPATH - Path to CSV file with beneficiates

Arguments:

-  `--endpoint` - RPC endpoint of the node in the network where SKALE Allocator is deployed
