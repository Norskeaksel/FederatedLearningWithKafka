import torch
from torch_geometric.loader import DataLoader
import torch.nn.functional as F

class FederatedClient:
    def __init__(self, model, data_loader, lr=0.01):
        self.model = model
        self.data_loader = data_loader
        self.optimizer = torch.optim.Adam(self.model.parameters(), lr=lr)
        self.criterion = torch.nn.MSELoss()
    
    def train(self, epochs=1):
        """ Train the model on local data """
        self.model.train()
        for epoch in range(epochs):
            for batch in self.data_loader:
                self.optimizer.zero_grad()
                out = self.model(batch)
                loss = self.criterion(out, batch.edge_attr.view(-1, 1))
                loss.backward()
                self.optimizer.step()
            print(f'Client Epoch {epoch + 1}, Loss: {loss.item()}')

    def evaluate(self, data_loader):
        """ Evaluate the model on a given data loader """
        self.model.eval()
        total_loss = 0
        with torch.no_grad():
            for batch in data_loader:
                out = self.model(batch)
                loss = self.criterion(out, batch.edge_attr.view(-1, 1))
                total_loss += loss.item()
        return total_loss / len(data_loader)

    def get_model(self):
        return self.model
    
    def get_gradients(self):
        """ Get the gradients of the model parameters """
        gradients = {}
        for name, param in self.model.named_parameters():
            if param.grad is not None:
                gradients[name] = param.grad.mean().item()
        return gradients

import torch
from collections import OrderedDict

class FederatedServer:
    def __init__(self, model, num_clients, lr=0.01):
        self.model = model
        self.num_clients = num_clients
        self.lr = lr
        self.optimizer = torch.optim.Adam(self.model.parameters(), lr=self.lr)

    def aggregate(self, client_models):
        """ Aggregate model parameters from clients """
        state_dicts = [client_model.state_dict() for client_model in client_models]
        average_state_dict = OrderedDict()

        for key in state_dicts[0].keys():
            average_state_dict[key] = torch.mean(
                torch.stack([state_dict[key].float() for state_dict in state_dicts]), dim=0
            )
        
        self.model.load_state_dict(average_state_dict)
    
    def evaluate(self, test_loader):
        """ Evaluate the global model """
        self.model.eval()
        total_loss = 0
        with torch.no_grad():
            for batch in test_loader:
                out = self.model(batch)
                loss = F.mse_loss(out, batch.edge_attr.view(-1, 1))
                total_loss += loss.item()
        return total_loss / len(test_loader)
    
    def get_gradients(self):
        """ Get the gradients of the global model parameters """
        gradients = {}
        for name, param in self.model.named_parameters():
            if param.grad is not None:
                gradients[name] = param.grad.mean().item()
        return gradients

import torch
from torch_geometric.data import Data, DataLoader
from torch_geometric.nn import GCNConv
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
import torch.nn.functional as F

# Define the GCN model
class GCN(torch.nn.Module):
    def __init__(self, in_channels, hidden_channels, out_channels):
        super(GCN, self).__init__()
        self.conv1 = GCNConv(in_channels, hidden_channels)
        self.conv2 = GCNConv(hidden_channels, hidden_channels)
        self.fc = torch.nn.Linear(hidden_channels * 2, out_channels)

    def forward(self, data):
        x, edge_index = data.x, data.edge_index
        x = self.conv1(x, edge_index)
        x = F.relu(x)
        x = self.conv2(x, edge_index)
        x = F.relu(x)
        edge_pred = self.fc(torch.cat([x[edge_index[0]], x[edge_index[1]]], dim=1))
        return edge_pred.squeeze()

# Define the Federated Client class
class FederatedClient:
    def __init__(self, model, data_loader, lr=0.01):
        self.model = model
        self.data_loader = data_loader
        self.optimizer = torch.optim.Adam(self.model.parameters(), lr=lr)
        self.criterion = torch.nn.MSELoss()
    
    def train(self, epochs=1):
        """ Train the model on local data """
        self.model.train()
        for epoch in range(epochs):
            for batch in self.data_loader:
                self.optimizer.zero_grad()
                out = self.model(batch)
                loss = self.criterion(out, batch.edge_attr.view(-1, 1))
                loss.backward()
                self.optimizer.step()
            print(f'Client Epoch {epoch + 1}, Loss: {loss.item()}')

    def evaluate(self, data_loader):
        """ Evaluate the model on a given data loader """
        self.model.eval()
        total_loss = 0
        with torch.no_grad():
            for batch in data_loader:
                out = self.model(batch)
                loss = self.criterion(out, batch.edge_attr.view(-1, 1))
                total_loss += loss.item()
        return total_loss / len(data_loader)

    def get_model(self):
        return self.model
    
    def get_gradients(self):
        """ Get the gradients of the model parameters """
        gradients = {}
        for name, param in self.model.named_parameters():
            if param.grad is not None:
                gradients[name] = param.grad.mean().item()
        return gradients

