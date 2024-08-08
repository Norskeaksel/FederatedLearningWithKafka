import pickle
import torch
import time
from kafkaLogic.produce import produce
from kafkaLogic.consume import consume
from recommender_model import Net, load_data, train, set_weights, get_weights


# DEVICE = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
DEVICE = torch.device("cpu")

def consumeTrainAndProduce(consumer, consumer_group, producer_topic, config):
  net = Net(in_channels=5227, hidden_channels=16, out_channels=1).to(DEVICE)
  trainloader, testloader = load_data()
  rounds = 10
  round_nr = 0
  for _ in range(rounds):
    msg = consume(consumer)
    try:
      received_time = time.time()
      if round_nr == 0:
        with open('epoch_times.log', 'a') as log_file:
          log_file.write("ClientName,epocTime,sendOrReceived,RoundNr\n")
      else:
        with open('epoch_times.log', 'a') as log_file:
          log_file.write(f"{consumer_group},{received_time},received,{round_nr}\n")
      
      round_nr += 1
      weights = pickle.loads(msg.value())
      set_weights(net, weights)
      #new_weights, nr_of_samples = trainModel(weights)
      results, net = train(net, trainloader, testloader, 1, DEVICE)
      print(results)
      new_weights = get_weights(net)
      new_serialized_weights = pickle.dumps(new_weights)
    except Exception as e:
      print("Could not prosses wights because of:", e)
      continue
    
    sending_time = time.time()
    if round_nr < rounds:
      with open('epoch_times.log', 'a') as log_file:
        log_file.write(f"{consumer_group},{sending_time},send,{round_nr}\n")
    produce(producer_topic, config, new_serialized_weights)
    consumer.commit(asynchronous=False)
  
  consumer.close()