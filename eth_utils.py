# base utils/defaults from the Ethereum network

SLOT_PER_EPOCH = 32
SLOT_TIME = 12 # 12 seconds
GENESIS_TIME = 1606824000 # (Dec 1, 2020, 12pm UTC)

def get_time_from_slot(slot):
    return GENESIS_TIME + (SLOT_TIME * slot) 



    