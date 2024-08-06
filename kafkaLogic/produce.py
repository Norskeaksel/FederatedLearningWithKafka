from confluent_kafka import Producer

def produce(topic, config, serialized_weights, sample_nr):
  producer = Producer(config)
  key = "key"
  sample_nr_binary = str(sample_nr).encode('utf-8')
  headers=("sample_nr", sample_nr_binary)
  print(f"Produceing {len(serialized_weights)} bytes to topic {topic}: key = {key:12}: headers: {headers}")
  producer.produce(topic=topic,
                   key=key,
                   value=serialized_weights), 
                   #headers=headers)
  # send any outstanding or buffered messages to the Kafka broker
  producer.flush()
  print(f"{len(serialized_weights)} bytes produced")