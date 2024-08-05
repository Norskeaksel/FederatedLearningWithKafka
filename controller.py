import uuid
from kafkaLogic.consumeTrainAndProduce import consumeTrainAndProduce
from kafkaLogic.read_config import read_config


config = read_config()
consumerGroup = str(uuid.uuid4()) # make random to consume from latest each time
consumer_topic = "client_weights_v1"
producer_topic = "aggregated_weights_v1"

consumeTrainAndProduce(config, consumerGroup, consumer_topic, producer_topic)