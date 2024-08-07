# Federated Learning with Kafka

## Setup
0. git clone https://github.com/Norskeaksel/FederatedLearningWithKafka.git; cd FederatedLearningWithKafka
1. Make a virtual environment with: python -m venv env  
2. Activate with: source env/bin/activate on linux, env\Scripts\activate on windows  
3. pip3 install confluent-kafka
4. pip3 install tensorflow

## Running with local kafka cluster
0. Install and run docker desktop
1. docker compose up -d  
2a. python client.py <<< "local" with bash  
2b. python client.py and manually enter "local" with powershell  
3. python controller.py <<< "local" Only have ONE controller active at the time!
4. python produce_initial_weights.py  

## Running with confluent kafka cluster 
1.  Rename the [cloud_client_dummy.properties](kafkaLogic/config/cloud_client_dummy.properties) 
file to "cloud_client.properties" and get the sasl username and password from Aksel  
2a. python client.py <<< "cloud" with bash  
2b. python client.py and manually enter "cloud" with powershell  
3. python controller.py <<< "cloud" Only have ONE controller active at the time!