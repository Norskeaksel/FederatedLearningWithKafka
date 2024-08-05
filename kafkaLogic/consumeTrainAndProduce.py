import pickle

from kafkaLogic.consume import consume
from kafkaLogic.produce import produce
import model

def consumeTrainAndProduce(config, consumerGroup, consumer_topic, producer_topic):
    while True:
      serialized_weights = consume(config, consumerGroup, consumer_topic)
      weights = pickle.loads(serialized_weights)
      new_weights = model.trainModel(weights)
      new_serialized_weights = pickle.dumps(new_weights)
      produce(producer_topic, config, new_serialized_weights)