import uuid
from kafkaLogic.consumeTrainAndProduce import consumeTrainAndProduce
from kafkaLogic.read_config import read_config


def main():
  config = read_config()
  consumerGroup = str(uuid.uuid4()) # "Aksel's client v4"
  consumer_topic = "aggregated_weights_v1"
  producer_topic = "client_weights_v1"
  
  consumeTrainAndProduce(config, consumerGroup, consumer_topic, producer_topic)


if __name__ == "__main__":
    main()