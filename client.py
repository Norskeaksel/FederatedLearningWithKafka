from kafkaLogic.consumeTrainAndProduce import consumeTrainAndProduce
from kafkaLogic.read_config import read_config


def main():
  config = read_config()
  consumerGroup = "Aksel's client v1"
  consumer_topic = "aggregated_weights_v1"
  producer_topic = "client_weights_v1"
  
  consumeTrainAndProduce(config, consumerGroup, consumer_topic, producer_topic)


if __name__ == "__main__":
    main()