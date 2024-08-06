def consume(consumer):
  while True:
    msg = consumer.poll(10)
    if msg is not None and msg.error() is None:
      key = msg.key().decode("utf-8")
      value = msg.value()
      print(f"Consumed {len(value)} bytes with key: {key}: headers: {msg.headers()}")
      return msg
    else:
      print(f"Consumed: {msg}")