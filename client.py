from confluent_kafka import Producer, Consumer, TopicPartition
# import uuid
import pickle
import model

def read_config():
  env = input("Running client of type: ")
  print(env)
  while env not in {"local", "cloud"}:
    env = input("Please spesify if client is of type 'local' or 'cloud': ")

  config = {}
  with open("config/"+env+"_client.properties") as fh:
    for line in fh:
      line = line.strip()
      if len(line) != 0 and line[0] != "#":
        parameter, value = line.strip().split('=', 1)
        config[parameter] = value.strip()
  return config


def produce(topic, config, received_weights):
  producer = Producer(config)
  key = "key"
  new_weights = model.trainModel(received_weights)
  serialized_weights = pickle.dumps(new_weights)
  print(f"Produceing {len(serialized_weights)} bytes to topic {topic}: key = {key:12}")
  producer.produce(topic, key=key, value=serialized_weights)
  # send any outstanding or buffered messages to the Kafka broker
  producer.flush()
  print(f"{len(serialized_weights)} bytes produced")


def consumeTrainAndProduce(topic, config):
  # sets the consumer group ID and offset  
  config["group.id"] = "Aksel's consumer" # uuid.uuid4().hex
  config["auto.offset.reset"] = "earliest"
  # produce(topic, config, "") # Only needed once. Comment out after produceing weights to the cluster for the first time

  consumer = Consumer(config)
  consumer.subscribe([topic])

  try:
    while True:
      # consumer polls the topic and prints any incoming messages
      msg = consumer.poll(10)
      if msg is not None and msg.error() is None:
        key = msg.key().decode("utf-8")
        value = msg.value()
        print(f"Consumed {len(msg)} bytes with key: {key}")
        produce(topic, config, pickle.loads(value))
        consumer.commit()
  except KeyboardInterrupt:
    pass
  finally:
    consumer.close()

def main():
  config = read_config()
  topic = "recommendation_weights_v1"
  consumeTrainAndProduce(topic, config)


main()