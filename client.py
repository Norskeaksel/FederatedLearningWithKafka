from confluent_kafka import Producer, Consumer
# from keras.datasets import mnist

def read_config():
  env = input("Running client of type: ")
  print(env)
  while env not in {"local", "cloud"}:
    env = input("Please spesify if client is of type 'local' or 'cloud': ")

  config = {}
  with open(env+"_client.properties") as fh:
    for line in fh:
      line = line.strip()
      if len(line) != 0 and line[0] != "#":
        parameter, value = line.strip().split('=', 1)
        config[parameter] = value.strip()
  return config

def produce(topic, config):
  producer = Producer(config)

  # produces a sample message
  key = "key"
  value = "value"
  producer.produce(topic, key=key, value=value)
  print(f"Produced message to topic {topic}: key = {key:12} value = {value:12}")

  # send any outstanding or buffered messages to the Kafka broker
  producer.flush()

def consume(topic, config):
  # sets the consumer group ID and offset  
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
        break
  except KeyboardInterrupt:
    pass
  finally:
    consumer.close()

def main():
  config = read_config()
  topic = "recommendation_weights"

  produce(topic, config)
  consume(topic, config)


main()