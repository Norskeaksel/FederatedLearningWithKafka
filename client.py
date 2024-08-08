import uuid
from kafkaLogic.setupConsumer import setupConsumer, seekToNPreviousOffset
from kafkaLogic.consumeTrainAndProduce import consumeTrainAndProduce
from kafkaLogic.read_config import read_config


def main():
  config = read_config()
  consumer_group = uuid.uuid4().hex # "Aksel's client v4"
  consumer_topic = "aggregated_weights_v1"
  consumer = setupConsumer(config, consumer_group, consumer_topic)
  seekToNPreviousOffset(consumer, 1)

  producer_topic = "client_weights_v1"
  consumeTrainAndProduce(consumer,consumer_group, producer_topic, config)
  
if __name__ == "__main__":
    main()