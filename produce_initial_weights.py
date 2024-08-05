import pickle
from kafkaLogic.produce import produce
from kafkaLogic.read_config import read_config
import model

config = read_config()
weights = model.trainModel("")
serialized_weights = pickle.dumps(weights)
produce("aggregated_weights_v1", config, serialized_weights) 