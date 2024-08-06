from confluent_kafka import Consumer, TopicPartition
from time import sleep

def setupConsumer(config, consumerGroup, consumer_topic):
  config["group.id"] = consumerGroup
  config["auto.offset.reset"] = "latest"
  consumer = Consumer(config)
  consumer.subscribe([consumer_topic])
  return consumer


def seekToLatestOffset(consumer):
  print("Identifying partitions")
  partitions = consumer.assignment()
  while partitions == []:
    sleep(1)
    consumer.poll(0)
    partitions = consumer.assignment()
  print(f"found {partitions} partitions")
  for p in partitions:
    _, high = consumer.get_watermark_offsets(p)
    consumer.seek(TopicPartition(p.topic, p.partition, high - 1))