# Define the Federated Server class
class FederatedServer:
    def __init__(self, model, num_clients, lr=0.01):
        self.model = model
        self.num_clients = num_clients
        self.lr = lr
        self.optimizer = torch.optim.Adam(self.model.parameters(), lr=self.lr)

    def aggregate(self, client_models):
        """ Aggregate model parameters from clients """
        state_dicts = [client_model.state_dict() for client_model in client_models]
        average_state_dict = {key: torch.mean(torch.stack([state_dict[key].float() for state_dict in state_dicts]), dim=0) for key in state_dicts[0]}
        self.model.load_state_dict(average_state_dict)
    
    def evaluate(self, test_loader):
        """ Evaluate the global model """
        self.model.eval()
        total_loss = 0
        with torch.no_grad():
            for batch in test_loader:
                out = self.model(batch)
                loss = F.mse_loss(out, batch.edge_attr.view(-1, 1))
                total_loss += loss.item()
        return total_loss / len(test_loader)
    
    def get_gradients(self):
        """ Get the gradients of the global model parameters """
        gradients = {}
        for name, param in self.model.named_parameters():
            if param.grad is not None:
                gradients[name] = param.grad.mean().item()
        return gradients

# Load and preprocess data
def load_data():
    url = "ratings_Electronics (1).csv"
    df = pd.read_csv(url)
    df.rename(columns={'AKM1MP6P0OYPR': 'userId', '0132793040': 'productId', '5.0': 'Rating', '1365811200': 'timestamp'}, inplace=True)
    df = df.head(5000)
    df.dropna(inplace=True)
    df.drop_duplicates(inplace=True)

    user_encoder = LabelEncoder()
    item_encoder = LabelEncoder()
    df['userId'] = user_encoder.fit_transform(df['userId'])
    df['productId'] = item_encoder.fit_transform(df['productId'])

    return df

def create_data_objects(df, split_ratio=0.2):
    train_df, test_df = train_test_split(df, test_size=split_ratio, random_state=42)
    train_df, val_df = train_test_split(train_df, test_size=split_ratio, random_state=42)

    edge_index = torch.tensor([train_df['userId'].values, train_df['productId'].values], dtype=torch.long)
    edge_attr = torch.tensor(train_df['Rating'].values, dtype=torch.float)
    num_users = df['userId'].nunique()
    num_items = df['productId'].nunique()
    num_nodes = num_users + num_items
    node_features = torch.eye(num_nodes)
    data = Data(edge_index=edge_index, edge_attr=edge_attr, x=node_features)
    
    train_loader = DataLoader([data], batch_size=1, shuffle=True)
    val_loader = DataLoader([data], batch_size=1, shuffle=False)
    
    return data, train_loader, val_loader

def model():
    # Initialize models and federated setup
    num_clients = 3
    df = load_data()
    client_data = [create_data_objects(df)[0] for _ in range(num_clients)]
    client_train_loaders = [create_data_objects(df)[1] for _ in range(num_clients)]
    client_val_loaders = [create_data_objects(df)[2] for _ in range(num_clients)]

    # Initialize the global model and server
    model = GCN(in_channels=client_data[0].x.size(1), hidden_channels=16, out_channels=1)
    server = FederatedServer(model, num_clients)

    # Federated learning rounds
    for round in range(5):  # Number of federated learning rounds
        client_models = []
        
        # Train clients
        for i, client_loader in enumerate(client_train_loaders):
            client = FederatedClient(model, client_loader)
            client.train(epochs=1)  # Train each client for 1 epoch
            client_models.append(client.get_model())
            
            # Evaluate client model
            val_loss = client.evaluate(client_val_loaders[i])
            print(f'Client {i + 1} Validation Loss: {val_loss}')
            
            # Inspect gradients
            gradients = client.get_gradients()
            print(f'Client {i + 1} Gradients: {gradients}')
        
        # Aggregate client models
        server.aggregate(client_models)
        
        # Evaluate global model
        test_loader = create_data_objects(df)[2]  # Use test loader for evaluation
        global_val_loss = server.evaluate(test_loader)
        print(f'Round {round + 1} Global Validation Loss: {global_val_loss}')
        
        # Inspect server model gradients
        server_gradients = server.get_gradients()
        print(f'Server Gradients: {server_gradients}')
        
        print(f'Round {round + 1} completed')

model()