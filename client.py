import uuid
from kafkaLogic.setupConsumer import setupConsumer, seekToLatestOffset
from kafkaLogic.consumeTrainAndProduce import consumeTrainAndProduce
from kafkaLogic.read_config import read_config


def main():
  config = read_config()
  consumerGroup = str(uuid.uuid4()) # "Aksel's client v4"
  consumer_topic = "aggregated_weights_v1"
  consumer = setupConsumer(config, consumerGroup, consumer_topic)
  seekToLatestOffset(consumer)

  producer_topic = "client_weights_v1"
  consumeTrainAndProduce(consumer, producer_topic, config)
  
if __name__ == "__main__":
    main()