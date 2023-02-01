# Ethereum Consensus Layer Sniffer (Python)
Set of scripts that allow indexing in CSV different stats or data from the Ethereum Consensus Layer. 

## Install
Install first the requirements doing:
```
pip3 install -r requirements.txt
```

## Supported calls

#### Validator Distribution

Index the active validator distribution of the desired slot range. 
```
usage: validator_distribution.py [-h] [--beacon-endp BEACON_ENDP] [--start-slot START_SLOT] [--finish-slot FINISH_SLOT] [--csv-path CSV_PATH]

optional arguments:
  -h, --help            show this help message and exit
  --beacon-endp BEACON_ENDP
                        Endpoint of the BeaconNode API where we will fetch the active validator distribution
  --start-slot START_SLOT
                        Starting slot to index (-1 to get the number of validators in head slot)
  --finish-slot FINISH_SLOT
                        Starting slot to index (-1 to set the finish slot to head slot in the beacon node)
  --csv-path CSV_PATH   Path to the csv where to store de distribution
```