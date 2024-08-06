from time import sleep
from confluent_kafka import Consumer, TopicPartition

def consume(config, consumerGroup, consumer_topic):
  config["group.id"] = consumerGroup
  config["auto.offset.reset"] = "latest"
  consumer = Consumer(config)
  consumer.subscribe([consumer_topic])
  consumer.poll(0)
  partitions = consumer.assignment()
  print("Identifying partitions")
  while partitions == []:
    sleep(1)
    consumer.poll(0)
    partitions = consumer.assignment()

  print(f"found {partitions} partitions")
  for p in partitions:
        _, high = consumer.get_watermark_offsets(p)
        consumer.seek(TopicPartition(p.topic, p.partition, high - 1))

  while True:
    msg = consumer.poll(15)
    if msg is not None and msg.error() is None:
      key = msg.key().decode("utf-8")
      value = msg.value()
      print(f"Consumed {len(msg)} bytes with key: {key}: headers: {msg.headers()}")
      return value
    else:
      print(f"Consumed from topic '{consumer_topic}': {msg}")