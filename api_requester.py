import requests
import json

REQUEST_TIMEOUT = 10 # 10 secs seems to be enough
HTTP_SUCCESS_CODE = 200

class Error():
    exists = False
    error = ""

    def __init__(self, exists:bool, error:str):
        self.exists = exists
        self.error = error

    def is_zero(self):
        return not self.exists

    def __str__(self):
        return self.error

class BeaconEndpoint():
    # define the enpoints
    api_queries = {
        "syncing": "/eth/v1/node/syncing",
        "active-validators": "/eth/v1/beacon/states/[_slot_]/validators",
    }

    def __init__(self, endp:str):
        self.beacon_endpoint = endp

    def make_api_request(self, query:str):
        res = requests.get(query, timeout=REQUEST_TIMEOUT)
        if res.status_code != HTTP_SUCCESS_CODE:
            error = Error(True, res.status_code)
            return res, error
        result = json.loads(res.text)
        error = Error(False, res.status_code)
        return result["data"], error

    def test_connection(self) -> bool:
        # ask if the remote node is syncing
        _, _, ok = self.request_head_slot()
        return ok

    def compose_query(self, query, attr) -> str:
        base = f'http://{self.beacon_endpoint}'
        req_query = self.api_queries[query]
        for key in attr:
            req_query = req_query.replace(f'[_{key}_]', str(attr[key]))
        return base + req_query
   

    def request_head_slot(self):
        query = self.compose_query("syncing", {})
        res, err = self.make_api_request(query)
        if not err.is_zero():
            return -1, False, err
        b_head_slot = res["head_slot"]
        syncing = res["is_syncing"] 
        return int(b_head_slot), syncing, err

    def get_active_validator_distribution(self, slot:int):
        # compose query
        query = self.compose_query("active-validators", {"slot": slot})
        res, err = self.make_api_request(query)
        if not err.is_zero():
            return -1, False, err
        # we only consider as "active" the ones with the "active_ongoing"
        active_validator_cnt = 0
        for item in res:
            if item["status"] == "active_ongoing" or item["status"] == "active" or item["status"] == "active":
                active_validator_cnt += 1
        return active_validator_cnt, err

