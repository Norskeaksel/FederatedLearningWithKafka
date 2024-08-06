import uuid
import pickle
import numpy as np
from kafkaLogic.setupConsumer import setupConsumer
from kafkaLogic.consume import consume
from kafkaLogic.produce import produce
from kafkaLogic.read_config import read_config

nr_of_clients = 3 # Adjust the number of "weight_set[1] * nr_of_samples[1]" lines to match this number
def fedAvg(clients_weights, nr_of_samples):
    average_weights = []
    for weight_set in zip(*clients_weights):
        weighted_sum = (
            weight_set[0] * nr_of_samples[0]
            + weight_set[1] * nr_of_samples[1]
            + weight_set[2] * nr_of_samples[2]
        )
        averaged_weights = weighted_sum / total_samples
        average_weights.append(averaged_weights)

    return average_weights


config = read_config()
consumerGroup = str(uuid.uuid4()) # make random to consume from latest each time
consumer_topic = "client_weights_v1"
consumer = setupConsumer(config, consumerGroup, consumer_topic)
producer_topic = "aggregated_weights_v1"

weights = []
nr_of_samples=[]
while True:
    msg = consume(consumer)
    consumer.commit(asynchronous=False)
    client_weights = pickle.loads(msg.value())
    header_value = msg.headers()[0][1]
    client_samples = int(header_value.decode('utf-8'))
    
    weights.append(client_weights)
    nr_of_samples.append(client_samples)
    nr_of_received_msg = len(nr_of_samples)
    print(f"Received weights from client {nr_of_received_msg}/{nr_of_clients} with length {len(client_weights)}")
    if nr_of_received_msg == nr_of_clients:
        total_samples = sum(nr_of_samples)
        average_weights = fedAvg(weights, nr_of_samples)
        serialized_averaged_weights = pickle.dumps(average_weights)
        produce(producer_topic, config, serialized_averaged_weights, total_samples)
        weights = []
        nr_of_samples=[]



