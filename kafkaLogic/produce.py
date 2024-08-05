from confluent_kafka import Producer

def produce(topic, config, serialized_weights):
  producer = Producer(config)
  key = "key"
  print(f"Produceing {len(serialized_weights)} bytes to topic {topic}: key = {key:12}")
  producer.produce(topic, key=key, value=serialized_weights)
  # send any outstanding or buffered messages to the Kafka broker
  producer.flush()
  print(f"{len(serialized_weights)} bytes produced")