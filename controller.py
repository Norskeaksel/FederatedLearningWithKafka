import uuid
from kafkaLogic.consumeTrainAndProduce import consumeTrainAndProduce
from kafkaLogic.read_config import read_config


config = read_config()
consumerGroup = uuid.uuid4().hex # TODO make this consume
consumer_topic = "client_weights_v1"
producer_topic = "aggregated_weights_v1"

consumeTrainAndProduce(config, consumerGroup, consumer_topic, producer_topic)