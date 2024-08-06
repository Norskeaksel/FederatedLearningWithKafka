import uuid
import pickle
import numpy as np
from kafkaLogic.setupConsumer import setupConsumer
from kafkaLogic.consume import consume
from kafkaLogic.produce import produce
from kafkaLogic.read_config import read_config

def fedAvg(weights, nr_of_samples):
    total_samples = sum(nr_of_samples)
    print(f"Averaging {nr_of_samples} = {total_samples} samples")
    average_weights = []

    # Iterate over each layer's weights
    for weights in zip(*weights):
        # Stack weights along a new dimension and calculate the weighted sum
        weighted_sum = np.sum(
            np.array([weight * num_samples for weight, num_samples in zip(weights, nr_of_samples)]), axis=0
        )
        
        averaged_weight = weighted_sum / total_samples
        average_weights.append(averaged_weight)

    return average_weights

config = read_config()
consumerGroup = str(uuid.uuid4()) # make random to consume from latest each time
consumer_topic = "client_weights_v1"
consumer = setupConsumer(config, consumerGroup, consumer_topic)
producer_topic = "aggregated_weights_v1"

weights = []
nr_of_samples=[]
nr_of_clients = 3
while True:
    msg = consume(consumer)
    consumer.commit(asynchronous=False)
    client_weights = pickle.loads(msg.value())
    header_value = msg.headers()[0][1]
    client_samples = int(header_value.decode('utf-8'))
    
    weights.append(client_weights)
    nr_of_samples.append(client_samples)
    nr_of_received_msg = len(nr_of_samples)
    print(f"Received weights from {nr_of_received_msg}/{nr_of_clients} clients")
    if nr_of_received_msg == nr_of_clients:
        total_samples = sum(nr_of_samples)
        average_weights = fedAvg(weights, nr_of_samples)
        serialized_averaged_weights = pickle.dumps(average_weights)
        produce(producer_topic, config, serialized_averaged_weights, total_samples)
        weights = []
        nr_of_samples=[]



