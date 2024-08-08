import pickle
from kafkaLogic.setupConsumer import setupConsumer, seekToNPreviousOffset
from kafkaLogic.consume import consume
from kafkaLogic.produce import produce
from kafkaLogic.read_config import read_config

nr_of_clients = 3
def fedAvg(clients_weights, nr_of_samples):
    average_weights = []
    total_samples = sum(nr_of_samples)
    for weight_set in zip(*clients_weights):
        weighted_sum = sum(weight_set[i] * nr_of_samples[i] for i in range(nr_of_clients))
        averaged_weights = weighted_sum / total_samples
        average_weights.append(averaged_weights)

    return average_weights

def main():
    config = read_config()
    consumerGroup = "Global controller"
    consumer_topic = "client_weights_v1"
    consumer = setupConsumer(config, consumerGroup, consumer_topic)
    seekToNPreviousOffset(consumer, 0)
    producer_topic = "aggregated_weights_v1"

    weights = []
    nr_of_samples=[]
    try:
        while True:
            msg = consume(consumer)
            consumer.commit(asynchronous=False)
            client_weights = pickle.loads(msg.value())
            header_value = msg.headers()[0][1]
            client_samples = int(header_value.decode('utf-8'))
            
            weights.append(client_weights)
            nr_of_samples.append(client_samples)
            nr_of_received_msg = len(nr_of_samples)
            print(f"Received weights from client {nr_of_received_msg}/{nr_of_clients}")
            if nr_of_received_msg == nr_of_clients:
                total_samples = sum(nr_of_samples)
                average_weights = fedAvg(weights, nr_of_samples)
                serialized_averaged_weights = pickle.dumps(average_weights)
                produce(producer_topic, config, serialized_averaged_weights, total_samples)
                weights = []
                nr_of_samples=[]
    except KeyboardInterrupt:
        pass
    finally:
        consumer.close() # Clean shutdown of consumer to let other instances of the controler to take over

if __name__ == "__main__":
    main()