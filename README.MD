# Federated Learning with Kafka

## Setup
1. Make a virtual environment with: python -m venv env  
2. Activate with: source env/bin/activate on linux, env\Scripts\activate on windows  
3. pip3 install confluent-kafka
4. pip3 install tensorflow
5. Give the consumerGroup variable in client.py a new name. It must be unique for each device.

## Running with local kafka cluster
1. docker compose up -d  
2a. python client.py <<< "local" with bash  
2b. python client.py and manually enter "local" with powershell  
3. python controller.py <<< "local"
4. python produce_initial_weights.py  

## Running with confluent kafka cluster 
1. Accuire the cloud_client.properties file from Aksel  
2a. python client.py <<< "cloud" with bash  
2b. python client.py and manually enter "cloud" with powershell  
3. python controller.py <<< "cloud"