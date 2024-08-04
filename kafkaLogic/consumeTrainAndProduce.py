from confluent_kafka import Consumer
import pickle
from kafkaLogic.produce import produce

def consumeTrainAndProduce(config):
  config["group.id"] = "Aksel's consumer v1" # uuid.uuid4().hex
  config["auto.offset.reset"] = "latest"

  consumer_topic = "aggregated_weights_v1"
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
        producer_topic = "client_weights_v1"
        produce(producer_topic, config, pickle.loads(value))
        consumer.commit()
      else:
        print(f"Consumed: {msg}")
  except KeyboardInterrupt:
    pass
  finally:
    consumer.close()