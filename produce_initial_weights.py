import pickle
from kafkaLogic.produce import produce
from kafkaLogic.read_config import read_config
import model

config = read_config()
weights, nr_of_samples = model.trainModel(None)
serialized_weights = pickle.dumps(weights)
client_topic = "client_weights_v1"
controler_topic = "aggregated_weights_v1"

produce(controler_topic, config, serialized_weights, nr_of_samples) 