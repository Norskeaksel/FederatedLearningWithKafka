from confluent_kafka import Consumer

def consume(config, consumerGroup, consumer_topic):
  config["group.id"] = consumerGroup
  config["auto.offset.reset"] = "latest"
  consumer = Consumer(config)
  consumer.subscribe([consumer_topic])

  try:
    while True:
      # consumer polls the topic and prints any incoming messages
      msg = consumer.poll(10)
      if msg is not None and msg.error() is None:
        key = msg.key().decode("utf-8")
        value = msg.value()
        print(f"Consumed {len(msg)} bytes with key: {key}")
        return value
      else:
        print(f"Consumed from topic '{consumer_topic}': {msg}")
  except KeyboardInterrupt:
    pass
  finally:
    consumer.close()