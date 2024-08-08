import pickle
import torch
from kafkaLogic.produce import produce
from recommender_model import Net, load_data, train, get_weights
from kafkaLogic.read_config import read_config


# DEVICE = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
DEVICE = torch.device("cpu")  

net = Net(in_channels=5227, hidden_channels=16, out_channels=1).to(DEVICE)
trainloader, testloader = load_data()
train(net, trainloader, testloader, 1, DEVICE)
weights = get_weights(net)
serialized_weights = pickle.dumps(weights)

config = read_config()
client_topic = "client_weights_v1"
controler_topic = "aggregated_weights_v1"

produce(controler_topic, config, serialized_weights) 