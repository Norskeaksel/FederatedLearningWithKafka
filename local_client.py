from confluent_kafka import Producer, Consumer
# from keras.datasets import mnist

config = {
    'bootstrap.servers': 'localhost:29092',
    'client.id': 'python-producer',
    'security.protocol': 'PLAINTEXT',
}

def produce(topic, config):
  producer = Producer(config)
  
  # produces a sample message
  key = "key"
  value = "value"
  producer.produce(topic, key=key, value=value)
  print(f"Produced message to topic {topic}: key = {key:12} value = {value:12}")
  producer.flush()

def consume(topic, config):
  config["group.id"] = "python-group-1"
  config["auto.offset.reset"] = "earliest"
  consumer = Consumer(config)
  consumer.subscribe([topic])

  try:
    while True:
      # consumer polls the topic and prints any incoming messages
      msg = consumer.poll(1.0)
      if msg is not None and msg.error() is None:
        key = msg.key().decode("utf-8")
        value = msg.value().decode("utf-8")
        print(f"Consumed message from topic {topic}: key = {key:12} value = {value:12}")
  except KeyboardInterrupt:
    pass
  finally:
    consumer.close()

def main():
  topic = "recommendation_weights"

  produce(topic, config)
  consume(topic, config)


main()