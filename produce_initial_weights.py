from kafkaLogic.produce import produce
from kafkaLogic.read_config import read_config

config = read_config()
produce("aggregated_weights_v1", config, "") 