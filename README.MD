# Federated lerning with kafka

## Setup
1. Make a virtual environment with: python -m venv env
2. Activate with: source env/bin/activate on linux, env\Scripts\activate on windows
3. pip3 install confluent-kafka

## Running with local kafka cluster
1. docker compose up -d
2. python client.py <<< "local"

## Running with confluent kafka cluster 
1. Accuire the client.properties file from Aksel
2. python client.py <<< "cloud"
