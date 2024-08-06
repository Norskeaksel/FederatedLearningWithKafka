import pickle

from kafkaLogic.produce import produce
from kafkaLogic.consume import consume
import model

def consumeTrainAndProduce(consumer, producer_topic, config):
  while True:
    msg = consume(consumer)
    try:
      weights = pickle.loads(msg.value())
      new_weights, nr_of_samples = model.trainModel(weights)
      new_serialized_weights = pickle.dumps(new_weights)
    except Exception as e:
      print("Could not prosses wights because of:", e)
      continue

    produce(producer_topic, config, new_serialized_weights, nr_of_samples)
    consumer.commit(asynchronous=False)