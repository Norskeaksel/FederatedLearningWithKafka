# Federated Learning with Kafka

## Setup
1. Make a virtual environment with: python -m venv env  
2. Activate with: source env/bin/activate on linux, env\Scripts\activate on windows  
3. pip3 install confluent-kafka  

## Running with local kafka cluster
1. docker compose up -d  
2a. python main.py <<< "local" with bash  
2b. python main.py and manually enter "local" with powershell  
3. python produce_initial_weights.py  

## Running with confluent kafka cluster 
1. Accuire the main.properties file from Aksel  
2a. python main.py <<< "cloud" with bash  
2b. python main.py and manually enter "cloud" with powershell  
