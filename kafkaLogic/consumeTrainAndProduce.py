import pickle
from time import sleep
from confluent_kafka import Consumer, TopicPartition
from kafkaLogic.produce import produce
import model

def consumeTrainAndProduce(config, consumerGroup, consumer_topic, producer_topic):
  config["group.id"] = consumerGroup
  config["auto.offset.reset"] = "latest"
  consumer = Consumer(config)
  consumer.subscribe([consumer_topic])
  consumer.poll(0)
  partitions = _identifyPartitions(consumer)
  for p in partitions:
    _, high = consumer.get_watermark_offsets(p)
    consumer.seek(TopicPartition(p.topic, p.partition, high - 1))
  
  while True:    
    msg = consumer.poll(10)
    if msg is not None and msg.error() is None:
      key = msg.key().decode("utf-8")
      value = msg.value()
      print(f"Consumed {len(msg)} bytes with key: {key}: headers: {msg.headers()}")
      old_weights = pickle.loads(value)

      new_weights, nr_of_samples = model.trainModel(old_weights)
      new_serialized_weights = pickle.dumps(new_weights)
      produce(producer_topic, config, new_serialized_weights, nr_of_samples)
      consumer.commit(asynchronous=False)
    else:
      print(f"Consumed from topic '{consumer_topic}': {msg}")

def _identifyPartitions(consumer):
  print("Identifying partitions")
  partitions = consumer.assignment()
  while partitions == []:
    sleep(1)
    consumer.poll(0)
    partitions = consumer.assignment()
  print(f"found {partitions} partitions")
  return partitions
