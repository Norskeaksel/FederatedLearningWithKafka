from confluent_kafka import Producer
import model
import pickle

def produce(topic, config, weights):
  producer = Producer(config)
  key = "key"
  new_weights = model.trainModel(weights)
  serialized_weights = pickle.dumps(new_weights)
  print(f"Produceing {len(serialized_weights)} bytes to topic {topic}: key = {key:12}")
  producer.produce(topic, key=key, value=serialized_weights)
  # send any outstanding or buffered messages to the Kafka broker
  producer.flush()
  print(f"{len(serialized_weights)} bytes produced")