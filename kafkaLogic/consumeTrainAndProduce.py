import pickle

from kafkaLogic.produce import produce
from kafkaLogic.consume import consume
from recommender_model import Net, load_data, train, set_weights
import torch

# DEVICE = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
DEVICE = torch.device("cpu")

def consumeTrainAndProduce(consumer, producer_topic, config):
  net = Net(in_channels=5227, hidden_channels=16, out_channels=1).to(DEVICE)
  trainloader, testloader = load_data()
  while True:
    msg = consume(consumer)
    try:
      weights = pickle.loads(msg.value())
      set_weights(net, weights)
      new_weights, nr_of_samples = train(net, trainloader, testloader, 1, DEVICE) # model.trainModel(weights)
      new_serialized_weights = pickle.dumps(new_weights)
    except Exception as e:
      print("Could not prosses wights because of:", e)
      continue

    produce(producer_topic, config, new_serialized_weights, nr_of_samples)
    consumer.commit(asynchronous=False)