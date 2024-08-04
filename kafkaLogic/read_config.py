def read_config():
  env = input("Running client of type: ")
  print(env)
  while env not in {"local", "cloud"}:
    env = input("Please spesify if client is of type 'local' or 'cloud': ")

  config = {}
  with open("kafkaLogic/config/"+env+"_client.properties") as fh:
    for line in fh:
      line = line.strip()
      if len(line) != 0 and line[0] != "#":
        parameter, value = line.strip().split('=', 1)
        config[parameter] = value.strip()
  return config