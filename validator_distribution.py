import argparse
import logging as log
import numpy as np
import pandas as pd
from datetime import datetime 

from api_requester import BeaconEndpoint
from eth_utils import * 



SLOT_INCREMENT = 64

def generate_active_validator_distribution(args):
    # Parse args
    start_slot = args.start_slot
    finish_slot =  args.finish_slot
    endpoint = args.beacon_endp 
    out_csv = args.csv_path 

    # check connection to the endpoint asking for current head
    beacon_node = BeaconEndpoint(endpoint)
    ok = beacon_node.test_connection()
    if not ok:
        log.info(f"unable to connect to {endpoint}")
        exit(1)

    # request remote head slot
    head, syncing, err = beacon_node.request_head_slot()
    if not err.is_zero():
        log.info(f"unable to retrieve syncing status {err.error}")
        exit(1)
    if syncing:
        log.warn(f"remote endpoint is syncing")
    log.info(f"remote beacon chain's head slot= {head}")
    
    # check if the slot range is valid
    if start_slot <= 0:
        start_slot = 1
    if finish_slot <= 0 or finish_slot > head:
        finish_slot = head
    #
    if finish_slot < start_slot:
        finish_slot = start_slot
    # based on head slot
    if start_slot > head:
        start_slot = head

    log.info(f"fetching distribution of active validators for slot ranges: {start_slot} - {finish_slot}")
    log.info(f"fetching from endpoint: {endpoint}")
    log.info(f"writing results at: {out_csv}")

    ## Arrays
    dist_row = {"time": [], "slot": [], "active_validators": []}

    # request range of slots
    for i in np.arange(start_slot, finish_slot, SLOT_INCREMENT):
        actv_vals, err = beacon_node.get_active_validator_distribution(i)
        if not err.is_zero():
            log.error(f"error retrieving vals for slot {i} - {err.error}")
 
        time = get_time_from_slot(i)
        dist_row["time"].append(datetime.utcfromtimestamp(time).strftime('%Y-%m-%d %H:%M:%S'))
        dist_row["slot"].append(i)
        dist_row["active_validators"].append(actv_vals)

    panda_obj = pd.DataFrame(dist_row)
    panda_obj.to_csv(out_csv)

    log.info("done!")
    print(panda_obj)




if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--beacon-endp",
        help="Endpoint of the BeaconNode API where we will fetch the active validator distribution",
        type=str,
        default="localhost:5052")
    parser.add_argument(
        "--start-slot",
        help="Starting slot to index (-1 to get the number of validators in head slot)",
        type=int,
        default=0)
    parser.add_argument(
        "--finish-slot",
        help="Starting slot to index (-1 to set the finish slot to head slot in the beacon node)",
        type=int,
        default=-1)
    parser.add_argument(
        "--csv-path",
        help="Path to the csv where to store de distribution",
        type=str)

    args = parser.parse_args()
    log.getLogger().setLevel(log.INFO)
    generate_active_validator_distribution(args)


    